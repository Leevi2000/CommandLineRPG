import NPCList
from objects import Entity, Node
from NPCList import NPCs
from dialog import DialogReader
from map import Map

def main():
    directions = ["NORTH", "EAST", "SOUTH", "WEST"]
    reader = DialogReader()

    current_node = Map.starting_house

    while True:
        print_locations(current_node)
        command = ask_input()
        if command in directions:
            current_node = node_action(current_node, command)

    print("-----------------")
    print("You meet eyes with a shady character when traversing through an old alley...")
    
    reader.read_dialog(NPCs.rogue)    

def ask_input():
    allowed_input = ["NORTH", "EAST", "SOUTH", "WEST", "INSPECT", "TAKE"]

    while True:
        command = input("> ")
        if command not in allowed_input:
            continue
        else:
            break
        
    return command

def node_action(current_node, command):
    node = current_node
    entity_type = ""
    directions = {
        "NORTH": current_node.to_north,
        "EAST": current_node.to_east,
        "SOUTH": current_node.to_south,
        "WEST": current_node.to_west
    }

    # Get the type if the direction exists in the dictionary, otherwise set type to None or a default value

    if command in directions:
        entity_type = directions.get(command).entity_type # type: ignore

    if entity_type == "Node":
        node = directions.get(command)

    if entity_type == "NPC":
         reader = DialogReader()
         reader.read_dialog(directions.get(command))

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

if __name__ == '__main__':
    main()