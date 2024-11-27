from time import sleep


BAR = "-----------------"

actions = ["INSPECT", "TAKE", "LOOK", "INVENTORY", "DROP", "EQUIP", "DIALOG"]
directions = ["NORTH", "EAST", "SOUTH", "WEST", "NONE"]

dialog_speed_options = {1: 60, 2: 40, 3: 20, 4: 1}
dialog_speed = 2

main_shortcut_input = {
    "N": "NORTH",
    "E": "EAST",
    "S": "SOUTH",
    "W": "WEST",
    "T": "TAKE",
    "INV": "INVENTORY",
    "INS": "INSPECT",
    "L": "LOOK",
    "D": "DROP",
    "EQ": "EQUIP",
    "U": "USE",
    "DLG": "DIALOG"
}

help_msg = """Shop:
When choosing items to sell or buy, you can add an number after your selection to
buy or sell multiple items. For example: 2 3 will set the buy/sell amount to three of option 2.

Battle mechanism:
Throwing items can be strategic. Success rate depends on item weight and when throw is succesful,
the enemy will be 'knocked' and you can make a new attack. Thus avoiding taking any damage.
Thrown items are discarded from the inventory, and can be picked up later.
The throwing damage differs from weapon damage, so you won't know the damage a item will make until you throw succesfully.
Fleeing probability depends on your hp and defense and enemy's attack damage. The more damage enemy does, less likely you are to get away."""

def print_item_list(items):
        for x in range(len(items)):
            print(f"{x + 1}: {items[x][0].name} [{items[x][1]}], {items[x][0].get_details()}")

        if len(items) == 0:
            print("No items to choose from!")
            return False

        print(f"{len(items) + 1}: Go back")
        return True

def select_item(items, msg = ""):
        print(msg)
        while True:
            items_not_empty = print_item_list(items)

            if not items_not_empty:
                return -1

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
        
def print_with_readtime(msg):
    global dialog_speed
    timer = (len(msg)/1200)*dialog_speed_options[dialog_speed]
    print(msg)
    sleep(timer)

def select_speed_option():
    global dialog_speed
    print("Dialog speed selector:")
    while True:
        key = input("Speed options: 1, 2, 3, 4. Two by default. One is slowest \n >")
        try:
            key = int(key)
        except:
            continue

        if key > 0 and key <= 4:
            dialog_speed = key
            print_with_readtime(f"Changed dialog speed to {key}")
            return key


    