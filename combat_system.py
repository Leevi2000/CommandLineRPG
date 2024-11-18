from ast import While
import random
from player import Player
from objects import *
from entity_list import *


BAR = "---------------------"

def start_combat(player, enemy, node):
    print(f"{BAR} \n Combat started!")
    handle_command(player, enemy, node)

def handle_command(player, enemy, node):
    input_choices = ["THROW", "USE", "INVENTORY", "FLEE", "EQUIP", "ATTACK"]
    # EQUIP should be for armor and weapons
    # USE for hp items

    while True:
        print(f"{BAR} \n Enter a command! (Possible commands: THROW, USE, INVENTORY, FLEE, EQUIP, ATTACK) \n {BAR}")
        i = input("> ") 

        if i not in input_choices:
            continue
        if "THROW" in i:
            throw_item(player, enemy, node)
        if "INVENTORY" in i:
            player.print_inventory()

def throw_item(player = Player(), enemy = NPC(), node = Node):
    items = get_items_of_type(player)
    selected_item = select_item(items)

    #if isinstance(selected_item, list):
    #    raise ValueError("Selected item should not be a list")
    
    # If player didn't choose an item to throw, go back into action selection
    if selected_item == -1:
        return

    player.remove_item(selected_item)
    node.add_item(selected_item)

    hit_probability = get_hit_probability(selected_item) * 100
    value = random.randrange(0, 100)
 
    print(f"Throwing {selected_item.name} | Chance of hitting: {round(hit_probability, 2)} %")

    if value <= hit_probability:
        enemy.take_damage(selected_item.throw_dmg)
        node.add_item(selected_item)
        print(f"Throw successful! {enemy.name} took {selected_item.throw_dmg} damage!")
    else:
        node.add_item(selected_item)
        print(f"Throw failed!")
        pass
    
def get_hit_probability(item):
    # Probability decreases with heavier items
    hit_probability = 1/(math.sqrt(float(item.weight) * 2))
    if hit_probability > 1:
        hit_probability = 1.0
    return hit_probability
     
def select_item(items):
    while True:
        print_item_list(items)
        i = input(f"{BAR} \n Select item > ")

        try:
            int(i)
        except:
            continue

        if int(i) == len(items) + 1:
            return -1

        if int(i) > len(items) or int(i) < 1:
            continue

        item = items[int(i) - 1][0]
        return item
#if items == hasattr(items, )
def print_item_list(items):
    for x in range(len(items)):
        print(f"{x + 1}: {items[x][0].name}, {items[x][0].get_details()}")

    if len(items) == 0:
        print("No items to throw!")


    print(f"{len(items) + 1}: Go back to action selection")

def print_stats(player):
    #Print HP, equipped weapon + its damage and speed, defense points
    print(f"{BAR} \n HP: {player.hp} | DEF: {player.defense} | Equipped weapon: {player.equipped_weapon.name}, DMG: {player.equipped_weapon.damage}, DMG: {player.equipped_weapon.attack_speed} \n {BAR}")

def get_items_of_type(player, filterList = [""]):
    
    all_items = player.inventory
   
    if filterList[0] == "":
        return all_items

    filtered_items = []

    for item in all_items:
            if item.type in filterList:
                filtered_items.append(item)

    return filtered_items
    