from objects import Entity, Node
from entity_list import NPCs

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


    map_to_direction(starting_house, town_center_area, north)
    map_to_direction(starting_house, neighbours_house, east)
    map_to_direction(town_center_area, marketplace, north)
    map_to_direction(town_center_area, NPCs.drunken_guard_of_windermere, west)
    map_to_direction(marketplace, alley, west)
    map_to_direction(alley, NPCs.rogue, north)


    #alley.to_north = NPCs.rogue