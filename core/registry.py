import winreg as reg
from resources.settings import Settings


# Read the status of the GSync
def read_status():
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, Settings.REGISTRY_PATH, 0, reg.KEY_READ)
    except FileNotFoundError:
        # If the key does not exist, return a default status
        return "OFF"
    except PermissionError:
        print("PermissionError: Access is denied. Please run the application as an administrator.")
        return "OFF"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "OFF"
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, Settings.REGISTRY_PATH, 0, reg.KEY_READ)
    status = reg.QueryValueEx(key, "GSyncStatus")[0]
    reg.CloseKey(key)
    return status
# Update the status of the GSync
def update_status_in_registry(option):
    key = reg.CreateKey(reg.HKEY_CURRENT_USER, Settings.REGISTRY_PATH)
    reg.SetValueEx(key, "GSyncStatus", 0, reg.REG_SZ, "ON" if option == 2 else "OFF")
    reg.CloseKey(key)

# Read DLSS Overlay status
def read_dlss_overlay_status():
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, Settings.REGISTRY_PATH_DLSS, 0, reg.KEY_READ)
    status = reg.QueryValueEx(key, "ShowDlssIndicator")[0]
    reg.CloseKey(key)
    return "ON" if status == 0x400 else "OFF"

# Update DLSS Overlay status
def update_dlss_overlay_in_registry(option):
    try:
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, Settings.REGISTRY_PATH_DLSS, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, "ShowDlssIndicator", 0, reg.REG_DWORD, 0x400 if option == 1 else 0x0)
        reg.CloseKey(key)
    except PermissionError:
        print("PermissionError: Access is denied. Please run the application as an administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Read NVNGX status from the registry
def read_nvngx_status() -> str:
    """
    Reads the NVNGX status from the Windows registry.
    
    Returns:
        str: The status of NVNGX, either "ON" or "OFF".
    """
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, Settings.REGISTRY_PATH, 0, reg.KEY_READ)
        status = reg.QueryValueEx(key, "NvngxStatus")[0]
        reg.CloseKey(key)
        return status
    except FileNotFoundError:
        return "OFF"
    except Exception as e:
        print(f"An error occurred while reading NVNGX status: {e}")
        return "OFF"








