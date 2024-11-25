
import random
from common_operations import BAR, print_with_readtime
import common_operations
import objects
from player import Player
from objects import *
from entity_list import *
import player




def start_combat(player, enemy, node):
    print(f"{BAR} \n Combat started!")
    return handle_command(player, enemy, node)

def handle_command(player, enemy, node):
    input_choices = ["THROW", "USE", "INVENTORY", "EQUIP", "ATTACK"]

    shortcut_input = {
        "INV": "INVENTORY",
        "T": "THROW",
        "EQ": "EQUIP",
        "U": "USE",
        "A": "ATTACK",
        "E": "EQUIP"
    }

    if player.equipped_weapon.name == "":
            player.equipped_weapon = Items.fists

    # EQUIP should be for armor and weapons
    # USE for hp items
    while True:
        winner = check_for_winner(player, enemy)
        if winner != -1:
            if winner == player:
                print_with_readtime(f"You have slain {enemy.name}!")
            if winner == enemy:
                print_with_readtime(f"You died to {enemy.name}!")
            return winner
        
        player.print_stats()
        print(f" {enemy.name} HP left: {enemy.hp}")

        print(f"{BAR} \n Enter a command! (Possible commands: THROW, USE, INVENTORY, EQUIP, ATTACK) \n {BAR}")
        i = input("> ").upper()

        for key, value in shortcut_input.items():
            if i == key:
                i = value
                break

        if i not in input_choices:
            continue

        if "THROW" in i:
            success = throw_item(player, enemy, node)
            if not success:
                damage_creature(player, enemy.attack_dmg, enemy)
        if "INVENTORY" in i:
            player.print_inventory()
        if "EQUIP" in i:
            player.equip_item()
        if "ATTACK" in i:
            attack_logic(player, enemy)
        if "USE" in i:
            player.use_item()

def check_for_winner(player, enemy):
    if player.hp > 0 and enemy.hp <= 0:
        return player
    elif player.hp <= 0 and enemy.hp > 0:
        return enemy
    
    return -1

def attack_logic(player, enemy):

    print_with_readtime(f"{BAR} \nYou attack with a {player.equipped_weapon.name}")

    enemy_alive = True
    player_alive = True
    # If player time to attack is smaller, deal damage to enemy first
    if enemy.speed >= player.equipped_weapon.attack_speed:
        print_with_readtime("You are quicker to strike!")        
        enemy_alive = damage_creature(enemy, player.equipped_weapon.damage)
        if enemy_alive:
            player_alive = damage_creature(player, enemy.attack_dmg, enemy)
    # If enemy is faster to attack, player takes damage first
    else:
        print_with_readtime(f"{enemy.name} is quicker to strike!")
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
        print_with_readtime(f"You deal {damage} damage to the {creature.name}!")

    if type(creature) == player.Player:
        damage = damage - round(creature.defense/2, 2)
        print_with_readtime(f"You take {damage} damage from {enemy.name}!")

    creature.hp -= damage

    if creature.hp <= 0:
        return False
    return True

def throw_item(player = Player(), enemy = NPC(), node = Node):
    items = player.get_items_of_type()
    selected_item = common_operations.select_item(items)

    # If player didn't choose an item to throw, go back into action selection
    if selected_item == -1:
        return True

    player.remove_item(selected_item)
    node.add_item(selected_item)

    if player.equipped_weapon == selected_item and player.equipped_weapon not in player.inventory[0]:
        player.equipped_weapon = Items.fists

    if selected_item not in player.inventory and selected_item in player.armor.values():
        player.unequip_armor(selected_item)

    hit_probability = get_hit_probability(selected_item) * 100
    value = random.randrange(0, 100)
 
    print_with_readtime(f"Throwing {selected_item.name} | Chance of hitting: {round(hit_probability, 2)} %")

    if value <= hit_probability:
        enemy.take_damage(selected_item.throw_dmg)
        print_with_readtime(f"Throw successful! {enemy.name} took {selected_item.throw_dmg} damage!")
        return True
    else:
        print_with_readtime(f"Throw failed!")
        return False
    
def get_hit_probability(item):
    # Probability decreases with heavier items
    hit_probability = 1/((float(item.weight) * 2) ** (1 / 3))
    if hit_probability > 1:
        hit_probability = 1.0
    return hit_probability
     
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
    