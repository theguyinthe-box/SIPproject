#!/bin/sh
adb pull sdcard/DCIM/Camera shared/
adb shell rm sdcard/DCIM/Camera/*

# run the program
python src/model/main.py

# run the GUI
node src/SIP_GUI/main.js