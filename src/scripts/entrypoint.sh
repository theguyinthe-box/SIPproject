#!/bin/sh
adb pull sdcard/DCIM/Camera shared/
adb shell rm sdcard/DCIM/Camera/*