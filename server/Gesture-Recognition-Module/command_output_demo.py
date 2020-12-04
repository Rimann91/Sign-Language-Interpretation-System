#    Copyright 2020 Braden Bagby, Robert Stonner, Riley Hughes, David Gray, Zachary Langford

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# Created by Zach Langford and Riley Hughes

"""
Functional Requirement 11
Non Functional requirement 5
"""
import requests

# Interaction between IFTTT and the software to trigger the smart home event
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

