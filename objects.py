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
    def __init__(self, hp = 1, attack_dmg = 1, name = "", speed = 1, appearance = "", dialog_path = "", excuse = ""):
        self.hp = hp
        self.attack_dmg = attack_dmg
        self.name = name
        self.speed = speed
        self.appearance = appearance
        self.dialog_path = "Dialogs\\" + dialog_path
        self.entity_type = "NPC"
        self.description = appearance
        self.excuse = excuse
        self.items = []

class Item(Entity):
    def __init__(self, name = "", weight = 0.0, throw_dmg = 0, value = 0, description = ""):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.description = description
        self.entity_type = "Item"
        self.value = value

class Weapon(Item):
    def __init__(self, name = "", weight = 0.0, throw_dmg = 0, value = 0, description = "", damage = 0.0, range = 0, attack_speed = 0):
        self.name = name
        self.weight = weight
        self.throw_dmg = throw_dmg
        self.value = value
        self.description = description
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
        