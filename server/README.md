## Server Installation Instructions:

1. Install dependencies
see: https://google.github.io/mediapipe/getting_started/install.html

MAKE SURE YOU INSTALL CORRECT VERSIONS FOR MEDIAPIE TO WORK

Python3 REQUIRED < 3.7. recommend 3.6.9 <br />
Bazel REQUIRED: 3.4.1 <br />
OpenCV <br />
FFmpeg <br />
Tensorflow 2.4.0-rc2 or similar. Is installed automatically in install script

*Note: all steps should be executed from the server directory of SLIS*

2. run install under server folder <br>
`$chmod +x ./install.sh` <br>
`$install.sh` <br> <br>

3. Run Server: <br>
`$chmod +x ./run.sh` <br>
`$run.sh` <br>


## TROUBLESHOOTING

Tensorflow version must be around: 2.4.0rc2 to read the model correclty (model-training/models/landmark*.h5)
Bazel MUST be version 3.4.1 (or maybe sooner)
Python MUST be less than 3.7 to work with tensorflow
pip3 and python3 must be in your path for python
