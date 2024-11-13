from objects import Entity, Node
from NPCList import NPCs

#
class Map:
    starting_house = Node("Home.")
    neighbours_house = Node("Neighbour's house.")
    town_center_area = Node("The central part of town")
    marketplace = Node("Marketplace")
    alley = Node("Shady alley")



    starting_house.to_east = neighbours_house
    starting_house.to_north = town_center_area

    town_center_area.to_north = marketplace
    town_center_area.to_south = starting_house

    marketplace.to_south = town_center_area
    marketplace.to_west = alley

    alley.to_east = marketplace
    alley.to_north = NPCs.rogue

    neighbours_house.to_west = starting_house



    #alley.to_north = NPCs.rogue