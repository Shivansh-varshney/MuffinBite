import sys
import logging
from settings import BASE_DIR

# Create logger
logger = logging.getLogger("email_logger")
logger.setLevel(logging.DEBUG)  # Capture all levels

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# File handler
file_location = BASE_DIR/'logs'/'errors.log'
file_handler = logging.FileHandler(file_location, mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
