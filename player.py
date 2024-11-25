
from hmac import new
import common_operations
from entity_list import Items
from objects import Armor, Item, Weapon
import math

BAR = "-----------------"

class Player:
    value_decrease_percent = 0.7
    def __init__(self, name=""):
        self.name = name
        self.inventory = [] # [item, quantity] pairs
        self.hp = 20.0
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
        
    def weight_overload(self, weight = 0):
        new_weight = weight + self.get_items_weight()
        if new_weight > self.max_weight:
            return True
        else:
            return False
        
    def get_items_weight(self):
        total_weight = 0.0
        for x in range(len(self.inventory)):
            item = self.inventory[x][0]
            quantity = self.inventory[x][1]
            total_weight += item.weight * quantity
        return round(total_weight, 2)

    def get_items_of_type(self, filterList = [""]):
    
        all_items = self.inventory
    
        if filterList[0] == "":
            return all_items

        filtered_items = []

        for item in all_items:
                if item[0].entity_type in filterList:
                    filtered_items.append(item)

        return filtered_items
    
    
    def print_item_list(self, items):
        for x in range(len(items)):
            print(f"{x + 1}: {items[x][0].name}, {items[x][0].get_details()}")

        if len(items) == 0:
            print("No items to choose from!")
            return False

        print(f"{len(items) + 1}: Go back")
        return True

    def use_item(self):
        items = self.get_items_of_type(["Healing"])
        selected_item = common_operations.select_item(items)

        # If player didn't choose an item to throw, go back into action selection
        if selected_item == -1:
            return

        self.remove_item(selected_item)
        self.heal(selected_item.healing)

        print(f"Healed {selected_item.healing} points. Your hp is now {self.hp}")

    def equip_item(self):

        items = self.get_items_of_type(["Weapon", "Armor"])
        items.append([Items.fists, 1])
        items.sort(key=lambda item: item[0].entity_type)
        selected_item = common_operations.select_item(items)

        # If player didn't choose an item to throw, go back into action selection
        if selected_item == -1:
            return
        
        if selected_item.entity_type == "Weapon":
            self.equipped_weapon = selected_item
            print(f"{BAR} \n Equipped {selected_item.name}, with ATK: {selected_item.damage}")
            return
        
        self.equip_armor(selected_item)
        print(f"{BAR} \n Equipped {selected_item.name}, with DEF: {selected_item.defense} \n Total DEF: {self.defense}")
    
    def drop_items(self):
        items_to_drop = []
        while True:
            items = self.get_items_of_type()
            msg = self.get_carried_weight_string()
            selected_item = common_operations.select_item(items, msg)

            if selected_item == -1:
                    break
            
            self.remove_item(selected_item)
            items_to_drop.append(selected_item)
            print(f"Dropped {selected_item.name} on the ground")
        return items_to_drop
        
    def get_carried_weight_string(self):
        return f"Carrying: {self.get_items_weight()} kg(s) of {self.max_weight} kg(s) maximum"
        
        