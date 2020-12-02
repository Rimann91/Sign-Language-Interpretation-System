#!/bin/bash

killbg() {
        for p in "${pids[@]}" ; do
                kill "$p";
        done
}
trap killbg EXIT
pids=()
echo "Starting mediapipe process"
cd mediapipe
bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_gpu   --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_mobile.pbtxt &
pids+=($!)
echo ""
echo "Starting python UDP receiver"
python3 ../udp_reciever.py &
pids+=($!)
echo ""
echo "Starting Gesture Interpret Model"
python3 ../Gesture-Recognition-Module/GestureModule.py



