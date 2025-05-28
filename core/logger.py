import logging
from resources.settings import Settings

def setup_logging():
    logging.basicConfig(
        filename=Settings.LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

