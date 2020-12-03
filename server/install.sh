#!/bin/bash

echo "Before continuing please see the list of dependencies:"
echo "Python3 REQUIRED < 3.7"
echo "Bazel version: REQUIRED: 3.4.1"
echo "OpenCV"
echo "FFmpeg"
echo ""



echo "Python Version should be < 3.7"
python3 --version

echo "Bazel Version should be 3.4.1"
bazel --version

echo ""
echo ""
read -rsp $'Press enter to continue...\n'
echo ""
echo ""


echo "Cloning Mediapipe and getting correct revision"
git clone https://github.com/google/mediapipe.git
cd mediapipe
git reset --hard 1db91b550aeb43c742042f5ab947b81d90710079
cd ../

#echo "Cloning customizations"
#git clone https://github.com/Rimann91/Sign-Language-Interpretation-System.git


echo "Moving files"
#cp Sign-Language-Interpretation-System/server/mediapipe-basic-handtracker/BUILD_calculator mediapipe/mediapipe/graphs/hand_tracking/calculators/BUILD
#cp Sign-Language-Interpretation-System/server/mediapipe-basic-handtracker/BUILD_subgraphs mediapipe/mediapipe/graphs/hand_tracking/subgraphs/BUILD
#cp Sign-Language-Interpretation-System/server/mediapipe-basic-handtracker/hand_landmark_gpu.pbtxt mediapipe/mediapipe/graphs/hand_tracking/subgraphs/
#cp Sign-Language-Interpretation-System/server/mediapipe-basic-handtracker/hand-gesture-recognition-calculator.cc mediapipe/mediapipe/graphs/hand_tracking/calculators/
#cp Sign-Language-Interpretation-System/server/mediapipe-basic-handtracker/demo_run_graph_main_gpu.cc mediapipe/mediapipe/examples/desktop/

cp mediapipe-basic-handtracker-custom-files/BUILD_calculator mediapipe/mediapipe/graphs/hand_tracking/calculators/BUILD
cp mediapipe-basic-handtracker-custom-files/BUILD_subgraphs mediapipe/mediapipe/graphs/hand_tracking/subgraphs/BUILD
cp mediapipe-basic-handtracker-custom-files/hand_landmark_gpu.pbtxt mediapipe/mediapipe/graphs/hand_tracking/subgraphs/
cp mediapipe-basic-handtracker-custom-files/hand-gesture-recognition-calculator.cc mediapipe/mediapipe/graphs/hand_tracking/calculators/
cp mediapipe-basic-handtracker-custom-files/demo_run_graph_main_gpu.cc mediapipe/mediapipe/examples/desktop/

echo "Building"
cd mediapipe
bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11   mediapipe/examples/desktop/hand_tracking:hand_tracking_gpu

echo "to run mediapipe standalone: bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_gpu   --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_mobile.pbtxt"
echo ""
echo "configuring python dependencies: "
cat Gesture-Recognition-Module/requirements.txt
pip3 install -r Gesture-Recognition-Module/requirements.txt


echo ""
chmod +x run.sh
echo "Install successful"
