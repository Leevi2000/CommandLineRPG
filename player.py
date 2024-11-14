
from entity_list import Items
from objects import Item

class Player:
    def __init__(self, name=""):
        self.name = name
        self.inventory = [] # [item, quantity] pairs
        self.hp = 20
        self.defense = 1

    
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
                
    # Calculates player wealth based on amount of silver coins in the inventory
    def calculate_wealth(self):

        wealth = 0

        for x in range(len(self.inventory)):
            if self.inventory[x][0] == Items.money:
                wealth = Items.money.value * self.inventory[x][1]

        return wealth


        