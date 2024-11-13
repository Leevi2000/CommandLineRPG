from operator import truediv


class Dialog:
    def __init__(self, filepath, relatedItems):
        self.filepath = filepath
        self.relatedItems = relatedItems

class DialogReader:
    BAR = "---------------------"

    def read_dialog(self, npc_details):
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
                self.outcome_handler(_content[row_num].strip(), npc_details)
                return True

            row_num += 1

        return True

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
            
            try:
                value = int(answer)
            except ValueError:
                print("Bad input! Try again.")
                continue

            # If allowed input answer, find the row for right dialog action from options list.
            if value > 0 and value <= len(options):
                break
            else: 
                print("Bad input! Try again.")


        return int(self.find_next_row_with_txt(options[value-1][1], row, content))  

    def find_next_row_with_txt(self, txt, current_row, content):
        new_row = current_row + 1

        while new_row < len(content):
            row_txt = content[new_row].strip('\n')
            if txt not in row_txt:
                
                new_row += 1
            else:
                return int(new_row)
            
        return -1

    def outcome_handler(self, outcome, npc_details):
        print(str(outcome))
