#!/bin/bash
# Install APK on connected device/emulator
# Usage: ./scripts/install_apk.sh [path_to_apk]

set -e

APK_PATH=${1:-"apps/smartkhotba.apk"}

if [ ! -f "$APK_PATH" ]; then
    echo "ERROR: APK not found at $APK_PATH"
    exit 1
fi

echo "Installing $APK_PATH..."
adb install -r "$APK_PATH"
echo "APK installed successfully."
