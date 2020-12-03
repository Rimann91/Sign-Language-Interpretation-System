# Sign Language Interpretation System

## Introduction
This Sign Language Interpretation System is a class project for CSC 450 under Dr. Razib Iqbal at Missouri State University.

The sign language interpretation system will take a video stream input from an integrated camera and interpret hand gestures into pre-defined commands. It will recognize the gestures with high accuracy in real time. The system will be tested with a smart home interface connected to the program output, which would be a valid command that is interpreted from the sign language input.  The system will act as a means of processing hand sign communication for the potential use by individuals with hearing impairments or other disabilities that require visual communication devices for interacting with technology. The actualization of this product will provide a way for more people to intuitively access technology that was previously diffcult, or impossible, to use. The primary goal of the sign language interpretation system is to bridge those gaps.


## Server Installation Instructions:

1. Install dependencies
see: https://google.github.io/mediapipe/getting_started/install.html

MAKE SURE YOU INSTALL CORRECT VERSIONS FOR MEDIAPIE TO WORK

Python3 REQUIRED < 3.7. recommend 3.6.9 <br />
Bazel REQUIRED: 3.4.1 <br />
OpenCV <br />
FFmpeg <br />

*Note: all steps should be executed from the server directory of SLIS*

2. run install under server folder <br>
`$chmod +x ./install.sh` <br>
`$install.sh` <br> <br>

3. Run Server: <br>
`$run.sh` <br>



## Client Installation Instructions:

The current client has only been tested on Windows 10. Currently the only version of python we are certain works with the client is **Python 32 bit version 3.6.8**. It is highly recommended that you use this specific version of Python in 32 bit architecture. Many errors were recieved from the *pattern* library using 64 bit and other newer python versions.

### Setup Steps

*Note: all steps should be executed from the client directory of SLIS*

LINUX:<br>

1. run install under client folder <br>
`$chmod +x ./install.sh` <br>
`$install.sh` <br> <br>

2. Run Server: <br>
`$run.sh` <br>
<br><br>


WINDOWS: 

**Method 1**
from powershell console, `cd` into the "client" directory. From there run the follwing command:

`.\build_environment.ps1 "path/to/python368/32bit/python.exe"`

*If this fails try method 2 to manually set up the environment*

**Method 2**

1. Create a new Python virtual environment
`$path/to/python368/32bit/python.exe -m virtualenv env`

2. Activate the virtual environment
`.\env\Scripts\activate.bat`

3. Install Dependancies
`pip install -r requirements.txt`


## Overview

Final system will look like this when completed
![failed to load image](resources/system_architecture.png?raw=true "Title")

## Model Training

## Demos
Each demo click to go to youtube video <br><br>

Turn light on and off with command: idea and black: <br>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/SfzaRuzIsD8/0.jpg)](https://www.youtube.com/watch?v=SfzaRuzIsD8)
<br>
<br>
Say hi Iqbal. (Dr. Iqbal is the professor): <br>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/pjP36tcUtyw/0.jpg)](https://www.youtube.com/watch?v=pjP36tcUtyw)
<br><br>
Demo Grammar Module:<br>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/snQtOAO4r9A/0.jpg)](https://www.youtube.com/watch?v=snQtOAO4r9A)
<br>
<br>
Demo UDP Video Stream:<br>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Syspn-O6Vc0/0.jpg)](https://www.youtube.com/watch?v=Syspn-O6Vc0)
