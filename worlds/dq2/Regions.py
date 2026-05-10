from BaseClasses import Region
from .Types import DQ2Location
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DQ2World

# This is where you will create your imaginary game world
# IE: connect rooms and areas together
# This is NOT where you'll add requirements for how to get to certain locations thats in Rules.py
# This is also long and tediouos
def create_regions(world: "DQ2World"):
    # The functions that are being used here will be located at the bottom to view
    # The important part is that if its not a dead end and connects to another place then name it
    # Otherwise you can just create the connection. Not that naming it is bad

    # You can technically name your connections whatever you want as well
    # You'll use those connection names in Rules.py
    r_world = create_region(world, "World")
    Midenhall = create_region_and_connect(world, "Midenhall", "World -> Midenhall", r_world)
    Leftwyne = create_region_and_connect(world, "Leftwyne", "World -> Leftwyne", r_world)
    Cannock = create_region_and_connect(world, "Cannock", "World -> Cannock", r_world)
    Lake_Cave = create_region_and_connect(world, "Lake_Cave", "World -> Lake_Cave", r_world)
    Spring_of_Bravery = create_region_and_connect(world, "Spring_of_Bravery", "World -> Spring_of_Bravery", r_world)
    # Make proper logic later, need 1 party member to proceed to Hamlin from Monolith or Ship
    Cannock_Monolith = create_region_and_connect(world, "Cannock_Monolith", "World -> Cannock_Monolith", r_world)
    Hamlin = create_region_and_connect(world, "Hamlin", "World -> Hamlin", r_world)
    Moonbrooke = create_region_and_connect(world, "Moonbrooke", "World -> Moonbrooke", r_world)
    Moonbrooke_Monolith = create_region_and_connect(world, "Moonbrooke_Monolith", "World -> Moonbrooke_Monolith", r_world)
    Tower_of_the_Wind = create_region_and_connect(world, "Tower_of_the_Wind", "World -> Tower_of_the_Wind", r_world)
    Dragons_Horn_South = create_region_and_connect(world, "Dragons_Horn_South", "World -> Dragons_Horn_South", r_world)
    # Make proper logic later, need Cloak of the Wind to proceed or Ship
    Dragons_Horn_North = create_region_and_connect(world, "Dragons_Horn_North", "World -> Dragons_Horn_North", r_world)
    Lianport = create_region_and_connect(world, "Lianport", "World -> Lianport", r_world)
    Tantegel = create_region_and_connect(world, "Tantegel", "World -> Tantegel", r_world)
    Charlock_Castle = create_region_and_connect(world, "Charlock_Castle", "World -> Charlock_Castle", r_world)
    Lighthouse = create_region_and_connect(world, "Lighthouse", "World -> Lighthouse", r_world)
    # Make proper logic later, need Jailor's Key and Watergate Key to get Moon fragment from Moon Tower
    Tuhn = create_region_and_connect(world, "Tuhn", "World -> Tuhn", r_world)
    Beran = create_region_and_connect(world, "Beran", "World -> Beran", r_world)
    # Make proper logic later, need Watergate Key to proceed to Moon Tower
    Moon_Tower = create_region_and_connect(world, "Moon_Tower", "Tuhn -> Moon_Tower", Tuhn)
    # Make proper logic later, need Moon Fragment to proceed to Sea Cave
    Sea_Cave = create_region_and_connect(world, "Sea_Cave", "World -> Sea_Cave", r_world)
    # Make proper logic later, need Eye of Malroth to proceed to Cave to Rhone
    Cave_to_Rhone = create_region_and_connect(world, "Cave_to_Rhone", "Beran -> Cave_to_Rhone", Beran)
    # Make proper logic later, need Charm of Rubiss to proceed to Hargon
    Hargons_Castle = create_region_and_connect(world, "Hargons_Castle", "Cave_to_Rhone -> Hargons_Castle", Cave_to_Rhone)
    # Shrines and other towns
    Fire_Shrine = create_region_and_connect(world, "Fire_Shrine", "World -> Fire_Shrine", r_world)
    Zahan = create_region_and_connect(world, "Zahan", "World -> Zahan", r_world)
    Wellgarth = create_region_and_connect(world, "Wellgarth", "World -> Wellgarth", r_world)
    Holy_Shrine = create_region_and_connect(world, "Holy_Shrine", "World -> Holy_Shrine", r_world)
    Osterfair = create_region_and_connect(world, "Osterfair", "World -> Osterfair", r_world)
    Shrine_of_Rubiss = create_region_and_connect(world, "Shrine_of_Rubiss", "World -> Shrine_of_Rubiss", r_world)


    #romania = create_region_and_connect(world, "Romania", "Menu -> Romania", menu)
    #sewer = create_region_and_connect(world, "The Sewer", "Menu -> The Sewer", menu)

    # ---------------------------------- Green Hill Zone ----------------------------------
    #greenhillzone1 = create_region_and_connect(world, "Green Hill Zone - Act 1", "Green Hill Zone -> Green Hill Zone - Act 1", greenhillzone)
    #greenhillzone2 = create_region_and_connect(world, "Green Hill Zone - Act 2", "Green Hill Zone - Act 1 -> Green Hill Zone - Act 2", greenhillzone1)
    #create_region_and_connect(world, "Green Hill Zone - Act 3", "Green Hill Zone - Act 2 -> Green Hill Zone - Act 3", greenhillzone2)

    # ---------------------------------- Romania ------------------------------------------
    #bucharest = create_region_and_connect(world, "Bucharest", "Romania -> Bucharest", romania)
    #sibiu = create_region_and_connect(world, "Sibiu", "Romania -> Sibiu", romania)
    #brașov = create_region_and_connect(world, "Brașov", "Romania -> Brașov", romania)
    #bucharest.connect(sibiu, "Bucharest -> Sibiu")
    #sibiu.connect(brașov, "Sibiu -> Brașov")
    #brașov.connect(bucharest, "Brașov, Bucharest")

    # ---------------------------------- The Sewer ----------------------------------------
    #create_region_and_connect(world, "Big Hole in the Floor", "The Sewer -> Big Hole in the Floor", sewer)

def create_region(world: "DQ2World", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    # When we create the region we go through all the locations we made and check if they are in that region
    # If they are and are valid, we attach it to the region
    for (key, data) in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = DQ2Location(world.player, key, data.ap_code, reg)
            reg.locations.append(location)

    world.multiworld.regions.append(reg)
    return reg

# This runs the create region function while also connecting to another region
# Just simplifies process since you woill be connecting a lot of regions
def create_region_and_connect(world: "DQ2World",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg