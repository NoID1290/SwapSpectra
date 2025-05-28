import winreg as reg
from resources.settings import Settings

def read_status():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, Settings.REGISTRY_PATH, 0, reg.KEY_READ)
    status = reg.QueryValueEx(key, "GSyncStatus")[0]
    reg.CloseKey(key)
    return status

def update_status_in_registry(option):
    key = reg.CreateKey(reg.HKEY_CURRENT_USER, Settings.REGISTRY_PATH)
    reg.SetValueEx(key, "GSyncStatus", 0, reg.REG_SZ, "ON" if option == 2 else "OFF")
    reg.CloseKey(key)
