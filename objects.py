from entity_list import *
import math

class Entity:
    entity_type = ""
    description = ""

class Item(Entity):
    def __init__(self, name = "", weight = 0.0, throw_dmg = 0, value = 0, description = ""):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.description = description
        self.entity_type = "Item"
        self.value = value

    def get_details(self):
        details = f""
        return details

class Node(Entity):
    def __init__(self, general_desc, detailed_desc = ""):
        self.description = general_desc
        self.to_south = Entity()
        self.to_west = Entity()
        self.to_north = Entity()
        self.to_east = Entity()
        self.entity_type = "Node"
        self.detailed_description = detailed_desc

        # Dropped items and perhaps other items also can be stored here
        self.items = []

    def remove_item(self, item = Item(), quantity = 1):
        # If same item already in inventory, decrease the quantity
        for x in range(len(self.items)):
            if self.items[x][0] == item:
                self.items[x][1] -= quantity
                # It quantity goes zero, remove item from inventory
                if self.items[x][1] <= 0:
                    self.items.pop(x)
            break

    def add_item(self, item = Item(), quantity = 1):

        # If same item already in inventory, increase the quantity
        for x in range(len(self.items)):
            if self.items[x][0] == item:
                self.items[x][1] += quantity
                return
            
        # If there wasn't similar item yet, append item to the list with quantity=1
        self.items.append([item, quantity])

class NPC(Entity):
    def __init__(self, hp = 1, attack_dmg = 1, name = "", speed = 1, general_description = "", dialog_path = "", excuse = ""):
        self.hp = hp
        self.attack_dmg = attack_dmg
        self.name = name
        self.speed = speed
        self.detailed_description = ""
        self.dialog_path = "Dialogs\\" + dialog_path
        self.entity_type = "NPC"
        self.description = general_description
        self.excuse = excuse
        self.items = []

    def take_damage(self, damage = 0):
        self.hp -= damage

    def remove_item(self, item = Item(), quantity = 1):
        # If same item already in inventory, decrease the quantity
        for x in range(len(self.items)):
            if self.items[x][0] == item:
                self.items[x][1] -= quantity
                # It quantity goes zero, remove item from inventory
                if self.items[x][1] <= 0:
                    self.items.pop(x)
                break

    def add_item(self, item = Item(), quantity = 1):

        # If same item already in inventory, increase the quantity
        for x in range(len(self.items)):
            if self.items[x][0] == item:
                self.items[x][1] += quantity
                return
            
        # If there wasn't similar item yet, append item to the list with quantity=1
        self.items.append([item, quantity])


class Weapon(Item):
    def __init__(self, name = "", weight = 0.0, throw_dmg = 0, value = 0, description = "", damage = 0.0, attack_speed = 0):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.value = value
        self.description = description
        self.damage = damage
        self.attack_speed = attack_speed
        self.entity_type = "Weapon"

    def get_details(self):
        details = f"Attack: {str(self.damage)}"
        return details


class Armor(Item):
    def __init__(self,name = "", weight = 0.0, throw_dmg = 0, value = 0, description = "", defense = 0):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.description = description
        self.value = value
        self.defense = defense
        self.entity_type = "Armor"

    def get_details(self):
        details = f"Defense: {str(self.defense)}"
        return details

class Healing(Item):
    def __init__(self, name = "", weight = 0.0, throw_dmg = 0, value = 0, description = "", healing = 0):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.description = description
        self.value = value
        self.healing = healing
        self.entity_type = "Healing"

    def get_details(self):
        details = f"Healing: {str(self.healing)}"
        return details
        