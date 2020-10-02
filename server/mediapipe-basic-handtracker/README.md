# How to install

- Remove "_calculator" from "BUILD_calculator" and replace BUILD file in /mediapipe/graphs/hand_tracking/calculators directory.
- Remove "_subgraphs" from "BUILD_subgraphs" and replace BUILD file in /mediapipe/graphs/hand_tracking/subgraphs directory.
- Add "hand-gesture-recognition-calculator.cc" to /mediapipe/graphs/hand_tracking/calculators directory.
- Replace hand_landmark_gpu.pbtxt graph in /mediapipe/graphs/hand_tracking/subgraphs directory with the one in this directory of the same name.
- Build mediapipe hand tracking gpu and run as normal. The console should output the detected hand gestures per frame of landmarks that it receives as input.
