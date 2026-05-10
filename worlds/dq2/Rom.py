import hashlib
import os
import pkgutil

import Utils

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .Items import event_items

from typing import TYPE_CHECKING, Dict, List, Tuple

from .rom_data import rom_item_table, item_place_locations, MP_Cost,\
Exp_Table1, Exp_Table2, Exp_Table3, EquipFields, MPCostsTable, \
EXPTablePointer

if TYPE_CHECKING:
    from . import DQ2World

def generate_output(world: "DQ2World", output_directory: str):
    patch = DQ2ProcedurePatch(player=world.player, player_name=world.player_name)

    patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "basepatch.bsdiff4"))

    actual_location_table = {}

    for location in world.multiworld.get_locations(world.player):
        if location.item is None:
            continue

        #get item byte
        the_item = location.item
        if the_item.player != world.player:
            #if is offworld item

            #if being placed at a chest
            if location.name.find("Chest") != -1:
                #make the chest have nothing :)
                the_item = 0
            else:
                the_item = 0x3F
        else:
            #if item is also an event item
            if the_item.name in list(event_items.keys()):
                #if being placed at a chest
                if location.name.find("Chest") != -1:
                    #make the chest have nothing :)
                    the_item = 0
                else:
                    the_item = 0x3F
            else:
                #if it is a real game item, make it an id
                print(the_item.name)
                if the_item.name in list(rom_item_table.keys()):
                    the_item = rom_item_table[the_item.name].rom_id
                else:
                    the_item = 0x3F
                    #TODO: handle event items/not actual items
                    #continue
                    print("fail")

        actual_location_table[location.name] = the_item

    for setter in list(item_place_locations.keys()):
        location_name = item_place_locations[setter]
        if location_name in list(actual_location_table.keys()):
            item = actual_location_table[location_name]
            bank, offset = setter
            rates = (bank*0x4000) + (offset-0x8000) + 0x10
            patch.write_bytes(rates, item)

    # #write exp mod
    if bool(world.options.MysteriousHatFix.value):
        x = 0
        for i in MP_Cost:
            patch.write_bytes(MPCostsTable + len(MP_Cost) + x, i//2)
            x += 1

    if bool(world.options.GlobalEquipment.value):
        x = 0
        for i in range(0x24):
            patch.write_bytes(EquipFields + x, 0b00000111)
            x += 1

    if world.options.ExpModifier.value != 1:
        x = 0
        for i in Exp_Table1 + Exp_Table2 + Exp_Table3:
            patch.write_bytes(EXPTablePointer + (2*x), int.to_bytes(i//world.options.ExpModifier.value, length=2, byteorder="little"))
            x += 1


    patch.write_file("tokens.bin", patch.get_token_binary())
    patch.write(os.path.join(output_directory,
                             f"{world.multiworld.get_out_file_name_base(world.player)}{patch.patch_file_ending}"))


class DQ2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = "3188792f0e6baee937a9859542c8c155"
    patch_file_ending = ".apdq2"
    game = "DQ2"
    result_file_ending = ".nes"
    procedure = [
        ("apply_bsdiff4", ["basepatch.bsdiff4"]),
        ("apply_tokens", ["tokens.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset, value):
        if isinstance(value, int):
            value = [value]
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def get_base_rom_bytes():
    file_name = get_base_rom_path()
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if DQ2ProcedurePatch.hash != basemd5.hexdigest():
        raise Exception("Supplied Base Rom does not match known MD5 for Dragon Warrior 2. "
                        "Get the correct game and version, then dump it")
    return base_rom_bytes


def get_base_rom_path():
    file_name = get_settings()["dq2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
