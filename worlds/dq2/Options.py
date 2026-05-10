from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

# If youve ever gone to an options page and seen how sometimes options are grouped
# This is that
def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in dq2_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class MysteriousHatFix(Toggle):
    """
    When this setting is toggled, the Mysterious Hat will ACTUALLY half the MP Cost of all spells in battle, unlike base game.
    """
    display_name = "Mysterious Hat Fix"
    default = 1

class GlobalEquipment(Toggle):
    """
    When this setting is toggled, all characters can wear any equipment. This makes characters stronger than they usually would be. (Cannock is no longer useless :))
    """
    display_name = "Global Equipment"
    default = 0

class ExpModifier(Range):
    """
    Modifies the game's level curves.
    Multiplies XP Values, setting range to 2 is 2x, 3 for 3x, etc.

    Default Value is 3x
    """
    display_name = "Exp Modifier"
    range_start = 1
    range_end = 5
    default = 3

@dataclass
class DQ2Options(PerGameCommonOptions):
    MysteriousHatFix:           MysteriousHatFix
    GlobalEquipment:           GlobalEquipment
    ExpModifier:                ExpModifier

# This is where you organize your options
# Its entirely up to you how you want to organize it
dq2_option_groups: Dict[str, List[Any]] = {
    "General Options": [MysteriousHatFix, ExpModifier, GlobalEquipment],
    "Trap Options": []
}