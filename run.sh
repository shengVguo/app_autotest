#!/bin/bash

project_dir=$(cd "$(dirname "$0")/";pwd)
atx_package_name=$(grep ATX_PACKAGE_NAME $project_dir/docker/.env | awk -F"=" '{print $2}')

function main() {

    echo 'start install the test apk'
    adb install -r -t *.apk

    echo 'clear the reports'
    rm -r $project_dir/reports/*

    echo 'Initialize atx service'
    adb shell am force-stop $atx_package_name

    echo 'start pytest'
    pytest
}

main
