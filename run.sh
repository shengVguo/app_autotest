#!/bin/bash

PROJECT_DIR=$(cd "$(dirname "$0")/";pwd)
ATX_PACKAGE_NAME=com.github.uiautomator

function main() {

    # echo 'start install the test apk'
    # adb install -r -t *.apk

    echo 'clear the reports'
    rm -r $PROJECT_DIR/reports/*

    echo 'Initialize atx service'
    adb shell am force-stop $ATX_PACKAGE_NAME

    echo 'start pytest'
    pytest
}

main
