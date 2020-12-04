import sys
from pattern.en import parse, pprint
from autocorrect import Speller
from pandas import DataFrame
import command_output_demo




# Function to tag specific verbs and action words and arrange them in a dataframe
def get_action(command_df):
    dfAction = command_df.query("TAG=='VB' or TAG=='IN' or CHUNK=='I-VP'")[['WORD']]
    action = []

    for label, content in dfAction.WORD.items():
        action.append(content)

    action = ' '.join(action)
    return action

# Function to tag specific nouns and descriptive nouns and arrange them in a dataframe
def get_objects(command_df):
    dfobject = command_df.query("TAG=='NN' or TAG=='NNS'  or CHUNK=='I-NP'")

    objects = []

    for label, content in dfobject.WORD.items():
        objects.append(content)

    objects = ' '.join(objects)
    return objects

def parse_command(strInput):
    lsParsed = parse(strInput, relations=True, lemmeta=True).split()
    if len(lsParsed) < 1:
        return strInput
    df = DataFrame(lsParsed[0], columns=["WORD", "TAG", "CHUNK", "ROLE", "PNP"])
    action = get_action(df)
    objects = get_objects(df)
    command = f"{action} {objects}"
    return command

# Function to remove any unwanted or unnecessary prepositions
def remove_prepositions(command_str):
    superfluous = ['the', 'at', 'in', 'an', 'a']
    command_lst = command_str.split(' ')
    for word in command_lst:
        if word in superfluous:
            command_lst.remove(word)
    return ' '.join(command_lst)


def get_command(strInput):

    strInput = strInput.lower()
        
    # Autocorrect Spelling    
    check = Speller(lang='en')
    corrected = check(strInput)

    # Parse the command into action-object structure
    command = parse_command(corrected)

    # remove unwanted prepositions
    command = remove_prepositions(command)
    return command

# Output the command given and perform the smart home command
def matchWord(word):
    command = get_command(word)
    command = command.replace(" ","")
    print("command: " + command)
    command_output_demo.toggle_lights(command)



# Below was used for further testing

# if len(sys.argv) > 1:
#     parser = ParseCommand()
#     if sys.argv[1] == "file":
#         with open("test_inputs.txt", 'r') as f:
#             test = f.readlines()
#             for c in test:
#                 command = parser.get_command(c)
#                 print(f"{c} -> {command}")
#                 command_output_demo.toggle_lights(command)

#     if sys.argv[1] == "key":
#         while True:
#             test = input("**> ")
#             if test != 'q':
#                 command = parser.get_command(test)
#                 print(f"{test} -> {command}")
#                 command_output_demo.toggle_lights(command)
#             else: break

#     else: print("argument error: enter a valid argument for match.py")
# else: print("Please provide arguments")