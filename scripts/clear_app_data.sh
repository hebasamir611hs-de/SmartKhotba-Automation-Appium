#!/bin/bash
# Clear app data before test run (clean state)
# Usage: ./scripts/clear_app_data.sh [package_name]

set -e

PACKAGE=${1:-"com.smartkhotba.app"}

echo "Clearing data for $PACKAGE..."
adb shell pm clear "$PACKAGE"
echo "App data cleared."
