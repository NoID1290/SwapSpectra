"""
NVAPI Initialization Module.
Handles the initialization and setup of NVIDIA GPU API wrapper through CLR interop.
"""

import clr
import sys
import os
import logging
import atexit
from typing import Optional
from resources.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_nvapi_loaded = False

def initialize_nvapi() -> bool:
    """
    Initialize the NVAPI wrapper library.
    
    Returns:
        bool: True if initialization successful, False otherwise.
    
    Raises:
        FileNotFoundError: If the required DLL is not found.
        ImportError: If there are issues loading the assembly.
    """
    global _nvapi_loaded
    
    # Check if already initialized
    if _nvapi_loaded:
        logger.debug("NVAPI already initialized")
        return True

    # Verify nvapi64.dll exists
    nvapi_path = os.path.join(os.environ.get('SystemRoot', ''), 'System32', 'nvapi64.dll')
    if not os.path.exists(nvapi_path):
        logger.error(f"NVAPI DLL not found at: {nvapi_path}")
        return False

    # Add the directory containing your wrapper DLL to the path
    dll_path = Settings.gvlibname
    if not os.path.exists(dll_path):
        logger.error(f"Wrapper DLL not found at path: {dll_path}")
        raise FileNotFoundError(f"DLL not found at {dll_path}")
    
    dll_dir = os.path.dirname(dll_path)
    if dll_dir not in sys.path:
        sys.path.append(dll_dir)
        logger.debug(f"Added DLL directory to path: {dll_dir}")

    # Load the assembly
    try:
        clr.AddReference("idsw-gvlib")
        from NvApiCall import NvapiWrapper  # type: ignore
        
        # Initialize NVAPI
        success = NvapiWrapper.Initialize()
        if success:
            _nvapi_loaded = True
            logger.info("NVAPI initialization successful")
            
            # Register cleanup on exit
            atexit.register(shutdown_nvapi)
            
            # Get and log NVAPI version
            version = NvapiWrapper.GetVersion()
            if version:
                logger.info(f"NVAPI Version: {version}")
            
            return True
        else:
            logger.error("NVAPI initialization failed")
            return False
            
    except Exception as e:
        logger.error(f"Failed to load NVAPI assembly: {str(e)}")
        raise ImportError(f"Failed to load NVAPI assembly: {str(e)}")

def shutdown_nvapi() -> None:
    """Properly shutdown NVAPI when the program exits."""
    global _nvapi_loaded
    if _nvapi_loaded:
        try:
            from NvApiCall import NvapiWrapper  # type: ignore
            NvapiWrapper.Unload()
            logger.info("NVAPI shutdown successful")
            _nvapi_loaded = False
        except Exception as e:
            logger.error(f"Error during NVAPI shutdown: {str(e)}")