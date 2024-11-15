from operator import le
from turtle import clear
from typing import Self
import entity_list
import dialog
from objects import Entity, Node
from entity_list import Items, NPCs
from dialog import DialogReader
from map import Map
import re
from player import Player

def main():
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    reader = DialogReader()

    player = Player("Player")
    player.add_item(Items.money, 40)

    current_node = Map.starting_house

    print("-----------")
    cleaned_description = re.sub(r'\s+', ' ', current_node.detailed_description.strip())
    print(cleaned_description)

    while True:
        print_locations(current_node)
        command = ask_input()
        if command[0] in directions:
            current_node = node_action(current_node, command[0], player)
        if command[0] == "LOOK" and command[1] in directions:
            print_direction_detail(current_node, command[1])
        if command[0] == "INVENTORY":
            player.print_inventory()
            
def print_direction_detail(node, direction):
    directions = {
        "NORTH": node.to_north,
        "EAST": node.to_east,
        "SOUTH": node.to_south,
        "WEST": node.to_west
    }

    # Get the type if the direction exists in the dictionary, otherwise set type to None or a default value
    entity = directions.get(direction)
    if direction in directions and entity is not None and hasattr(entity, "entity_type"):
        entity_type = entity.entity_type

    if entity_type == "NPC" and entity is not None and hasattr(entity, "detailed_description"):
        print(f"----------------- \n {entity.detailed_description}")



def ask_input():
    allowed_input = ["NORTH", "EAST", "SOUTH", "WEST", "INSPECT", "TAKE", "LOOK", "INVENTORY"]
    directions = ["NORTH", "EAST", "SOUTH", "WEST", "NONE"]

    while True:
        command = input("> ").split()
        if len(command) == 1:
            command.append("NONE")
        if len(command) != 2:
            continue

        if command[0] not in allowed_input and command[1] not in directions:
            continue
        else:
            break
        
    return command

def node_action(current_node, command, player_detail):
    node = current_node
    entity_type = ""
    directions = {
        "NORTH": current_node.to_north,
        "EAST": current_node.to_east,
        "SOUTH": current_node.to_south,
        "WEST": current_node.to_west
    }

    # Get the type if the direction exists in the dictionary, otherwise set type to None or a default value
    entity = directions.get(command)
    if command in directions and entity is not None and hasattr(entity, "entity_type"):
        entity_type = entity.entity_type

    if entity_type == "Node" and entity is not None and hasattr(entity, "detailed_description"):
        node = entity
        print("-----------")
        cleaned_description = re.sub(r'\s+', ' ', entity.detailed_description.strip())
        print(cleaned_description)

    if entity_type == "NPC":
        reader = DialogReader()
        outcome = reader.read_dialog(entity, player_detail)
        player_detail = outcome[0]

        outcome_handler(outcome[1], entity, node, command, player_detail)
        
    # Return node + player
    return node
    
def print_locations(current_node):

    directions = {
        "NORTH": current_node.to_north,
        "EAST": current_node.to_east,
        "SOUTH": current_node.to_south,
        "WEST": current_node.to_west
    }
    print("-----------")
    for x in directions:
        entity_type = directions.get(x).entity_type # type: ignore
        if entity_type != "":
            print(f"To the {x} you can see {directions.get(x).description}") # type: ignore

def outcome_handler(outcome, npc_details, node, direction, player_detail = Player()):

    direction_map = {
            "NORTH": "to_north",
            "EAST": "to_east",
            "SOUTH": "to_south",
            "WEST": "to_west"
    }

    print(str(outcome))

    if "ATTACK" in outcome:
        # Attack logic
        pass

    if "TRADE" in outcome:
        # Trade logic
        pass

    if "LEAVE" in outcome:
        # Exit
        pass
    
    if "GIVE" in outcome:
        for x in npc_details.items:
            player_detail.add_item(x[0], x[1])
            print(f"You got {x[1]} {x[0].name} (s)")
        
        npc_details.items.clear()

    if npc_details is not None and hasattr(npc_details, "excuse"):
        # If npc has excuse (excuse -> to leave from map), remove mapping
        if npc_details.excuse != "":
            print(npc_details.name + ": " + npc_details.excuse)
            setattr(node, direction_map[direction], Entity())


    



if __name__ == '__main__':
    main()