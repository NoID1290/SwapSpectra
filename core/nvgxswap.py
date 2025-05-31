import clr
import sys
import os
import logging
from typing import Optional
from resources.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the directory containing your DLL to the path
dll_path = Settings.gvlibname
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"DLL not found at {dll_path}")

sys.path.append(os.path.dirname(dll_path))

# Load the assembly
try:
    clr.AddReference("idsw-gvlib")
    from NvngxUpdaterLib import NvngxUpdater # type: ignore
    from ClearNVGX import ClearNvngx  # type: ignore
except Exception as e:
    logger.error(f"Failed to load idsw-gvlib assembly: {e}")
    raise

def update_nvngx(dll_path: str) -> bool:
    """
    Update NVNGX DLL by copying it to the appropriate location and updating config.
    
    Args:
        dll_path: Path to the source NVNGX DLL file
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    if not dll_path:
        logger.error("DLL path cannot be empty")
        return False
        
    dll_path = os.path.abspath(dll_path)
    if not os.path.exists(dll_path):
        logger.error(f"DLL not found at {dll_path}")
        return False
        
    try:
        logger.info(f"Attempting to update NVNGX DLL from {dll_path}")
        NvngxUpdater.UpdateNvngxDll(dll_path)
        logger.info("NVNGX DLL update completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating NVNGX DLL: {e}")
        return False

class NvngxSwap:
    """Encapsulates the NVNGX DLL update process."""

    @staticmethod
    def run():
        """Entry point for running the update process with user interaction."""
        try:
            dll_path = input("Enter the path to the DLSS DLL (e.g., C:\\path\\to\\nvngx.dll): ").strip()
            if update_nvngx(dll_path):
                print("Update completed successfully")
            else:
                print("Update failed, check the logs for details")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.exception("Unexpected error occurred")