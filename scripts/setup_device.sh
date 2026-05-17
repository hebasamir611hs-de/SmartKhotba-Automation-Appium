#!/bin/bash
# SmartKhotba — Device/Emulator Setup Script
# Usage: ./scripts/setup_device.sh [emulator|device]

set -e

MODE=${1:-emulator}
echo "=== SmartKhotba Device Setup ($MODE) ==="

# Check ADB
if ! command -v adb &> /dev/null; then
    echo "ERROR: ADB not found. Install Android SDK platform-tools."
    exit 1
fi

# Check Appium
if ! command -v appium &> /dev/null; then
    echo "ERROR: Appium not found. Run: npm install -g appium"
    exit 1
fi

# Check UiAutomator2 driver
if ! appium driver list --installed 2>/dev/null | grep -q "uiautomator2"; then
    echo "Installing UiAutomator2 driver..."
    appium driver install uiautomator2
fi

if [ "$MODE" = "emulator" ]; then
    echo "Starting emulator..."
    emulator -avd Pixel_7_API_34 -no-snapshot-load &
    adb wait-for-device
    echo "Emulator ready."
elif [ "$MODE" = "device" ]; then
    echo "Checking connected devices..."
    DEVICES=$(adb devices | grep -v "List" | grep "device$" | wc -l)
    if [ "$DEVICES" -eq 0 ]; then
        echo "ERROR: No device connected. Enable USB debugging."
        exit 1
    fi
    echo "Device connected: $(adb devices | grep 'device$' | awk '{print $1}')"
fi

echo "=== Setup Complete ==="
echo "Start Appium: appium --use-plugins=images"
