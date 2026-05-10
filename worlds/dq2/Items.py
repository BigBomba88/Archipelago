# So the goal here is to have a catalog of all the items in your game
# To correctly generate a games items they need to be bundled in a list
# A list in programming terms is anything in square brackets [] to put it simply

# When a list is described its described as a list of x where x is the type of variable within it
# IE: ["apple", "pear", "grape"] is a list of strings (anything inside "" OR '' are considered strings)

# Logging = output. How you'll figure out whats going wrong
import logging

# Built in AP imports
from BaseClasses import Item, ItemClassification

# These come from the other files in this example. If you want to see the source ctrl + click the name
# You can also do that ctrl + click for any functions to see what they do
from .Types import ItemData, DQ2Item
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

# This is just making sure nothing gets confused dw about what its doing exactly
if TYPE_CHECKING:
    from . import DQ2World

# If you're curious about the -> List[Item] that is a syntax to make sure you return the correct variable type
# In this instance we're saying we only want to return a list of items
# You'll see a bunch of other examples of this in other functions
# It's main purpose is to protect yourself from yourself
def create_itempool(world: "DQ2World") -> List[Item]:
    # This is the empty list of items. You'll add all the items in the game to this list
    itempool: List[Item] = []
    locked_locations = 0

    # This creates your win item and then places it at the "location" where you win
    victory = create_item(world, "Victory")
    Boss = world.multiworld.get_location("Malroth Defeated", world.player)
    Boss.place_locked_item(victory)
    locked_locations += 1

    #world.multiworld.push_precollected(create_item(world, "Cash Card"))
    #world.multiworld.push_precollected(create_item(world, starting_character))

    shuffle_blacklist = [
        "Victory",
        "Cash Card",
    ]
    #shuffle_blacklist.append(starting_character)

    shuffle_pool = list(dq2_items.keys())
    shuffle_pool += list(event_items.keys())
    shuffle_pool += list(party_items.keys())


    for item in shuffle_pool:
        if item in shuffle_blacklist:
            continue
        if item_table[item].count > 1:
            itempool += create_multiple_items(world, item, item_table[item].count, item_table[item].classification)
        else:
            result_item = create_item(world, item)
            itempool.append(result_item)

    print(itempool)


    # Then junk items are made
    # Check out the create_junk_items function for more details
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool)-1) 

    return itempool

# This is a generic function to create a singular item
def create_item(world: "DQ2World", name: str) -> Item:
    data = item_table[name]
    return DQ2Item(name, data.classification, data.ap_code, world.player)

# Another generic function. For creating a bunch of items at once!
def create_multiple_items(world: "DQ2World", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [DQ2Item(name, item_type, data.ap_code, world.player)]

    return itemlist

# Finally, where junk items are created
def create_junk_items(world: "DQ2World", count: int) -> List[Item]:
    trap_chance = 0
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    # This grabs all the junk items and trap items
    for name in item_table.keys():
        # Here we are getting all the junk item names and weights
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

        # This is for traps if your randomization includes it
        # It also grabs the trap weights from the options page
        elif trap_chance > 0 and ic == ItemClassification.trap:
            if name == "StoneOrigin":
                trap_list[name] = world.options.StoneOriginTrapWeight.value
            elif name == "PoisnNeedl":
                trap_list[name] = world.options.PoisnNeedleTrapWeight.value

    # Where all the magic happens of adding the junk and traps randomly
    # AP does all the weight management so we just need to worry about how many are created
    for i in range(count):
        if trap_chance > 0 and world.random.randint(1, 100) <= trap_chance:
            junk_pool.append(world.create_item(
                world.random.choices(list(trap_list.keys()), weights=list(trap_list.values()), k=1)[0]))
        else:
            junk_pool.append(world.create_item(
                world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool

# Time for the fun part of listing all of the items
# Watch out for overlap with your item codes
# These are just random numbers dont trust them PLEASE
# I've seen some games that dynamically add item codes such as DOOM as well

dq2_items = {
# Progression items

#ITEMS EXPLICITLY REQUIRED TO REACH THE END
    "Silver Key": ItemData(1, ItemClassification.progression),
    "Gold Key": ItemData(2, ItemClassification.progression),
    "Jailor's Key": ItemData(3, ItemClassification.progression),
    
#not required but gets more checks
    "Watergate Key": ItemData(4, ItemClassification.progression),
    "Moon Fragment": ItemData(5, ItemClassification.progression),
    "Eye of Malroth": ItemData(6, ItemClassification.progression),
    #Location currently vanilla, item given through dialogue handlers
    #"Charm of Rubiss": ItemData(7, ItemClassification.progression),
    "Mirror of Ra": ItemData(8, ItemClassification.progression, 2),
    "Cloak of Wind": ItemData(9, ItemClassification.progression, 2),
    "Tresures": ItemData(10, ItemClassification.progression),
    "Echoing Flute": ItemData(11, ItemClassification.progression),
    "Magic Loom": ItemData(12, ItemClassification.progression),
    "Dew's Yarn": ItemData(13, ItemClassification.progression),
    "Token of Erdrick": ItemData(14, ItemClassification.progression),
    


# Useful items
    "Dragon's Potion": ItemData(20, ItemClassification.useful),

#game items
    #(7) are the global burger/drug vendors
    "Wizard's Ring": ItemData(21, ItemClassification.useful, 3),

    "Golden Card": ItemData(22, ItemClassification.useful),
    "Leaf of the World Tree": ItemData(23, ItemClassification.useful, 5),
    "Dragon's Bane": ItemData(24, ItemClassification.useful, 3),
    

#equipment
##weapons
    "Bamboo Stick": ItemData(25, ItemClassification.useful, 3),
    "Magic Knife": ItemData(26, ItemClassification.useful, 3),
    "Wizard's Wand": ItemData(27, ItemClassification.useful, 3),
    "Staff of Thunder": ItemData(28, ItemClassification.useful, 3),
    "Club": ItemData(29, ItemClassification.useful, 3),
    "Copper Sword": ItemData(30, ItemClassification.useful, 3),
    "Chain Sickle": ItemData(31, ItemClassification.useful, 3),
    "Iron Spear": ItemData(32, ItemClassification.useful, 3),
    "Falcon Sword": ItemData(33, ItemClassification.useful, 3),
    "Broad Sword": ItemData(34, ItemClassification.useful, 3),
    "Giant Hammer": ItemData(35, ItemClassification.useful, 3),
    "Sword of Destruction": ItemData(36, ItemClassification.useful, 3),
    "Dragon Killer": ItemData(37, ItemClassification.useful, 3),
    "Light Sword": ItemData(38, ItemClassification.useful, 3),
    "Sword of Erdrick": ItemData(39, ItemClassification.useful, 1),
    "Thunder Sword": ItemData(40, ItemClassification.useful),
    #Armor
    "Clothes": ItemData(41, ItemClassification.useful, 3),
    "Clothes Hiding": ItemData(42, ItemClassification.useful, 3),
    "Water Flying Cloth": ItemData(43, ItemClassification.useful, 3),
    "Mink Coat": ItemData(44, ItemClassification.useful, 3),
    "Leather Armor": ItemData(45, ItemClassification.useful, 2),
    "Chain Mail": ItemData(46, ItemClassification.useful, 2),
    "Gremlin's Armor": ItemData(47, ItemClassification.useful, 2),
    "Magic Armor": ItemData(48, ItemClassification.useful, 2),
    "Full Plate Armor": ItemData(49, ItemClassification.useful),
    "Armor of Gaia": ItemData(50, ItemClassification.useful),
    "Armor of Erdrick": ItemData(51, ItemClassification.useful),
    #Shields
    "Leather Shield": ItemData(52, ItemClassification.useful, 2),
    "Shield of Strength": ItemData(53, ItemClassification.useful, 2),
    "Steel Shield": ItemData(54, ItemClassification.useful),
    "Evil Shield": ItemData(55, ItemClassification.useful),
    "Shield of Erdrick": ItemData(56, ItemClassification.useful),
    #Helmets
    "Mysterious Hat": ItemData(57, ItemClassification.useful, 3),
    "Iron Helmet": ItemData(58, ItemClassification.useful),
    "Helmet of Erdrick": ItemData(59, ItemClassification.useful),

#borderline filler


    #Null: 10


# Victory is added here since in this organization it needs to be in the default item pool
    "Victory": ItemData(90, ItemClassification.progression)
}

event_items = {
    "Star Crest": ItemData(15, ItemClassification.progression),
    "Moon Crest": ItemData(16, ItemClassification.progression),
    "Sun Crest": ItemData(17, ItemClassification.progression),
    "Water Crest": ItemData(18, ItemClassification.progression),
    "Life Crest": ItemData(19, ItemClassification.progression),
    "Ship": ItemData(65, ItemClassification.progression),
}

party_items = {

}

# In the way that I made items, I added a way to specify how many of an item should exist
# That's why junk has a 0 since how many are created is in the create_junk_items
# There is a better way of doing this but this is my jank
junk_items = {
    # Junk
    "Medical Herb": ItemData(60, ItemClassification.filler, 10),
    "Antidote Herb": ItemData(61, ItemClassification.filler, 10),
    "Fairy Water": ItemData(62, ItemClassification.filler, 7),
    "Wing of the Wyvern": ItemData(63, ItemClassification.filler, 7),
    "Lottery Ticket": ItemData(64, ItemClassification.filler, 7),
    

    # Traps
    #causes Petrification
    # "StoneOrigin": ItemData(13, ItemClassification.trap, 0),
    #inflicts Poison
    # "PoisnNeedle": ItemData(14, ItemClassification.trap, 0),
}

# Junk weights is just how often an item will be chosen when junk is being made
# Bigger item = more likely to show up
junk_weights = {
    "Medical Herb": 30,
    "Antidote Herb": 30,
    "Fairy Water": 20,
    "Wing of the Wyvern": 20,
    "Lottery Ticket": 10,
}

# This makes a really convenient list of all the other dictionaries
# (fun fact: {} is a dictionary)
item_table = {
    **dq2_items,
    **event_items,
    **party_items,
    **junk_items,
}

