import os
import subprocess
import sys
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def check_env():
    print("--- Android Environment Check ---")
    
    android_home = os.getenv("ANDROID_HOME")
    print(f"ANDROID_HOME: {android_home}")
    
    if not android_home or not os.path.exists(android_home):
        print("ERROR: ANDROID_HOME is not set or path does not exist.")
        return False
    
    # Define adb path
    adb_path = os.path.join(android_home, "platform-tools", "adb.exe")
    print(f"ADB Path: {adb_path}")
    
    if not os.path.exists(adb_path):
        print(f"ERROR: adb.exe not found at {adb_path}")
        return False
    
    # Try to execute adb
    try:
        result = subprocess.run([adb_path, "version"], capture_output=True, text=True)
        print("ADB Version Output:")
        print(result.stdout)
        if result.returncode != 0:
            print(f"ERROR: adb returned non-zero exit code: {result.returncode}")
            return False
    except Exception as e:
        print(f"ERROR: Failed to execute adb: {e}")
        return False
    
    # Check for connected devices
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
        print("Connected Devices:")
        print(result.stdout)
    except Exception as e:
        print(f"ERROR: Failed to list devices: {e}")
    
    print("--- Check Complete: SUCCESS ---")
    return True

if __name__ == "__main__":
    if check_env():
        sys.exit(0)
    else:
        sys.exit(1)


def verify_app_activity():
    """Confirm APP_ACTIVITY string matches what's in the APK manifest."""
    import subprocess, os
    from dotenv import load_dotenv
    load_dotenv()
    apk = "apps/smartkhotba.apk"
    expected = os.getenv("APP_ACTIVITY", "")
    out = subprocess.run(
        ["aapt", "dump", "badging", apk], capture_output=True, text=True
    )
    if "launchable-activity: name='" in out.stdout:
        actual = out.stdout.split("launchable-activity: name='")[1].split("'")[0]
        match = actual == expected
        print(f"Expected: {expected}\nActual:   {actual}\nMatch:    {match}")
        return match
    print("Could not extract launchable activity from APK.")
    return False


if __name__ == "__main__":
    verify_app_activity()
