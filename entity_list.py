from objects import Item


class Items:
    from objects import Item, Weapon, Healing, Armor

    godsword = Weapon("Holy Blade", 1, 100, 10000, "Wielder gains otherworldly powers", 100, 1)

    fists = Weapon("Fists", 0, 0, 0, "", 1, 0.5)

    money = Item("Silver Coin", 0.01, 0, 1)
    rogue_dagger = Weapon("Rogue's Dagger", 0.3, 5, 10, "A swift, lightweight dagger perfect for stealth and quick strikes.", 3, 1)

    apple = Healing("Apple", 0.2, 1, 3, "Looks so delicious that you could eat it straight away", 2)
    leather_tunic = Armor("Leather tunic", 3, 0, 10, "A piece of armor, looks comfortable", 2, "chest")

    bilberry = Healing("Bilberry", 0.1, 0, 2, "Small, tasty berry", 1)
    
    mysterious_rock = Weapon("Mysterious rock", 4, 15, 10, "Holding the rock in my hand creates a poweful feeling, yet wielding the rock does not work well... How is that possible", 2, 5)

    bear_meat = Healing("Bear meat", 5, 2, 15, "Delicious looking meat.", 10)

    aether_shard = Item("Aether shard", 1, 2, 30, "Shard carried by Elderglow Nymphs glows with otherworldy colours when placed in direct sunlight")
    shroud_of_mistwarden = Armor("Shroud Of Mistwarden", 0.1, 0, 50, "A shimmering cloak made of pure mist. When worn, mist compresses itself around you to create a firm, defensive layer", 5, "chest")
    mistbound_roots = Healing("Mistbound Roots", 0.1, 0, 20, "Gnarled roots wrapped in a soft, glowing mist, still pulsing with life.", 20)

    fenlight_crystal = Item("Fenlight Crystal", 2, 4, 25, "A small, pale crystal that glows faintly when held.")

    mossy_bark_greaves = Armor("Mossy bark greaves", 4, 2, 20, "You can still feel Elder Myrrow's protective spell flowing through the trousers")

    wooden_dart = Weapon("Wooden Dart", 0.2, 1, 5, "ordinary darts, nothing special", 2, 1)

    mushroom = Healing("Red Mushroom", 0.1, 0, 4, "Basic mushrooms", 2)


# Holds list of different kind of NPC variables that can be used in game
class NPCs:
    from objects import NPC

    # --------------------------------
    # Town of Windermere NPC's
    # --------------------------------
    rogue = NPC(6, Items.rogue_dagger.damage, "Violent Rogue", 2, "Shady figure with tattered clothing", "rogue.txt", "I've got some other business to do, I'm leavin'")
    rogue.add_item(Items.rogue_dagger, 1)

    drunken_guard_of_windermere = NPC(1, 10, "Drunken Guard", 1, "Drunken Guard that looks like he is a hazard to himself", "drunken_guard_of_windermere.txt", "See you around, I gotta leave")
    drunken_guard_of_windermere.add_item(Items.money, 10)
    trader_of_windermere = NPC(1, 4, "Gustavus von Wittenberg", 1, "Tall figure smiling at you from a market stall", "trader_of_windermere.txt")
    trader_of_windermere.add_item(Items.apple, 3)
    trader_of_windermere.add_item(Items.leather_tunic, 1)
    trader_of_windermere.detailed_description = "He has a fancy moustache, dark cloak and worn out leather boots."

    # --------------------------------
    # Forest of Windermere NPC's
    # --------------------------------

    bear = NPC(15, 6, "Furious Bear", 1, "shade of a moving, round like creature", "furious_bear.txt")
    bear.add_item(Items.bear_meat, 2)

    FOW_mysterious_man = NPC(8, 20, "Mysterious Man", 5, "ominous looking human with a rugged beard", "mysterious_man.txt")
    FOW_mysterious_man.add_item(Items.mysterious_rock)

    FOW_small_goblin_army = NPC(15, 2, "Greedy Goblins", 1, "Flock of Goblins sparkling with excitement with an addition of greed in their eyes", "FOW_goblin_army.txt")

    # --------------------------------
    # Evermist Glade NPC's
    # --------------------------------

    EG_lost_seeker = NPC(1, 1, "The Lost Seeker", 1, "A spectral being resembling a human", "EG_lost_seeker.txt")

    EG_elderglow_nymph = NPC(10, 5, "Elderglow Nymph", 2, "Ethereal looking, humanoid creature", "EG_elderglow_nymph.txt")
    EG_elderglow_nymph.add_item(Items.aether_shard)

    EG_mistwarden = NPC(30, 8, "The Mistwarden", 10, "A tall, ghostly figure cloaked in flowing robes of mist", "EG_mistwarden.txt")
    EG_mistwarden.add_item(Items.shroud_of_mistwarden)
    EG_mistwarden.add_item(Items.mistbound_roots)

    # --------------------------------
    # Moonlit Fen NPC's
    # --------------------------------

    MF_lumina_twins = NPC(12, 5, "The Lumina Twins", 0.3, "Two spirits, who appear to be made of faintly glowing mist", "MF_lumina_twins.txt")
    MF_lumina_twins.add_item(Items.fenlight_crystal)

    MF_elder_myrrow = NPC(20, 10, "Elder Myrrow", 4, "Humanoid creature with bark-like skin and moss growing across their body", "MF_elder_myrrow.txt")
    MF_elder_myrrow.create_reward(Items.fenlight_crystal, Items.mossy_bark_greaves)

    MF_kael_moonlit_wanderer = NPC(10, 3, "Kael the Moonlit wanderer", 2, "A mysterious figure cloaked in dark, tattered robes that seem to drink in the moonlight", "MF_kael_moonlit_wanderer.txt")
    MF_kael_moonlit_wanderer.add_item(Items.wooden_dart, 3)
    MF_kael_moonlit_wanderer.add_item(Items.bear_meat)
    MF_goblin_grunt = NPC(25, 4, "Goblin Grunt", 4, "a much bigger goblin than most goblins", "MF_goblin_grunt.txt")
    MF_goblin_grunt.add_item(Items.money, 7)
