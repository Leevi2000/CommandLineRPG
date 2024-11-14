from operator import truediv
import entity_list
from player import Player
from objects import *
from entity_list import *

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

        while row_num < len(_content):
            if "[TXT]" in _content[row_num]:
                print(self.BAR)
                row_num = self.print_text_block(row_num + 1, _content)
                print(self.BAR)

            if "[CHOICES]" in _content[row_num]:
                row_num = self.choose_dialog_option(row_num + 1, _content)
                
            if "[OUTCOME:" in _content[row_num]:
                return self.player, _content[row_num].strip(), 
                

            if "[SELL DIALOG]" in _content[row_num]:
                pass

            if "[BUY DIALOG]" in _content[row_num]:
                self.buy_dialog()

            row_num += 1

        return self.player, "NO OUTCOME"
    
    def sell_dialog(self):
        pass

    def buy_dialog(self):
        while True:
            items = self.npc.items
            
            print(self.BAR + "\n What do you wish to buy? \n" + self.BAR)

            for x in range(len(items)):
                if items[x][0] is not None  and hasattr(items[x][0], "value"):
                    print(str(x + 1) + ": BUY " + items[x][0].name + " for " + str(items[x][0].value))

            print(f"{len(items) + 1}: EXIT")
            
            command = input("> ")

            if self.is_int(command):
                    value = int(command)
            else: 
                continue

            # Check whether or not the given input was allowed
            if int(value) > 0 and int(value) <= len(items):
                item_cost = items[value-1][0].value
                player_wealth = self.player.calculate_wealth()

                # Remove money from player if enough money for chosen item
                if item_cost > player_wealth:
                    print("Not enough money")
                    continue
                else:
                    self.player.remove_item(Items.money, item_cost)
                    self.player.add_item(items[value-1])
                    print(f"Bought {items[value-1][0].name} for {items[value-1][0].value}")
                    self.npc.items.pop(value-1)

            elif int(value) == len(items) + 1:
                print("CLOSING BUY DIALOG")
                break

            #if self.player.inventory

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
            
            if self.is_int(answer):
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


    


