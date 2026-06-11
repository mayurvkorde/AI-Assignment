import logging
from logging.handlers import RotatingFileHandler

# Set up logging

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=5242880, backupCount=5),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)