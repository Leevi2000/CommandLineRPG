from objects import *

class Items:
    money = Item("Silver Coin", 0.01, 0, 1)
    rogue_dagger = Weapon("Rogue's Dagger", 0.3, 5, 10, "Ominous marks around the dagger makes makes anyone wonder what the dagger has seen", 3, 1)

# Holds list of different kind of NPC variables that can be used in game
class NPCs:
    rogue = NPC(5, 1, "Violent Rogue", 3, "Shady figure with tattered clothing", "rogue.txt", "I've got some other business to do, I'm leavin'")
    rogue.items.append([Items.rogue_dagger, 1])

    drunken_guard_of_windermere = NPC(1, 10, "Drunken Guard", 1, "Drunken Guard that looks like he is a hazard to himself", "drunken_guard_of_windermere.txt", "See you around, I gotta leave")
    drunken_guard_of_windermere.items.append([Items.money, 10])

