# How to install

- Clone original mediapipe source https://github.com/google/mediapipe
- Remove "_calculator" from "BUILD_calculator" and replace BUILD file in /mediapipe/graphs/hand_tracking/calculators directory.
- Remove "_subgraphs" from "BUILD_subgraphs" and replace BUILD file in /mediapipe/graphs/hand_tracking/subgraphs directory.
- Add "hand-gesture-recognition-calculator.cc" to /mediapipe/graphs/hand_tracking/calculators directory.
- Replace hand_landmark_gpu.pbtxt graph in /mediapipe/graphs/hand_tracking/subgraphs directory with the one in this directory of the same name.
- Build mediapipe hand tracking gpu and run as normal. The console should output the detected hand gestures per frame of landmarks that it receives as input.



MediaPipe TCP Input port is 4433 defined in demo_run_graph_main_gpu.css
Hand Gesture Recognitino Input Port is 6009 defined in GestureModule.py and hand_gesture_recognition_calculator.css

Build. Make sure you are in mediapipe root directory: 

Install Dependencies:
https://google.github.io/mediapipe/getting_started/install.html
Python version: 
OpenCV Version: 
Bazel Version: 

bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 \
  mediapipe/examples/desktop/hand_tracking:hand_tracking_gpu



  RUN: 
GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_gpu \
  --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_mobile.pbtxt