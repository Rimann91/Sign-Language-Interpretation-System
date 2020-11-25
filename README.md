# Sign Language Interpretation System

## Introduction
This Sign Language Interpretation System is a class project for CSC 450 under Dr. Razib Iqbal at Missouri State University.

The sign language interpretation system will take a video stream input from an integrated camera and interpret hand gestures into pre-defined commands. It will recognize the gestures with high accuracy in real time. The system will be tested with a smart home interface connected to the program output, which would be a valid command that is interpreted from the sign language input.  The system will act as a means of processing hand sign communication for the potential use by individuals with hearing impairments or other disabilities that require visual communication devices for interacting with technology. The actualization of this product will provide a way for more people to intuitively access technology that was previously diffcult, or impossible, to use. The primary goal of the sign language interpretation system is to bridge those gaps.

## Client Installation Instructions:

The current client has only been tested on Windows 10. Currently the only version of python we are certain works with the client is **Python 32 bit version 3.6.8**. It is highly recommended that you use this specific version of Python in 32 bit architecture. Many errors were recieved from the *pattern* library using 64 bit and other newer python versions.

### Setup Steps

*Note: all steps should be executed from the client directory of SLIS*

1. Create a new Python virtual environment
`$path/to/python368/32bit/python.exe -m virtualenv env`

2. Activate the virtual environment
`.\env\Scripts\activate.bat`

3. Install Dependancies
`pip install -r requirements.txt`
