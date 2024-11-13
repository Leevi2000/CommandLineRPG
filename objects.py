class Entity:
    entity_type = ""
    description = ""

class Node(Entity):
    def __init__(self, general_desc, detailed_desc = ""):
        self.description = general_desc
        self.to_south = Entity()
        self.to_west = Entity()
        self.to_north = Entity()
        self.to_east = Entity()
        self.entity_type = "Node"
        self.detailed_description = detailed_desc
        items = []

class NPC(Entity):
    def __init__(self, hp, attack_dmg, name, speed, appearance, dialog_path):
        self.hp = hp
        self.attack_dmg = attack_dmg
        self.name = name
        self.speed = speed
        self.appearance = appearance
        self.dialog_path = "Dialogs\\" + dialog_path
        self.entity_type = "NPC"
        self.description = appearance

class Item(Entity):
    def __init__(self, name, weight, throw_dmg, description):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.description = description
        self.entity_type = "Item"

class Weapon(Item):
    def __init__(self, damage, range, attack_speed):
        self.damage = damage
        self.range = range
        self.attack_speed = attack_speed
        self.entity_type = "Weapon"

class Armor(Item):
    def __init__(self, defense):
        self.defense = defense
        self.entity_type = "Armor"

class Healing(Item):
    def __init__(self, healing):
        self.healing = healing
        self.entity_type = "Healing"
        