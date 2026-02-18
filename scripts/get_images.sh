#!/bin/sh
SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
SRC_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

adb pull sdcard/DCIM/Camera $SRC_DIR/model/data/
adb shell rm sdcard/DCIM/Camera/*