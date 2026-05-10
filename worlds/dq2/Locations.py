# Look at init or Items.py for more information on imports
from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import DQ2World

# This is technique in programming to make things more readable for booleans
# A boolean is true or false
def did_include_extra_locations(world: "DQ2World") -> bool:
    return bool(False)

# This is used by ap and in Items.py
# Theres a multitude of reasons to need to grab how many locations there are
def get_total_locations(world: "DQ2World") -> int:
    # This is the total that we'll keep updating as we count how many locations there are
    total = 0
    for name in location_table:
        # If we did not turn on extra locations (see how readable it is with that thing from the top)
        # AND the name of it is found in our extra locations table, then that means we dont want to count it
        # So continue moves onto the next name in the table
        if not did_include_extra_locations(world) and name in extra_locations:
            continue

        # If the location is valid though, count it
        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    # This is just a fancy way of getting all the names and data in the location table and making a dictionary thats {name, code}
    # If you have dynamic locations then you want to add them to the dictionary as well
    names = {name: data.ap_code for name, data in location_table.items()}

    return names

# The check to make sure the location is valid
# I know it looks like the same as when we counted it but thats because this is an example
# Things get complicated fast so having a back up is nice
def is_valid_location(world: "DQ2World", name) -> bool:
    if not did_include_extra_locations(world) and name in extra_locations:
        return False

    return True

# You might need more functions as well so be liberal with them
# My advice, if you are about to type the same thing in a second time, turn it into a function
# Even if you only do it once you can turn it into a function too for organization

# Heres where you do the next fun part of listing out all those locations
# Its a lot
# My advice, zone out for half an hour listening to music and hope you wake up to a completed list
dq2_locations = {
    # You can take a peak at Types.py for more information but,
    # LocData is code, region in this instance
    # Regions will be explained more in Regions.py
    # But just know that it's mostly about organization
    # Place locations together based on where they are in the game and what is needed to get there


    "Midenhall Gold Key Chest 1": LocData(1, "Midenhall"),
    "Midenhall Gold Key Chest 2": LocData(2, "Midenhall"),
    "Midenhall Gold Key Chest 3": LocData(3, "Midenhall"),
    "Midenhall Gold Key Chest 4": LocData(4, "Midenhall"),
    "Token of Erdrick Chest": LocData(5, "Midenhall"),

    "Midenhall Item Shop 1": LocData(6, "Midenhall"),
    "Midenhall Item Shop 2": LocData(7, "Midenhall"),

    #Leftwyne
    "Leftwyne Item Shop 1": LocData(8, "Leftwyne"),
    "Leftwyne Item Shop 2": LocData(9, "Leftwyne"),
    "Leftwyne Item Shop 3": LocData(10, "Leftwyne"),

    "Leftwyne Weapon Shop 1": LocData(11, "Leftwyne"),
    "Leftwyne Weapon Shop 2": LocData(12, "Leftwyne"),
    "Leftwyne Weapon Shop 3": LocData(13, "Leftwyne"),
    "Leftwyne Weapon Shop 4": LocData(14, "Leftwyne"),
    "Leftwyne Weapon Shop 5": LocData(15, "Leftwyne"),
    "Leftwyne Weapon Shop 6": LocData(16, "Leftwyne"),
    # Cannock Partysanity Check?
    #"Prince Recruited": LocData(17, "Leftwyne"),

    #Cannock
    "Cannock Item Shop 1": LocData(18, "Cannock"),
    "Cannock Item Shop 2": LocData(19, "Cannock"),
    "Cannock Item Shop 3": LocData(20, "Cannock"),
    "Cannock Item Shop 4": LocData(21, "Cannock"),

    "Erdrick's Shield": LocData(22, "Cannock"),

    #Hamlin
    "Hamlin Item Shop 1": LocData(23, "Hamlin"),
    "Hamlin Item Shop 2": LocData(24, "Hamlin"),
    "Hamlin Item Shop 3": LocData(25, "Hamlin"),
    "Hamlin Item Shop 4": LocData(26, "Hamlin"),

    "Hamlin Weapon Shop 1": LocData(27, "Hamlin"),
    "Hamlin Weapon Shop 2": LocData(28, "Hamlin"),
    "Hamlin Weapon Shop 3": LocData(29, "Hamlin"),
    "Hamlin Weapon Shop 4": LocData(30, "Hamlin"),
    "Hamlin Weapon Shop 5": LocData(31, "Hamlin"),
    "Hamlin Weapon Shop 6": LocData(32, "Hamlin"),
    # Need Gold Key and Jailor's Key
    "Water Crest": LocData(33, "Hamlin"),
    # Moonbrooke Patysanity check?
    #"Princess Recruited": LocData(34, "Hamlin"),

    #Moonbrooke
    #"Moonbrooke Chest 1": LocData(35, "Moonbrooke"),
    #"Moonbrooke Chest 2": LocData(36, "Moonbrooke"),

    #Lake Cave
    "Lake Cave Chest 1": LocData(37, "Lake_Cave"),
    "Lake Cave Chest 2": LocData(38, "Lake_Cave"),
    "Lake Cave Chest 3": LocData(39, "Lake_Cave"),
    "Lake Cave Chest 4": LocData(40, "Lake_Cave"),
    "Lake Cave Chest 5": LocData(41, "Lake_Cave"),
    "Lake Cave Chest 6": LocData(42, "Lake_Cave"),
    "Silver Key Chest": LocData(43, "Lake_Cave"),
    
    #Spring of Bravery
    "Spring of Bravery Chest 1": LocData(44, "Spring_of_Bravery"),
    "Spring of Bravery Chest 2": LocData(45, "Spring_of_Bravery"),
    "Spring of Bravery Chest 3": LocData(46, "Spring_of_Bravery"),

    #Tower of the Wind
    "Tower of the Wind Chest 1": LocData(47, "Tower_of_the_Wind"),
    "Cloak of the Wind Chest": LocData(48, "Tower_of_the_Wind"),
    "Tower of the Wind Chest 2": LocData(49, "Tower_of_the_Wind"),
    #"Tower of the Wind Chest 3": LocData(50, "Tower_of_the_Wind"),

    #Dragon's Horn North Tower
    #"Dew's Yarn": LocData(51, "Dragons_Horn_North"),

    

    #Lianport
    "Lianport Item Shop 1": LocData(52, "Lianport"),
    "Lianport Item Shop 2": LocData(53, "Lianport"),
    "Lianport Item Shop 3": LocData(54, "Lianport"),
    "Lianport Item Shop 4": LocData(55, "Lianport"),
    "Lianport Item Shop 5": LocData(56, "Lianport"),

    "Lianport Weapon Shop 1": LocData(57, "Lianport"),
    "Lianport Weapon Shop 2": LocData(58, "Lianport"),
    "Lianport Weapon Shop 3": LocData(59, "Lianport"),
    "Lianport Weapon Shop 4": LocData(60, "Lianport"),
    "Lianport Weapon Shop 5": LocData(61, "Lianport"),
    "Lianport Weapon Shop 6": LocData(62, "Lianport"),
    # Defeat 2 Gremlins on West of town
    #"Ship Unlock": LocData(63, "Lianport"),
    # Need Sunken Treasure to trade, not properly implemented yet
    #"Echoing Flute": LocData(64, "Lianport"),

    #Tantegel
    "Tantegel Item Shop 1": LocData(65, "Tantegel"),
    "Tantegel Item Shop 2": LocData(66, "Tantegel"),
    "Tantegel Item Shop 3": LocData(67, "Tantegel"),
    "Tantegel Item Shop 4": LocData(68, "Tantegel"),
    "Tantegel Item Shop 5": LocData(69, "Tantegel"),

    "Tantegel Weapon Shop 1": LocData(70, "Tantegel"),
    "Tantegel Weapon Shop 2": LocData(71, "Tantegel"),
    "Tantegel Weapon Shop 3": LocData(72, "Tantegel"),
    "Tantegel Weapon Shop 4": LocData(73, "Tantegel"),
    "Tantegel Weapon Shop 5": LocData(74, "Tantegel"),
    "Tantegel Weapon Shop 6": LocData(75, "Tantegel"),

    #Charlock Castle
    "Erdrick's Sword Chest": LocData(76, "Charlock_Castle"),
    # Gold Key
    "Charlock Chest 1": LocData(77, "Charlock_Castle"),
    "Charlock Chest 2": LocData(78, "Charlock_Castle"),
    "Charlock Chest 3": LocData(79, "Charlock_Castle"),
    "Charlock Chest 4": LocData(80, "Charlock_Castle"),
    
    #Zahan
    "Zahan Item Shop 1": LocData(81, "Zahan"),
    "Zahan Item Shop 2": LocData(82, "Zahan"),
    "Zahan Item Shop 3": LocData(83, "Zahan"),
    "Zahan Item Shop 4": LocData(84, "Zahan"),

    "Gold Key": LocData(85, "Zahan"),
    # Jailor's Key/ Stepguard
    "Magic Loom": LocData(86, "Zahan"),
    #"Zahan Chest 1": LocData(87, "Zahan"),

    #Wellgarth
    "Wellgarth Jailor Item Shop 1": LocData(88, "Wellgarth"),
    "Wellgarth Jailor Item Shop 2": LocData(89, "Wellgarth"),
    "Wellgarth Jailor Item Shop 3": LocData(90, "Wellgarth"),
    "Jailor's Key": LocData(91, "Wellgarth"),
    # not the jailor key shop
    "Wellgarth Item Shop 1": LocData(92, "Wellgarth"),
    "Wellgarth Item Shop 2": LocData(93, "Wellgarth"),
    "Wellgarth Item Shop 3": LocData(94, "Wellgarth"),
    "Wellgarth Item Shop 4": LocData(95, "Wellgarth"),

    "Wellgarth Weapon Shop 1": LocData(96, "Wellgarth"),
    "Wellgarth Weapon Shop 2": LocData(97, "Wellgarth"),
    "Wellgarth Weapon Shop 3": LocData(98, "Wellgarth"),
    "Wellgarth Weapon Shop 4": LocData(99, "Wellgarth"),
    "Wellgarth Weapon Shop 5": LocData(100, "Wellgarth"),
    "Wellgarth Weapon Shop 6": LocData(101, "Wellgarth"),
    # Need Jailor's Key
    "Watergate Key": LocData(102, "Wellgarth"),

    #Fire Monolith
    "Sun Crest": LocData(103, "Fire_Shrine"),

    #Holy Shrine
    #"Erdrick's Helmet": LocData(104, "Holy_Shrine"),

    #Overworld Search Spots
    "Mirror of Ra": LocData(105, "Holy_Shrine"),
    "Sunken Treasure": LocData(106, "Holy_Shrine"),
    "Leaf of the World Tree": LocData(107, "Holy_Shrine"),

    #Beran
    "Beran Item Shop 1": LocData(108, "Beran"),
    "Beran Item Shop 2": LocData(109, "Beran"),
    "Beran Item Shop 3": LocData(110, "Beran"),
    "Beran Item Shop 4": LocData(111, "Beran"),

    "Beran Weapon Shop 1": LocData(112, "Beran"),
    "Beran Weapon Shop 2": LocData(113, "Beran"),
    "Beran Weapon Shop 3": LocData(114, "Beran"),
    "Beran Weapon Shop 4": LocData(115, "Beran"),
    "Beran Weapon Shop 5": LocData(116, "Beran"),
    "Beran Weapon Shop 6": LocData(117, "Beran"),

    #Osterfair Castle
    "Osterfair Weapon Shop 1": LocData(118, "Osterfair"),
    "Osterfair Weapon Shop 2": LocData(119, "Osterfair"),
    "Osterfair Weapon Shop 3": LocData(120, "Osterfair"),
    "Osterfair Weapon Shop 4": LocData(121, "Osterfair"),
    "Osterfair Weapon Shop 5": LocData(122, "Osterfair"),
    "Osterfair Weapon Shop 6": LocData(123, "Osterfair"),

    "Osterfair Shop Chest 1": LocData(124, "Osterfair"),
    "Osterfair Shop Chest 2": LocData(125, "Osterfair"),

    "Moon Crest": LocData(126, "Osterfair"),

    #Lighthouse
    "Lighthouse Chest 1": LocData(127, "Lighthouse"),
    "Lighthouse Chest 2": LocData(128, "Lighthouse"),
    "Lighthouse Chest 3": LocData(129, "Lighthouse"),
    "Lighthouse Chest 4": LocData(130, "Lighthouse"),

    "Star Crest": LocData(131, "Lighthouse"),

    #Tuhn
    "Tuhn Weapon Shop 1": LocData(132, "Tuhn"),
    "Tuhn Weapon Shop 2": LocData(133, "Tuhn"),
    "Tuhn Weapon Shop 3": LocData(134, "Tuhn"),
    "Tuhn Weapon Shop 4": LocData(135, "Tuhn"),
    "Tuhn Weapon Shop 5": LocData(136, "Tuhn"),
    "Tuhn Weapon Shop 6": LocData(137, "Tuhn"),

    "Tuhn Item Shop 1": LocData(138, "Tuhn"),
    "Tuhn Item Shop 2": LocData(139, "Tuhn"),
    "Tuhn Item Shop 3": LocData(140, "Tuhn"),

    # Need Dew's Yarn and Magic Loom, not implemented ran by dialogue
    #"Water Flying Cloth": LocData(141, "Tuhn"),

    #Moon Tower
    "Moon Tower Chest 1": LocData(142, "Moon_Tower"),
    "Moon Tower Chest 2": LocData(143, "Moon_Tower"),
    "Moon Tower Chest 3": LocData(144, "Moon_Tower"),
    "Moon Tower Chest 4": LocData(145, "Moon_Tower"),
    #"Moon Tower Chest 5": LocData(146, "Moon_Tower"),

    "Moon Fragment": LocData(147, "Moon_Tower"),

    #Sea Cave
    "Sea Cave Chest 1": LocData(148, "Sea_Cave"),
    "Sea Cave Chest 2": LocData(149, "Sea_Cave"),
    "Sea Cave Chest 3": LocData(150, "Sea_Cave"),
    "Sea Cave Chest 4": LocData(151, "Sea_Cave"),
    "Sea Cave Chest 5": LocData(152, "Sea_Cave"),
    "Sea Cave Chest 6": LocData(153, "Sea_Cave"),
    "Sea Cave Chest 7": LocData(154, "Sea_Cave"),

    "Eye of Malroth": LocData(155, "Sea_Cave"),

    #Cave to Rhone
    "Cave to Rhone Chest 1": LocData(156, "Cave_to_Rhone"),
    "Cave to Rhone Chest 2": LocData(157, "Cave_to_Rhone"),
    "Cave to Rhone Chest 3": LocData(158, "Cave_to_Rhone"),
    "Cave to Rhone Chest 4": LocData(159, "Cave_to_Rhone"),
    "Cave to Rhone Chest 5": LocData(160, "Cave_to_Rhone"),

    "Life Crest": LocData(161, "Cave_to_Rhone"),
    "Thunder Sword": LocData(162, "Cave_to_Rhone"),
    "Erdrick's Armor": LocData(163, "Cave_to_Rhone"),

    #Hargon's Castle
    #"Hargon's Castle Chest 1": LocData(164, "Hargons_Castle"),
    #"Hargon's Castle Chest 2": LocData(165, "Hargons_Castle"),

    #Shrine of Rubiss
    #Unimplemented, item given through dialogue
    #"Charm of Rubiss": LocData(166, "Shrine_of_Rubiss"),

    #win con lol
    "Malroth Defeated": LocData(167, "Hargons_Castle"),

}

extra_locations = {
    #"ml7's house": LocData(166, "Sibiu"),
}

# Like in Items.py, breaking up the different locations to help with organization and if something special needs to happen to them
event_locations = {
   
}

# Also like in Items.py, this collects all the dictionaries together
# Its important to note that locations MUST be bigger than progressive item count and should be bigger than total item count
# Its not here because this is an example and im not funny enough to think of more locations
# But important to note
location_table = {
    **dq2_locations,
    **extra_locations,
    **event_locations
}