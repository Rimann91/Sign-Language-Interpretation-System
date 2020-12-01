#from match import command
import requests

def control_lights(state):
    requests.post("https://maker.ifttt.com/trigger/"+state+"/with/key/lQAvLfKbKh9JHMq9zkdkQkcYoPLK9NY0LS8pqrgHEZz")


def toggle_lights(command):
    if command == "turn on light kitchen":
        control_lights("toggle_lights_kitchen")
        print("Sending toggle request on")
    if command == "turn off light kitchen":
        control_lights("toggle_lights_kitchen")
        print("Sending toggle request off")
    else:
        pass

# command = input("Enter command:")
# toggle_lights()