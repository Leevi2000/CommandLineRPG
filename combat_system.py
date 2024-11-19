
import random
import objects
from player import Player
from objects import *
from entity_list import *
import player


BAR = "---------------------"

def start_combat(player, enemy, node):
    print(f"{BAR} \n Combat started!")
    return handle_command(player, enemy, node)

def handle_command(player, enemy, node):
    input_choices = ["THROW", "USE", "INVENTORY", "FLEE", "EQUIP", "ATTACK"]

    if player.equipped_weapon.name == "":
            player.equipped_weapon = Items.fists

    # EQUIP should be for armor and weapons
    # USE for hp items
    while True:

        winner = check_for_winner(player, enemy)
        if winner != -1:
            if winner == player:
                print(f"You have slain {enemy.name}!")
            if winner == enemy:
                print(f"You died to {enemy.name}!")
            return winner
        
        player.print_stats()
        print(f" {enemy.name} HP left: {enemy.hp}")

        print(f"{BAR} \n Enter a command! (Possible commands: THROW, USE, INVENTORY, FLEE, EQUIP, ATTACK) \n {BAR}")
        i = input("> ") 

        if i not in input_choices:
            continue

        if "THROW" in i:
            success = throw_item(player, enemy, node)
            if not success:
                damage_creature(player, enemy.attack_dmg)
        if "INVENTORY" in i:
            player.print_inventory()
        if "EQUIP" in i:
            equip_item(player)
        if "ATTACK" in i:
            attack_logic(player, enemy)

        if "USE" in i:
            use_item(player)

def check_for_winner(player, enemy):
    if player.hp > 0 and enemy.hp <= 0:
        return player
    elif player.hp <= 0 and enemy.hp > 0:
        return enemy
    
    return -1

def attack_logic(player, enemy):

    print(f"{BAR} \nYou attack with a {player.equipped_weapon.name}")

    enemy_alive = True
    player_alive = True
    # If player time to attack is smaller, deal damage to enemy first
    if enemy.speed >= player.equipped_weapon.attack_speed:
        print("You are quicker to strike!")        
        enemy_alive = damage_creature(enemy, player.equipped_weapon.damage)
        if enemy_alive:
            player_alive = damage_creature(player, enemy.attack_dmg, enemy)
    # If enemy is faster to attack, player takes damage first
    else:
        print(f"{enemy.name} is quicker to strike!")
        player_alive = damage_creature(player, enemy.attack_dmg, enemy)
        if player_alive:
            enemy_alive = damage_creature(enemy, player.equipped_weapon.damage)

    if not enemy_alive:
        return enemy
    if not player_alive:
        return player
    
    return -1

# Reduces hp from creature and returns False is creature dies
def damage_creature(creature, damage, enemy = objects.NPC()):

    if type(creature) == objects.NPC:
        print(f"You deal {damage} damage to the {creature.name}!")

    if type(creature) == player.Player:
        print(f"You take {damage} damage from {enemy.name}!")

    creature.hp -= damage

    if creature.hp <= 0:
        return False
    return True

def equip_item(player = Player()):
    items = get_items_of_type(player, ["Weapon", "Armor"])
    items.append([Items.fists, 1])
    items.sort(key=lambda item: item[0].entity_type)
    selected_item = select_item(items)

    # If player didn't choose an item to throw, go back into action selection
    if selected_item == -1:
        return
    
    if selected_item.entity_type == "Weapon":
        player.equipped_weapon = selected_item
        print(f"{BAR} \n Equipped {selected_item.name}, with ATK: {selected_item.damage}")
        return
    
    player.equip_armor(selected_item)
    print(f"{BAR} \n Equipped {selected_item.name}, with DEF: {selected_item.defense} \n Total DEF: {player.defense}")
    
def use_item(player = Player()):
    items = get_items_of_type(player, ["Healing"])
    selected_item = select_item(items)

    # If player didn't choose an item to throw, go back into action selection
    if selected_item == -1:
        return

    player.remove_item(selected_item)
    player.heal(selected_item.healing)

    print(f"Healed {selected_item.healing} points. Your hp is now {player.hp}")


def throw_item(player = Player(), enemy = NPC(), node = Node):
    items = get_items_of_type(player)
    selected_item = select_item(items)

    # If player didn't choose an item to throw, go back into action selection
    if selected_item == -1:
        return True

    player.remove_item(selected_item)
    node.add_item(selected_item)

    hit_probability = get_hit_probability(selected_item) * 100
    value = random.randrange(0, 100)
 
    print(f"Throwing {selected_item.name} | Chance of hitting: {round(hit_probability, 2)} %")

    if value <= hit_probability:
        enemy.take_damage(selected_item.throw_dmg)
        node.add_item(selected_item)
        print(f"Throw successful! {enemy.name} took {selected_item.throw_dmg} damage!")
        return True
    else:
        node.add_item(selected_item)
        print(f"Throw failed!")
        return False
    
def get_hit_probability(item):
    # Probability decreases with heavier items
    hit_probability = 1/((float(item.weight) * 2) ** (1 / 3))
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
        print("No items to choose from!")


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
            if item[0].entity_type in filterList:
                filtered_items.append(item)

    return filtered_items
    