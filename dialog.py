from itertools import count
from operator import truediv
import entity_list
from player import Player
from objects import *
from entity_list import *
import math
class Dialog:
    def __init__(self, filepath, relatedItems):
        self.filepath = filepath
        self.relatedItems = relatedItems

class DialogReader:
    BAR = "---------------------"
    player = Player()
    npc = NPC()

    def read_dialog(self, npc_details, player):

        self.npc = npc_details
        self.player = player

        path = npc_details.dialog_path

        file = open(str(path), "r")
        _content = file.readlines()
        file.close()
        for x in range(len(_content)):
            _content[x] = _content[x].replace('{NPC}', str(npc_details.name))
            _content[x] = _content[x].lstrip()

        row_num = 0
        previous_choice_row = 0
        while row_num < len(_content):
            if "[TXT]" in _content[row_num]:
                print(self.BAR)
                row_num = self.print_text_block(row_num + 1, _content)
                print(self.BAR)

            if "[CHOICES]" in _content[row_num]:
                previous_choice_row = row_num - 1
                row_num = self.choose_dialog_option(row_num + 1, _content)
                
            if "[SELL DIALOG]" in _content[row_num]:
                self.sell_dialog()
                if "[OUTCOME:" in _content[row_num]:
                    return self.player, _content[row_num].strip()
                row_num = previous_choice_row

            if "[BUY DIALOG]" in _content[row_num]:
                self.buy_dialog()
                if "[OUTCOME:" in _content[row_num]:
                    return self.player, _content[row_num].strip()
                row_num = previous_choice_row

            if "[OUTCOME:" in _content[row_num]:
                return self.player, _content[row_num].strip()

            row_num += 1

        return self.player, "NO OUTCOME"
    
    def sell_dialog(self):
        # Percentage of the original value
        value_decrease_percent = 0.7

        while True:
            #items = self.player.inventory

            # Filter out money from items
            items = []
            for item in self.player.inventory:
                if item[0] != Items.money:
                    items.append(item)

            if len(items) == 0:
                print(f"{self.BAR} \n You have no items to sell! \n {self.BAR}")
                break


            print(self.BAR + "\n What do you wish to sell? \n" + self.BAR)
            print(f"You have {self.player.calculate_wealth()} {Items.money.name} (s) \n {self.BAR}")

            for x in range(len(items)):
                item = items[x][0]
                item_quantity = items[x][1]
                if items[x][0] is not None  and hasattr(item, "value"):
                    print(str(x + 1) + ": SELL " + item.name + " for " + str(math.floor(item.value * value_decrease_percent)) + " " + Items.money.name + "(s) | In inventory: " + str(item_quantity))
            
            print(f"{len(items) + 1}: EXIT \n {self.BAR}")

            args = self.get_shop_input()

            # Exit dialog
            if int(args[0]) == len(items) + 1:
                print(self.BAR)
                break

            item_id = int(args[0])
            quantity = int(args[1])

             # Check whether or not the given input was allowed
            if int(item_id) > 0 and int(item_id) <= len(items):
                if quantity > items[item_id-1][1]:
                    print("You can't sell more than you own!")
                    continue
                item = items[item_id-1][0]
                item_worth = math.floor(item.value * value_decrease_percent) * quantity
                print(f"{self.BAR} \n Sold {quantity} {item.name} (s) for {item_worth} {Items.money.name} (s)")
                self.player.remove_item(item, quantity)
                self.player.add_item(Items.money, item_worth)

    def buy_dialog(self):
        while True:
            items = self.npc.items

            if len(items) == 0:
                print(f"{self.BAR} \n No items to buy! \n {self.BAR}")
                break
            
            print(self.BAR + "\n What do you wish to buy? \n" + self.BAR)
            print(f"You have {self.player.calculate_wealth()} {Items.money.name} (s) \n {self.BAR}")

            # Print out buy options
            for x in range(len(items)):
                item = items[x][0]
                item_quantity = items[x][1]
                if item is not None  and hasattr(item, "value"):
                    print(str(x + 1) + ": BUY " + item.name + " for " + str(item.value) + " " + Items.money.name + "(s) | In stock: " + str(item_quantity))

            print(f"{len(items) + 1}: EXIT \n {self.BAR}")

            args = self.get_shop_input()

            # Exit dialog
            if int(args[0]) == len(items) + 1:
                print(self.BAR)
                break

            item_id = int(args[0])
            quantity = int(args[1])
            item = items[item_id-1][0]

            # Check whether or not the given input was allowed
            if int(item_id) > 0 and int(item_id) <= len(items):
                if quantity > items[item_id-1][1]:
                    print(f"{self.BAR} \n You can't buy more than there is stock!")
                    continue
                 
                item_cost = item.value * quantity
                player_wealth = self.player.calculate_wealth()

                # Remove money from player if enough money for chosen item
                if item_cost > player_wealth:
                    print("Not enough money")
                    continue
                else:
                    self.player.remove_item(Items.money, item_cost)
                    self.player.add_item(item, quantity)
                    print(f"{self.BAR} \n Bought {quantity} {item.name} (s) for {item.value*quantity} {Items.money.name} (s)")
                    self.npc.remove_item(item, quantity)

            #if self.player.inventory

    def get_shop_input(self):
        while True:
            command = input("> ")
            args = command.split()

            # If only one argument was given, set item quantity to one
            if len(args) == 1:
                args.append("1")

            args_are_numbers = True

            for arg in args:
                if not self.is_int(arg):
                    args_are_numbers = False

            # If there were wrong amount of arguments, restart the sell dialog
            if not args_are_numbers or len(args) != 2:
                print("Incorrect input. Correct way is -> [ACTION] [QUANTITY]")
                continue
            elif args[1] == 0:
                print("You cant buy zero of item!")
                continue
            else:
                break
        return args

    # Prints text block from the given row number to the text section end. Returns the end row number.
    def print_text_block(self, from_row, content):
        row = from_row
        
        while row < len(content):
            row_txt = content[row]
            if "[TXT END]" not in row_txt:
                print(content[row].strip())
                row += 1
            else:
                return int(row + 1)
        
        return row
   
    def choose_dialog_option(self, from_row, content):
        row = from_row

        # Dialog text and action will be mapped to this list in as "[text][action]"" lists
        options = []

        while row < len(content):
            row_txt = content[row].strip('\n')
            if "[CHOICES END]" not in row_txt:
                if "[" in row_txt:
                    option = row_txt.split("[")    
                    option[1] = "[" + str(option[1])
                    options.append(option)
                row += 1
            else:
                #ask for input and print options, if false input, row = from_row
                break

        for i in range(len(options)):
            print(str(i+1) + ": " + options[i][0])

        # Loop though until accepted input is given.
        while True:
            answer = input("> ")
            
            if not self.is_int(answer):
                continue

            value = int(answer)

            # If allowed input answer, find the row for right dialog action from options list.
            if value > 0 and value <= len(options):
                break
            else: 
                print("Bad input! Try again.")

        return int(self.find_next_row_with_txt(options[value-1][1], row, content))  
    
    def is_int(self, given_string):
        try:
            value = int(given_string)
        except ValueError:
            print("Bad input! Try again.")
            return False
        
        return True
                


    def find_next_row_with_txt(self, txt, current_row, content):
        new_row = current_row + 1

        while new_row < len(content):
            row_txt = content[new_row].strip('\n')
            if txt not in row_txt:
                
                new_row += 1
            else:
                return int(new_row)
            
        return -1


    


