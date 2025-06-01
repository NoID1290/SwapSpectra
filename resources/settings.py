class Settings:
    APP_TITLE = "SwapSpectra"
    APP_VERSION = "v0.3.1"
    BUILD_VERSION = "250601"
    MAIN_TITLE = "SwapSpectra"
    EXECUTABLE_PATH = "gsyncwrapper-1.1.0-x86_64.dll"
    LOG_FILE = "gsyncwrapper.log"
    ICON_PATH = "gvico.ico"
    REGISTRY_PATH = r"Software\NoID Softwork\GvSync"
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 600
    BUTTON_ON_TEXT = "Turn G-SYNC ON"
    BUTTON_OFF_TEXT = "Turn G-SYNC OFF"
    BUTTON_REFRESH_TEXT = "Refresh"
    COPY_RIGHT = "© 2024-2025 NoID Softwork"
    REGISTRY_PATH_DLSS = r"SOFTWARE\NVIDIA Corporation\Global\NGXCore"
    DLSS_ON_TEXT = "DLSS Overlay ON"
    DLSS_OFF_TEXT = "DLSS Overlay OFF"
    DLSS_SWAP_TEXT = "Swap DLSS"
    COPYRIGHT_TEXT = "© 2024-2025 NoID Softwork - All rights reserved."
    TXT_TRUE = "ON"
    TXT_FALSE = "OFF"

    # Path to the DLL
    gvlibname = "idsw-gvlib.dll"
    
    # System Tray Settings
    # Need to put this to an external file
    #CLOSE_ON_TRAY = False
    #RUN_AS_ADMIN = True # Keep to False for now until we have a proper code
     

class format_text:
    cpVbuild = f"{Settings.COPY_RIGHT}  {Settings.APP_VERSION}"



