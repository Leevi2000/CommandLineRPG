from urllib import request
from common_operations import BAR, print_with_readtime
import entity_list
from player import Player
from objects import *
from entity_list import *
import math
import player

class Dialog:
    def __init__(self, filepath, relatedItems):
        self.filepath = filepath
        self.relatedItems = relatedItems

class DialogReader:
    player = Player()
    npc = NPC()

    def read_dialog(self, npc_details, player):

        self.npc = npc_details
        self.player = player

        path = npc_details.dialog_path

        file = open(str(path), "r", encoding="utf8")
        _content = file.readlines()
        file.close()
        for x in range(len(_content)):
            _content[x] = _content[x].replace('{NPC}', str(npc_details.name))
            _content[x] = _content[x].lstrip()

        row_num = 0
        previous_choice_row = 0
        while row_num < len(_content):
            if "[TXT]" in _content[row_num]:
                print(BAR)
                row_num = self.print_text_block(row_num + 1, _content)
                print(BAR)

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

            if "[REWARDS]" in _content[row_num]:
                self.reward_dialog()
                if "[OUTCOME:" in _content[row_num]:
                    return self.player, _content[row_num].strip()
                row_num = previous_choice_row

            if "[CONTINUE]" in _content[row_num]:
                row_num = previous_choice_row

            if "[OUTCOME:" in _content[row_num]:
                return self.player, _content[row_num].strip()

            row_num += 1

        return self.player, "NO OUTCOME"

    def reward_dialog(self):
        while True:
            rewards = self.npc.rewards
            print(f"{BAR} \n What do you want to exchange? \n {BAR}")
            i = 1
            for reward in rewards:
                needed_item = reward[0][0]
                needed_item_qty = reward[0][1]
                reward_item = reward[1][0]
                reward_item_qty = reward[1][1]

                print(f"{i}: You'll get {reward_item_qty}x {reward_item.name}(s) for {needed_item_qty}x {needed_item.name}(s)")
                i += 1

            print(f"{i}: Exit")

            reward_index = input(f"{BAR} \n> ")

            try:
                reward_index = int(reward_index) - 1
            except ValueError:
                continue

            if reward_index == len(rewards):
                break

            if reward_index >= 0 and reward_index < len(rewards):
                needed_item = rewards[reward_index][0][0]
                needed_item_qty = rewards[reward_index][0][1]
                reward_item = rewards[reward_index][1][0]
                reward_item_qty = rewards[reward_index][1][1]

                if self.player.remove_item(needed_item, needed_item_qty):
                    self.player.add_item(reward_item, reward_item_qty)
                    rewards.pop(reward_index)
                    print_with_readtime(f"You got {reward_item_qty}x {reward_item}")
                else:
                    print_with_readtime("You don't have the item(s)")

    def sell_dialog(self):
        while True:
            # Filter out money from items
            items = []
            for item in self.player.inventory:
                if item[0] != Items.money:
                    items.append(item)

            if len(items) == 0:
                msg = f"{BAR} \n You have no items to sell! \n {BAR}"
                print_with_readtime(msg)
                break

            print(BAR + "\n What do you wish to sell? \n" + BAR)
            print(f"You have {self.player.calculate_wealth()} {Items.money.name} (s) \n {BAR}")

            self.print_out_trade_options(items, True)

            print(f"{len(items) + 1}: EXIT \n {BAR}")

            args = self.get_shop_input()

            if self.exit_trade_input(args, items):
                break

            item_id, quantity, item = self.return_trade_arguments(args, items)
            if item_id == -1:
                continue

            msg = "You can't sell more than you own!"
            if self.validate_trade_input(items, item_id, quantity, msg):
                self.sell_procedure(item, quantity)

    def buy_dialog(self):
        while True:
            items = self.npc.items

            if len(items) == 0:
                print(f"{BAR} \n No items to buy! \n {BAR}")
                break
            
            print(BAR + "\n What do you wish to buy? \n" + BAR)
            print(f"You have {self.player.calculate_wealth()} {Items.money.name} (s) \n {BAR}")

            self.print_out_trade_options(items)

            print(f"{len(items) + 1}: EXIT \n {BAR}")

            args = self.get_shop_input()

            if self.exit_trade_input(args, items):
                break

            item_id, quantity, item = self.return_trade_arguments(args, items)
            if item_id == -1:
                continue
            msg = f"{BAR} \n You can't buy more than there is stock!"
            if self.validate_trade_input(items, item_id, quantity, msg):
                if not self.buy_procedure(item, quantity):
                    continue

    def exit_trade_input(self, args, items):
        # Exit dialog
        if int(args[0]) == len(items) + 1:
                print(BAR)
                return True
        return False

    def return_trade_arguments(self, args, items):
        try:
            item_id = int(args[0])
            quantity = int(args[1])
            item = items[item_id-1][0]
            return item_id, quantity, item
        except IndexError:
            print("You must choose a number in the given list")
            return -1, -1, -1

    def validate_trade_input(self, items, item_id, quantity, error_msg):
        # Check whether or not the given input was allowed
        if int(item_id) > 0 and int(item_id) <= len(items):
            if quantity > items[item_id-1][1]:
                print_with_readtime(error_msg)
                return False
        return True

    def sell_procedure(self, item, quantity):
            item_worth = math.floor(item.value * self.player.value_decrease_percent) * quantity
            print(f"{BAR} \n Sold {quantity} {item.name} (s) for {item_worth} {Items.money.name} (s)")
            self.player.remove_item(item, quantity)
            self.player.add_item(Items.money, item_worth)
        
    # Returns true if bought succesfully and player has enough money
    def buy_procedure(self, item, quantity):

        item_cost = item.value * quantity
        player_wealth = self.player.calculate_wealth()

        # Remove money from player if enough money for chosen item
        if item_cost > player_wealth:
            print_with_readtime("Not enough money")
            return False
        elif self.player.weight_overload(item.weight * quantity):
            print_with_readtime("You can't carry that much!")
            return False
        else:
            self.player.remove_item(Items.money, item_cost)
            self.player.add_item(item, quantity)
            print(f"{BAR} \n Bought {quantity} {item.name} (s) for {item.value*quantity} {Items.money.name} (s)")
            self.npc.remove_item(item, quantity)
            return True

    def print_out_trade_options(self, items, player_is_selling = False):
        # Print out buy options
            weight_info = self.player.get_carried_weight_string()
            print(f"{weight_info} \n {BAR}")
            for x in range(len(items)):
                item = items[x][0]
                item_quantity = items[x][1]
                if item is not None  and hasattr(item, "value"):
                    npc_to_player_str = str(x + 1) + ": BUY " + item.name + " for " + str(item.value) + " " + Items.money.name + "(s) | In stock: " + str(item_quantity) +  " | Weight: " + str(item.weight) + " kg(s)"
                    player_to_npc_str = str(x + 1) + ": SELL " + item.name + " for " + str(math.floor(item.value * self.player.value_decrease_percent)) + " " + Items.money.name + "(s) | In inventory: " + str(item_quantity) +  " | Weight: " + str(item.weight) + " kg(s)"
                    if(player_is_selling):
                        print(player_to_npc_str)
                    else:
                        print(npc_to_player_str)

                 
    def get_shop_input(self):
        while True:
            command = input("> ")
            args = command.split()
    
            if len(args) == 0:
                args.append("0")

            # If only one argument was given, set item quantity to one
            if len(args) == 1:
                args.append("1")

            if args[0] == "INVENTORY":
                self.player.print_inventory()
                input("> Press enter to continue")
                return -1, -1, -1

            args_are_numbers = True

            for arg in args:
                if not self.is_int(arg):
                    args_are_numbers = False

            # If there were wrong amount of arguments, restart the sell dialog
            if not args_are_numbers or len(args) != 2:
                print_with_readtime("Incorrect input. Correct way is -> [ACTION] [QUANTITY]")
                continue
            elif args[1] == 0:
                print_with_readtime("You cant buy zero of item!")
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
                print_with_readtime(content[row].strip())
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
                print_with_readtime("Bad input! Try again.")

        return int(self.find_next_row_with_txt(options[value-1][1], row, content))  
    
    def is_int(self, given_string):
        try:
            value = int(given_string)
        except ValueError:
            print_with_readtime("Bad input! Try again.")
            return False
        
        return True
                
    def find_next_row_with_txt(self, txt, current_row, content):
        new_row = current_row + 1

        while new_row < len(content):
            row_txt = content[new_row].strip('\n')
            if txt != row_txt:
                new_row += 1
            else:
                return int(new_row)
            
        return -1


    


