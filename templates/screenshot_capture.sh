sleep 2s
adb shell am start -n <package_name>/<package_name>.MainActivity
sleep 5s
adb shell screencap -p /sdcard/<package_name>.png
sleep 2s
adb pull /sdcard/<package_name>.png <output_screenshot_folder>/<package_name>.png
adb shell rm /sdcard/<package_name>.png
