# Thermal-Surveillance 
 
Temperature of a given person will be identified using face detection.

We use FLIR C5 camera as a input source, feel free to you any type of thermal camera.

Snap shots of persons with high temperature is saved automatically.

Face detection using opencv's “hidden” deep learning-based face detector.

This module uses the dnn module of opencv. Primary contributor for rhe dnn module is Aleksandr Rybnikov (https://github.com/arrybn). Also, thanks to Adrian Rosebrock(www.pyimagesearch.com) for an awesome tutorial which enabled me to write this code. I am including the prototext file and caffe model for the same, which again is, provided by Adrian Rosebrock. Check out his tutorial: https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/.

Steps to run:

    clone this repository
    pip install requirements.txt
    run main.py


