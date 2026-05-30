from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import DQ2World



# This is the last big thing to do (at least for me)
# This is where you add item
# These are omega simplified rules
# There are a ton of different ways you can add rules from amoount of items you need to optional items
# Theres also difficulty options and a bunch others
# Id suggest going through a bunch of different ap worlds and seeing how they do the rules
# Even better if its a game you know a lot about and can tell what you need to get to certain locations
def set_rules(world: "DQ2World"):
    player = world.player
    options = world.options

    # Chapter Access
    #IMPORTANT - add_rule is required to init the rule. otherwise add_rule should be fine
    #keys

    #MyHome
    
    for i in range(4) :
        add_rule(world.multiworld.get_location("Midenhall Gold Key Chest "+str(i+1), player),
             lambda state: state.has("Gold Key", player))
    add_rule(world.multiworld.get_location("Erdrick's Shield", player),
             lambda state: state.has("Gold Key", player))
    add_rule(world.multiworld.get_location("Token of Erdrick Chest", player),
             lambda state: state.has("Gold Key", player))
    add_rule(world.multiworld.get_location("Water Crest", player),
             lambda state: state.has_all(["Jailor's Key", "Gold Key"], player))
    # add_rule(world.multiworld.get_location("Princess Recruited", player),
    #          lambda state: state.has("Mirror of Ra", player))
    #add_rule(world.multiworld.get_location("Dew's Yarn", player),
    #         lambda state: state.has_any(["Ship", "Cloak of Wind"], player))
    #add_rule(world.multiworld.get_location("Echoing Flute", player),
    #         lambda state: state.has_all(["Ship", "Silver Key"], player))
    add_rule(world.multiworld.get_location("Star Crest", player),
             lambda state: state.has("Ship", player) and state.has("Gold Key", player))
    for i in range(4) :
        add_rule(world.multiworld.get_location("Charlock Chest "+str(i+1), player),
             lambda state: state.has("Gold Key", player))
    #add_rule(world.multiworld.get_location("Water Flying Cloth", player),
             #lambda state: state.has_all(["Dew's Yarn", "Gold Key", "Magic Loom"], player))
    add_rule(world.multiworld.get_location("Moon Fragment", player),
             lambda state: state.has("Ship", player) and state.has("Gold Key", player))
    for i in range(3) :
        add_rule(world.multiworld.get_location("Sea Cave Chest "+str(i+1), player),
             lambda state: state.has("Gold Key", player))
    add_rule(world.multiworld.get_location("Eye of Malroth", player),
             lambda state: state.has("Gold Key", player))
    #add_rule(world.multiworld.get_location("Erdrick's Helmet", player),
             #lambda state: state.has("Token of Erdrick", player))
    add_rule(world.multiworld.get_location("Watergate Key", player),
             lambda state: state.has("Jailor's Key", player))
    #add_rule(world.multiworld.get_location("Zahan Chest 1", player),
             #lambda state: state.has("Jailor's Key", player))
    add_rule(world.multiworld.get_location("Magic Loom", player),
             lambda state: state.has("Jailor's Key", player))
    add_rule(world.multiworld.get_location("Osterfair Shop Chest 1", player),
             lambda state: state.has("Gold Key", player))
    add_rule(world.multiworld.get_location("Osterfair Shop Chest 2", player),
             lambda state: state.has("Gold Key", player))
    add_rule(world.multiworld.get_location("Sunken Treasure", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_location("Leaf of the World Tree", player),
             lambda state: state.has("Ship", player))
    #add_rule(world.multiworld.get_location("Charm of Rubiss", player),
             #lambda state: state.has_all(["Ship", "Star Crest", "Moon Crest", "Sun Crest", "Water Crest", "Life Crest"], player))
    #Region Logic
    add_rule(world.multiworld.get_entrance("World -> Hamlin", player),
             lambda state: state.has_any(["Prince Recruited", "Ship"], player))
    add_rule(world.multiworld.get_entrance("World -> Moonbrooke", player),
             lambda state: state.has_any(["Prince Recruited", "Ship"], player))
    add_rule(world.multiworld.get_entrance("World -> Tower_of_the_Wind", player),
             lambda state: state.has_any(["Prince Recruited", "Ship"], player))
    add_rule(world.multiworld.get_entrance("World -> Dragons_Horn_South", player),
             lambda state: state.has_any(["Prince Recruited", "Ship"], player))
    add_rule(world.multiworld.get_entrance("World -> Dragons_Horn_North", player),
             lambda state: state.has_any(["Cloak of Wind", "Ship"], player))
    add_rule(world.multiworld.get_entrance("World -> Lianport", player),
             lambda state: state.has_any(["Cloak of Wind", "Ship"], player))
    add_rule(world.multiworld.get_entrance("World -> Tantegel", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Charlock_Castle", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Lighthouse", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Tuhn", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Beran", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("Tuhn -> Moon_Tower", player),
             lambda state: state.has_all(["Ship", "Jailor's Key", "Watergate Key"], player))
    add_rule(world.multiworld.get_entrance("World -> Sea_Cave", player),
             lambda state: state.has_all(["Ship", "Moon Fragment"], player))
    add_rule(world.multiworld.get_entrance("Beran -> Cave_to_Rhone", player),
             lambda state: state.has_all(["Jailor's Key", "Eye of Malroth"], player))
    add_rule(world.multiworld.get_entrance("Cave_to_Rhone -> Hargons_Castle", player),
             lambda state: state.has_all(["Jailor's Key"], player))
    add_rule(world.multiworld.get_entrance("World -> Fire_Shrine", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Holy_Shrine", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Wellgarth", player),
             lambda state: state.has_all(["Ship", "Gold Key"], player))
    add_rule(world.multiworld.get_entrance("World -> Zahan", player),
             lambda state: state.has("Ship", player))
    add_rule(world.multiworld.get_entrance("World -> Osterfair", player),
             lambda state: state.has("Ship", player))

    #add Spookane, Reindeer, and Snowman based on whether or not you want to
    #walk for five years and also probably die a lot
    

    # Victory condition rule!
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
