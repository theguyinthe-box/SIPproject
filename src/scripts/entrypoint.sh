#!/bin/sh
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
SRC_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
sh $SCRIPT_DIR/clear_shared_folders.sh

adb pull sdcard/DCIM/Camera $SRC_DIR/shared/
adb shell rm sdcard/DCIM/Camera/*

#go to main.py directory
# run the program
python $SRC_DIR/model/main.py

echo "moving altered files to test dir..."
mv $SRC_DIR/shared/altered/* $SRC_DIR/shared/test/

echo "creating 5 copies of original..."
for i in $(seq 1 5); do
    cp $SRC_DIR/shared/aligned/* $SRC_DIR/shared/test/original_aligned_$i.png
done

echo "deleting any leftover images..."
rm $SRC_DIR/shared/aligned/*
rm $SRC_DIR/shared/alignment_vector/*

# run the GUI
node src/SIP_GUI/main.js