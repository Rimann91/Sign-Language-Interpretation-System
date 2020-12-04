import requests

# Interation between IFTTT and the software to trigger the smart home event
def control_lights(state):
    requests.get("https://maker.ifttt.com/trigger/"+state+"/with/key/lQAvLfKbKh9JHMq9zkdkQkcYoPLK9NY0LS8pqrgHEZz")


# Function to recognize command and perform specific smart home command
def toggle_lights(command):
    if command == "idea":
        control_lights("toggle_lights_kitchen")
        print("Sending toggle request on")
    if command == "block":
        control_lights("toggle_lights_kitchen")
        print("Sending toggle request off")
    else:
        pass


# Below used for testing

# command = input("Enter command:")
# toggle_lights()

