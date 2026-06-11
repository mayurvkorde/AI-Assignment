import logging
from logging.handlers import RotatingFileHandler
from app.config.config import config

# Set up logging

logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(config.LOG_FILE, maxBytes=5242880, backupCount=5),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)