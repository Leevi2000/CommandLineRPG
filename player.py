
from entity_list import Items
from objects import Armor, Item, Weapon
import math

class Player:
    value_decrease_percent = 0.7
    def __init__(self, name=""):
        self.name = name
        self.inventory = [] # [item, quantity] pairs
        self.hp = 20
        self.defense = 0
        self.max_weight = 40
        self.equipped_weapon = Weapon()
        self.armor = {"head": Armor(), "chest": Armor(), "legs": Armor()}
    
    def add_item(self, item = Item(), quantity = 1):

        # If same item already in inventory, increase the quantity
        for x in range(len(self.inventory)):
            if self.inventory[x][0] == item:
                self.inventory[x][1] += quantity
                return
            
        # If there wasn't similar item yet, append item to the list with quantity=1
        self.inventory.append([item, quantity])

    def equip_armor(self, item):
        self.armor[item.armor_type] = item
        defense = 0
        for item in self.armor.values():
            defense += item.defense

        self.defense = defense

    def heal(self, amount):
        self.hp += amount
        if self.hp > 20:
            self.hp = 20
        
    def remove_item(self, item = Item(), quantity = 1):
        
        # If same item already in inventory, decrease the quantity
        for x in range(len(self.inventory)):
            if self.inventory[x][0] == item:
                self.inventory[x][1] -= quantity
                # It quantity goes zero, remove item from inventory
                if self.inventory[x][1] <= 0:
                    if item in self.armor.values():
                        self.unequip_armor(item)
                    self.inventory.pop(x)
                break
                

    def unequip_armor(self, item):
        if item in self.armor.values():
            # Find the key that maps to the given item (value)
            for key, value in self.armor.items():
                if value == item:
                    # Change the value of the found key to a new Armor() instance
                    self.armor[key] = Armor()
                    break

    # Calculates player wealth based on amount of silver coins in the inventory
    def calculate_wealth(self):

        wealth = 0

        for x in range(len(self.inventory)):
            if self.inventory[x][0] == Items.money:
                wealth = Items.money.value * self.inventory[x][1]

        return wealth
    
    def print_stats(self):
        print(f"---------------------- \n Your stats | HP: {self.hp} | DEF: {self.defense} | Weapon: {self.equipped_weapon.name}")



    def print_inventory(self):
        print("-----------------")

        if len(self.inventory) == 0:
            print("Inventory is empty")
        
        total_weight = 0.0
        for x in range(len(self.inventory)):
            item = self.inventory[x][0]
            quantity = self.inventory[x][1]
            total_weight += item.weight * quantity
            general_details = item.get_details()
            if general_details != "":
                general_details = " | " + general_details

            print(f"{str(quantity) + "x":<3} {item.name + " (s)":<20} | Total Weight: {str(round(item.weight * quantity, 2)) + " kg(s)":<12} {general_details:<15} {item.description}")

        print("-----------------")
        print(f"Carrying: {total_weight} kg(s) of {self.max_weight} kg(s) maximum")
        


        
        