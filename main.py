import combat_system
import common_operations
import entity_list
import dialog
from objects import Entity, Node
from entity_list import Items, NPCs
from dialog import DialogReader
from map import Map
import re
from player import Player
import player

game_over = False

def main():
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    reader = DialogReader()

    player = Player("Player")
    player.add_item(Items.money, 40)
    player.add_item(Items.leather_tunic, 10)

    current_node = Map.alley

    print("-----------")
    cleaned_description = re.sub(r'\s+', ' ', current_node.detailed_description.strip())
    print(cleaned_description)

    while True:

        if game_over:
            break

        print_locations(current_node)
        command = ask_input()
        if command[0] in directions:
            current_node = node_action(current_node, command[0], player)
        if command[0] == "LOOK" and command[1] in directions:
            print_direction_detail(current_node, command[1])
        if command[0] == "INVENTORY":
            player.print_inventory()
        if command[0] == "STATS":
            player.print_stats()
        if command[0] == "EQUIP":
            player.equip_item()
        if command[0] == "USE":
            player.use_item()
        if command[0] == "TAKE":
            take_items_on_node(current_node, player)
        if command[0] == "INSPECT":
            print_amount_of_items(current_node)
            
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

def print_amount_of_items(node):
    print(f"There are {len(node.items)} items nearby")

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
    npc_on_node = False

    directions = {
        "NORTH": current_node.to_north,
        "EAST": current_node.to_east,
        "SOUTH": current_node.to_south,
        "WEST": current_node.to_west
    }

    # Get the type if the direction exists in the dictionary, otherwise set type to None or a default value
    entity = directions.get(command)
    npc = directions.get(command)
    if command in directions and entity is not None and hasattr(entity, "entity_type"):
        entity_type = entity.entity_type

    if entity_type == "Node" and entity is not None and hasattr(entity, "detailed_description"):
        node = entity
        print("-----------")
        cleaned_description = re.sub(r'\s+', ' ', entity.detailed_description.strip())
        print(cleaned_description)
        if entity.npc_on_enter.name != "":
            npc_on_node = True
            npc = entity.npc_on_enter.name

    if entity_type == "NPC" or npc_on_node:
        reader = DialogReader()
        outcome = reader.read_dialog(npc, player_detail)
        player_detail = outcome[0]
        outcome_handler(outcome[1], npc, node, player_detail, command)
        
    # Return node + player
    return node

def take_items_on_node(node, player):
    while True:
        item = common_operations.select_item(node.items)

        if item == -1:
            return
        
        node.remove_item(item)
        player.add_item(item)

    
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


def outcome_handler(outcome, npc_details, node, player_detail = Player(), direction = ""):
    global game_over

    direction_map = {
            "NORTH": "to_north",
            "EAST": "to_east",
            "SOUTH": "to_south",
            "WEST": "to_west"
    }

    if "ATTACK" in outcome:
        winner = combat_system.start_combat(player_detail, npc_details, node)
        if winner == npc_details:
            game_over = True
            print_game_over(npc_details)
            return
        else:
            return


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

    
def print_game_over(enemy):
    print(f"{combat_system.BAR}\nGame Over\n{combat_system.BAR}")
    

if __name__ == '__main__':
    main()