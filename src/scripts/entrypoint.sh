#!/bin/sh
sh /scripts/clear_shared_folders.sh

#adb pull sdcard/DCIM/Camera shared/
#adb shell rm sdcard/DCIM/Camera/*

#go to main.py directory
# run the program
python /src/model/main.py

# run the GUI
#node src/SIP_GUI/main.js