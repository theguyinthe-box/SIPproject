#!/bin/sh
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
SRC_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
SHARED_DIR="{$SRC_DIR}/shared"
sh {$SCRIPT_DIR}/clear_shared_folders.sh

#adb pull sdcard/DCIM/Camera {$SRC_DIR}/shared/
#adb shell rm sdcard/DCIM/Camera/*

#go to main.py directory
# run the program
python {$SRC_DIR}/model/main.py

mv $SHARED_DIR/altered/* $SHARED_DIR/test/
for i in {1..5}; do
    cp $SHARED_DIR/aligned/* $SHARED_DIR/test/og_aligned_$i.png
done
rm cp $SHARED_DIR/aligned/*
rm cp $SHARED_DIR/alignment_vector/*

# run the GUI
#node src/SIP_GUI/main.js