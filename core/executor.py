import subprocess
import os

def run_gsync_command(gswdll, option):
    if not os.path.exists(gswdll):
        return False, f"Executable not found: {gswdll}"

    try:
        result = subprocess.run([gswdll, str(option)], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return True, f"G-SYNC {'ON' if option == 2 else 'OFF'} applied!"
        else:
            return False, f"Command failed: {result.stderr}"
    except Exception as e:
        return False, f"An error occurred: {e}"

