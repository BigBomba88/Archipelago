import base64
import logging

from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import read, write, guarded_write, display_message

logger = logging.getLogger("Client")

from .Locations import location_table
from .Items import item_table, event_items, party_items
from .rom_data import rom_item_table, all_object_codes, \
all_present_flags, all_story_flags

class DQ2Client(BizHawkClient):
    system = ("NES")
    patch_suffix = ".apdq2"
    game = "DQ2"


    variables = {
        "Crests": (0x112, 1, "RAM"),
        "COLLECTEDITEMS": (0x520, 6, "WRAM"),
        "APIn": (0x510, 0x10, "WRAM"),
        "APOut": (0x500, 7, "WRAM"),
        "Malroth_Flag": (0xD0, 1, "RAM"),
        "Ship": (0xcf, 1, "RAM"),
        "Inventory": (0x600, 24, "RAM"),
        "Midenhall Status": (0x62d, 1, "RAM"),
        "Cannock Status": (0x63f, 1, "RAM"),
        "Moonbrooke Status": (0x651, 1, "RAM"),
    }

    def __init__(self):
        super().__init__()
        self.locations_array = []
        self.recieved_items = []
        self.previous_level = None

        self.init_to_merrsyville = False

    async def validate_rom(self, ctx):
        game_name = await read(ctx.bizhawk_ctx, [(0x3FE0, 0x10, "PRG ROM")])
        game_name = game_name[0].decode("ascii")
        if game_name != "DRAGON WARRIORS2":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
        return True

    #async def set_auth(self, ctx):
    #    auth_name = await read(ctx.bizhawk_ctx, [(0x77777, 21, "ROM")])
    #    auth_name = base64.b64encode(auth_name[0]).decode()
    #    ctx.auth = auth_name

    def cliprint(self, string):
        logger.log(1, string)

    async def bizprint(self, string, ctx):
        await display_message(ctx, string)

    async def game_watcher(self, ctx):
        await super().game_watcher(ctx)

        locations_checked = []
        data_writes = []

        ram_variables = {}
        args = await read(ctx.bizhawk_ctx, list(self.variables.values()))

        i = 0
        for value in args:
            name = list(self.variables.keys())[i]
            ram_variables[name] = value
            #self.cliprint(name)
            #self.cliprint(value.hex())
            i += 1

        #wait until game started
        #if ram_variables["PlayerName"] != bytearray([0xFF] * 0x10):

        #workaround for flag 135

        #workaround for win con
        #check for switch to credits music bank
        # to do later, fix
        if ram_variables["Malroth_Flag"][0] == 0xFF:
            locations_checked.append(locations_checked.append(location_table["Malroth Defeated"].ap_code))
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        send_item = ram_variables["APOut"]
        mapid = send_item[0]
        mapxpos = send_item[1]
        mapypos = send_item[2]
        chestid = send_item[3]
        shopid = send_item[4]
        choicer = send_item[5]
        confirmation = send_item[6]
        self.cliprint(str((mapid, mapxpos, mapypos, chestid, shopid, choicer)))
        if send_item[0] != 0x0:
            if mapid != 0xFF:
                to_compare = (mapid, mapxpos, mapypos)
                for data in list(all_object_codes.keys()):

                    match = False
                    #include choicer
                    if len(data) <= 2:
                        continue

                    idata = data[:-1]
                    match = idata == to_compare

                    if match:
                        value = all_object_codes[data]
                        await self.bizprint(value, ctx.bizhawk_ctx)
                        locations_checked.append(location_table[value].ap_code)
                        break
            new = list(self.variables["APOut"])
            new[1] = [0xff] * new[1]
            new[1][0] = 0
            data_writes.append(new)
        if shopid !=0xFF and confirmation == 0x0:
            to_compare = (shopid, choicer)
            for data in list(all_object_codes.keys()):

                match = False
                #include choicer
                if len(data) > 2:
                    continue

                match = data == to_compare

                if match:
                    value = all_object_codes[data]
                    await self.bizprint(value, ctx.bizhawk_ctx)
                    locations_checked.append(location_table[value].ap_code)
                    break

            #cleanup
            new = list(self.variables["APOut"])
            new[1] = [0xff] * new[1]
            new[1][0] = 0
            data_writes.append(new)
        if len(locations_checked) > 0:
            self.cliprint(locations_checked)
        #receival handler
        self.recieved_items = ctx.items_received

        #internal rom collected items counter
        #literally required
        counter = int.from_bytes(ram_variables["COLLECTEDITEMS"], 'little')
        if counter == 0xFFFFFFFFFFFF:
            counter = 0

        #if mismatch, update as needed
        if len(self.recieved_items) > counter:
            #figure out how to give items
            wip_apin = bytearray(ram_variables["Inventory"])

            #TODO: does not account for party rando :)
            has_midenhall = (ram_variables["Midenhall Status"][0] & 0b00000100) >> 2
            has_cannock = (ram_variables["Cannock Status"][0] & 0b00000100) >> 2
            has_moonbrooke = (ram_variables["Moonbrooke Status"][0] & 0b00000100) >> 2

            total_party = has_midenhall + has_cannock + has_moonbrooke
            inventory_size = total_party * 8
            #stop at last (available) inventory slot
            inventory_wip = wip_apin[:inventory_size]


            #1. there is room in queue
            #2. you are below the recieved item count
            #keep adding items to queue
            while wip_apin.count(0) > 0 and len(self.recieved_items) > counter:
                the_item = self.recieved_items[counter]

                #get item name
                ret_name = ""
                for item in list(item_table.keys()):
                    if item_table[item].ap_code == the_item.item:
                        ret_name = item
                        break
                if ret_name == "":
                    self.cliprint("how")

                #if the location is from a non-item given location in base game, use multiplayer input
                if ret_name in list(event_items.keys()):
                    #event items
                    if ret_name == "Sun Crest":
                        currentcrests = ram_variables["Crests"][0]
                        currentcrests |= 0b00000001
                        #remove rocks
                        data_writes.append((0x112, [currentcrests], "RAM"))
                        counter += 1
                        continue
                    elif ret_name == "Star Crest":
                        currentcrests = ram_variables["Crests"][0]
                        currentcrests |= 0b00000010
                        #remove rocks
                        data_writes.append((0x112, [currentcrests], "RAM"))
                        counter += 1
                        continue
                    elif ret_name == "Moon Crest":
                        currentcrests = ram_variables["Crests"][0]
                        currentcrests |= 0b00000100
                        #remove rocks
                        data_writes.append((0x112, [currentcrests], "RAM"))
                        counter += 1
                        continue
                    elif ret_name == "Water Crest":
                        currentcrests = ram_variables["Crests"][0]
                        currentcrests |= 0b00001000
                        #remove rocks
                        data_writes.append((0x112, [currentcrests], "RAM"))
                        counter += 1
                        continue
                    elif ret_name == "Life Crest":
                        currentcrests = ram_variables["Crests"][0]
                        currentcrests |= 0b00010000
                        #remove rocks
                        data_writes.append((0x112, [currentcrests], "RAM"))
                        counter += 1
                        continue
                    elif ret_name == "Ship":
                        ship_status = ram_variables["Ship"][0]
                        ship_status |= 0b00000010
                        #remove rocks
                        data_writes.append((0xcf, [ship_status], "RAM"))
                        counter += 1
                        continue

                    else:
                        counter += 1
                        continue


		#if no physical inventory space, completely skip items
                elif inventory_wip.count(0) <= 0:
                    break

                #all of this only matters if the item is for this world (and not an event item)
                if the_item.player == ctx.slot:
                    self.cliprint("GOT ITEM FOR SELF!! HANDLE NOW")

                    #get item name
                    ret_loc_name = ""
                    for location in list(location_table.keys()):
                        if location_table[location].ap_code == the_item.location:
                            ret_loc_name = location
                            break
                    if ret_loc_name == "":
                        self.cliprint("how")

                    if ret_loc_name in list(all_story_flags.values()):
                        self.cliprint("ITEM IS OKAY TO GIVE!!")
                    else:
                        self.cliprint("ITEM IS NOT OKAY TO GIVE!!")
                        self.cliprint("IT IS GIVEN THROUGH AN ITEM GIVER!!")
                        self.cliprint("IMPLEMENT PROPERLY DICKHEAD!!")
                        counter += 1
                        continue

                #at this point, an item is okay to be given to the player
                #check against actual rom data to make sure it is a valid item
                self.cliprint(f"got item {ret_name}")
                rom_item_id = 0xff
                if ret_name in list(rom_item_table.keys()):
                    rom_item_id = rom_item_table[ret_name].rom_id
                else:
                    self.cliprint("lmfao/. not implemented yet :)")
                    counter += 1
                    continue

                #add to queue
                self.cliprint(wip_apin)
                self.cliprint(rom_item_id)
                wip_apin[wip_apin.index(0)] = rom_item_id
                counter += 1

            #cleanup
            #write back to emulator
            new = list(self.variables["Inventory"])
            new[1] = wip_apin
            data_writes.append(new)

            #update the count!!
            new = list(self.variables["COLLECTEDITEMS"])
            new[1] = int.to_bytes(counter, 6, 'little')
            data_writes.append(new)




        #write to emu
        if len(data_writes) > 0:
            success = await write(ctx.bizhawk_ctx, data_writes)

        #if not connected, dont checkloc
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        if len(locations_checked) > 0:
            self.locations_array = locations_checked
            await ctx.check_locations(locations_checked)

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)
        #if cmd == 'Connected':
        #    if ctx.slot_data["energy_link"]:
        #        ctx.set_notify(f"EnergyLink{ctx.team}")
        #        if ctx.ui:
        #            ctx.ui.enable_energy_link()
        #            ctx.ui.energy_link_label.text = "Lives: Standby"
        #elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
        #    if ctx.ui:
        #        ctx.ui.energy_link_label.text = f"Lives: {int(args['value'] / BANK_EXCHANGE_RATE)}"
        #elif cmd == "Retrieved":
        #    if f"EnergyLink{ctx.team}" in args["keys"] and args['keys'][f'EnergyLink{ctx.team}'] and ctx.ui:
        #        ctx.ui.energy_link_label.text = f"Lives: {int(args['keys'][f'EnergyLink{ctx.team}'] / BANK_EXCHANGE_RATE)}"
