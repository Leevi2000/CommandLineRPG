from time import sleep


BAR = "-----------------"

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
    timer = (len(msg)/1200)*60
    print(msg)
    sleep(timer)