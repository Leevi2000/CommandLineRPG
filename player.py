
from entity_list import Items
from objects import Item
import math

class Player:
    def __init__(self, name=""):
        self.name = name
        self.inventory = [] # [item, quantity] pairs
        self.hp = 20
        self.defense = 1
        self.max_weight = 40
    
    def add_item(self, item = Item(), quantity = 1):

        # If same item already in inventory, increase the quantity
        for x in range(len(self.inventory)):
            if self.inventory[x][0] == item:
                self.inventory[x][1] += quantity
                return
            
        # If there wasn't similar item yet, append item to the list with quantity=1
        self.inventory.append([item, quantity])



    def remove_item(self, item = Item(), quantity = 1):
        
        # If same item already in inventory, decrease the quantity
        for x in range(len(self.inventory)):
            if self.inventory[x][0] == item:
                self.inventory[x][1] -= quantity
                # It quantity goes zero, remove item from inventory
                if self.inventory[x][1] <= 0:
                    self.inventory.pop(x)
            break
                
    # Calculates player wealth based on amount of silver coins in the inventory
    def calculate_wealth(self):

        wealth = 0

        for x in range(len(self.inventory)):
            if self.inventory[x][0] == Items.money:
                wealth = Items.money.value * self.inventory[x][1]

        return wealth

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

            #if item.description != "":
           #     print(f"{item.description:>60}")

        print("-----------------")
        print(f"Carrying: {total_weight} kg(s) of {self.max_weight} kg(s) maximum")
        


        
        