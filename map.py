from tkinter import N
from objects import Entity, Item, Node
from entity_list import NPCs, Items

def map_to_direction(node, target_entity, direction):
        
        direction_map = {
            "NORTH": "to_north",
            "EAST": "to_east",
            "SOUTH": "to_south",
            "WEST": "to_west"
        }

        opposite_direction = {
            "NORTH": "SOUTH",
            "EAST": "WEST",
            "SOUTH": "NORTH",
            "WEST": "EAST"
        }

        if direction in direction_map:
            setattr(node, direction_map[direction], target_entity)

        if target_entity.entity_type == "Node":
            setattr(target_entity, direction_map[opposite_direction[direction]], node)

#
class Map:
    # Direction variables
    north = "NORTH"
    east = "EAST"
    south = "SOUTH"
    west = "WEST"


    # --------------------------------
    # Town of Windermere Nodes
    # --------------------------------
    starting_house = Node("Home", 
                          "Home sweet home! I'll hope to settle there again someday!")
    
    neighbours_house = Node("Neighbour's house.", 
                            """You walk past neighbour's clean yard.
                             How do they manage to keep it like that!""")
    
    town_center_area = Node("The central part of town", 
                            "The drunken guards' chatter drifts over as they watch the town hall.")
    
    marketplace = Node("Marketplace", 
                       "The marketplace is unusually quiet today...")
    
    alley = Node("Shady alley",
                 "A lot goes unnoticed here.")
    
    windermere_southern_exit = Node("Southern exit", 
                                    "A well-worn path winds its way toward the shadowed expanse of the Windermere Forest, its air heavy with whispers of untold mysteries.")


    map_to_direction(starting_house, town_center_area, north)
    map_to_direction(starting_house, neighbours_house, east)
    map_to_direction(town_center_area, marketplace, north)
    map_to_direction(town_center_area, NPCs.drunken_guard_of_windermere, west)
    map_to_direction(marketplace, alley, west)
    map_to_direction(alley, NPCs.rogue, north)
    map_to_direction(marketplace, NPCs.trader_of_windermere, east)
    map_to_direction(neighbours_house, windermere_southern_exit, south)
    

    # --------------------------------
    # Forest of Windermere Nodes
    # --------------------------------

    FOW_junction_north = Node("Diverging roads",
                              """You find yourself at a quiet forest road intersection, the soft rustle of leaves filling the air.
                              To the north you can see a outlines of a few houses. Southern road delves deeper into the forest while to the west you can see a small path leading to bilberry bushes""")

    FOW_bilberry_area = Node("Bilberry bushes",
                             "Your gaze meets the bilberry bushes")
    FOW_bilberry_area.add_item(Items.bilberry, 7)

    FOW_middle_section = Node("Glade",
                              """You walk upon a small glade. The sun slices through the leaves and lights up the otherwise dark area. The road continues to the NORTH and EAST.
                              """)
    
    FOW_Ambush = Node("Eastern diverging roads",
                      "You hear the leaves rattle as you approach the intersection")
    FOW_Ambush.npc_on_enter = NPCs.FOW_small_goblin_army
    
    map_to_direction(FOW_junction_north, windermere_southern_exit, north)
    map_to_direction(FOW_junction_north, FOW_bilberry_area, west)
    map_to_direction(FOW_junction_north, FOW_middle_section, south)
    map_to_direction(FOW_middle_section, NPCs.bear, west)
    map_to_direction(FOW_middle_section, NPCs.FOW_mysterious_man, south)
    map_to_direction(FOW_middle_section, FOW_Ambush, east)

    # --------------------------------
    # Evermist Glade
    # --------------------------------
    
    EG_north = Node("Northern entrance to the Evermist Glade", "A magical clearing shrouded in perpetual mist.")

    EG_northern_junction = Node("Junction with blue fireflies", "Faint, ethereal song carries over the mist.")

    EG_the_shimmering_arch = Node("Natural stone arch covered in glowing moss", "There seems to be an ancient portal-like structure.")

    EG_southern_junction = Node("ancient oak roots diverging into two directions", "The air is thick with glowing spores, and faint whispers seem to echo from all directions, making it a place of both decision and unease.")

    EG_crystal_pool = Node("Crystal pool", "Still, circular pool of water that reflects the surroundings like a perfect mirror.")

    EG_south = Node("Southern entrance to the Evermist Glade", "The mist is thin here. A giant tree can be seen east of the Evermist Glade")

    # Path to the tree
    EG_east_path = Node("ancient roots fusing into a clear path", "The mist here is dense, almost forming a layer on my skin")

    EG_entrance_tree = Node("Outline of an ancient tree of Mistspire", "The tree is massive, ancient tree with a silvery trunk and sprawling branches that seem to support the mist itself. Far away your eyes detect some movement")

    EG_the_mistspire_tree = Node("The Mistspire Tree", "Its hollow base houses a small sanctuary with carvings of forgotten gods and a faintly glowing orb, believed to be the source of the glade’s perpetual mist.")
    EG_the_mistspire_tree.npc_on_enter = NPCs.EG_mistwarden

    map_to_direction(EG_north, FOW_Ambush, north)
    map_to_direction(EG_north, EG_northern_junction, south)
    map_to_direction(EG_northern_junction, EG_the_shimmering_arch, south)
    map_to_direction(EG_the_shimmering_arch, EG_southern_junction, south)
    map_to_direction(EG_the_shimmering_arch, NPCs.EG_lost_seeker, west)
    map_to_direction(EG_southern_junction, EG_crystal_pool, west)
    map_to_direction(EG_crystal_pool, NPCs.EG_elderglow_nymph, north)
    map_to_direction(EG_southern_junction, EG_south, south)

    map_to_direction(EG_northern_junction, EG_east_path, east)
    map_to_direction(EG_east_path, EG_entrance_tree, south)
    map_to_direction(EG_entrance_tree, EG_the_mistspire_tree, south)
    EG_the_mistspire_tree.npc_on_enter = NPCs.EG_mistwarden
    
    # --------------------------------
    # Moonlit Fen
    # --------------------------------

    MF_shimmering_thicket = Node("Shimmering Thicket", "The thicket is a maze of glowing vines, ferns, and flowers that shift subtly, making it easy to lose one’s way.")

    MF_silver_mire = Node("Silver Mire", "A treacherous marsh where pools of water glimmer like liquid mercury under the moonlight. Mist drifts low to the ground, obscuring uneven terrain and dangerous sinkholes.")

    MF_pathway = Node("Vine-formed path", "Intertwining vines arch gracefully overhead, creating a tunnel-like passage.")

    MF_celestial_basin = Node("The Celestial Basin", "A massive, moonlit pool at the heart of the Fen, its water so still it perfectly reflects the sky above.")

    MF_greyhold_passage = Node("Faint imagery of a giant castle not so far away")
    
    MF_ruins_enter = Node("Ruin Entrance", "Ruin pathway that seems to lead further downward")

    MF_lunar_obelisk = Node("Lunar Obelisk", "A towering stone pillar carved with ancient runes, located in a moonlit clearing.")

    MF_glowspire_canopy = Node("Glowspire Canopy", "A dense cluster of towering ferns that rise high above the fen, their fronds tipped with bioluminescent light.")