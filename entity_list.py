from objects import Item


class Items:
    from objects import Item, Weapon, Healing, Armor

    fists = Weapon("Fists", 0, 0, 0, "", 1, 0.5)

    money = Item("Silver Coin", 0.01, 0, 1)
    rogue_dagger = Weapon("Rogue's Dagger", 0.3, 5, 10, "A swift, lightweight dagger perfect for stealth and quick strikes.", 3, 1)

    apple = Healing("Apple", 0.2, 1, 3, "Looks so delicious that you could eat it straight away", 2)
    leather_tunic = Armor("Leather tunic", 3, 0, 10, "A piece of armor, looks comfortable", 2, "chest")


# Holds list of different kind of NPC variables that can be used in game
class NPCs:
    from objects import NPC
    rogue = NPC(6, Items.rogue_dagger.damage, "Violent Rogue", 2, "Shady figure with tattered clothing", "rogue.txt", "I've got some other business to do, I'm leavin'")
    rogue.add_item(Items.rogue_dagger, 1)

    drunken_guard_of_windermere = NPC(1, 10, "Drunken Guard", 1, "Drunken Guard that looks like he is a hazard to himself", "drunken_guard_of_windermere.txt", "See you around, I gotta leave")
    drunken_guard_of_windermere.add_item(Items.money, 10)
    trader_of_windermere = NPC(1, 4, "Gustavus von Wittenberg", 1, "Tall figure smiling at you from a market stall", "trader_of_windermere.txt")
    trader_of_windermere.add_item(Items.apple, 3)
    trader_of_windermere.add_item(Items.leather_tunic, 1)
    trader_of_windermere.detailed_description = "He has a fancy moustache, dark cloak and worn out leather boots."
