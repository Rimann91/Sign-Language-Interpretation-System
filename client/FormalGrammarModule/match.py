import sys
from pattern.en import parse, pprint
from autocorrect import Speller
from pandas import DataFrame
import command_output_demo


class ParseCommand():
    def __init__(self):
        pass

    def get_action(self, command_df):
        dfAction = command_df.query("TAG=='VB' or TAG=='IN' or CHUNK=='I-VP'")[['WORD']]
        action = []

        for label, content in dfAction.WORD.items():
            action.append(content)

        action = ' '.join(action)
        return action

    def get_objects(self, command_df):
        """
        #TODO decide if we need to catch proper nouns
        """
        dfobject = command_df.query("TAG=='NN' or TAG=='NNS'  or CHUNK=='I-NP'")

        objects = []

        for label, content in dfobject.WORD.items():
            objects.append(content)

        objects = ' '.join(objects)
        return objects

    def parse_command(self, strInput):
        lsParsed = parse(strInput, relations=True, lemmeta=True).split()
        df = DataFrame(lsParsed[0], columns=["WORD", "TAG", "CHUNK", "ROLE", "PNP"])
        action = self.get_action(df)
        objects = self.get_objects(df)
        command = f"{action} {objects}"
        return command

    def remove_prepositions(self, command_str):
        superfluous = ['the', 'at', 'in', 'an', 'a']
        command_lst = command_str.split(' ')
        for word in command_lst:
            if word in superfluous:
                command_lst.remove(word)
        return ' '.join(command_lst)


    def get_command(self, strInput):

        #TODO convert numberical number representation to alphabetical number representation
            
        # Autocorrect Spelling    
        check = Speller(lang='en')
        corrected = check(strInput)

        # Parse the command into action-object structure
        command = self.parse_command(corrected)

        # remove unwanted prepositions
        command = self.remove_prepositions(command)
        return command



if len(sys.argv) > 1:
    parser = ParseCommand()
    if sys.argv[1] == "file":
        with open("test_inputs.txt", 'r') as f:
            test = f.readlines()
            for c in test:
                command = parser.get_command(c)
                print(f"{c} -> {command}")
                command_output_demo.toggle_lights(command)

    if sys.argv[1] == "key":
        while True:
            test = input("**> ")
            if test != 'q':
                command = parser.get_command(test)
                print(f"{test} -> {command}")
                command_output_demo.toggle_lights(command)
            else: break

    else: print("argument error: enter a valid argument for match.py")
else: print("Please provide arguments")
