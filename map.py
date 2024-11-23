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
    

    # --------------------------------
    # Forest of Windermere Nodes
    # --------------------------------

    FOW_junction_north = Node("Diverging roads",
                              """You find yourself at a quiet forest road intersection, the soft rustle of leaves filling the air.
                              To the north you can see a outlines of a few houses. Southern road delves deeper into the forest while to the west you can see a small path leading to bilberry bushes""")

    FOW_bilberry_area = Node("Bilberry bushes",
                             "Your gaze meets the bilberry bushes")
    FOW_bilberry_area.add_item(Items.bilberry, 7)