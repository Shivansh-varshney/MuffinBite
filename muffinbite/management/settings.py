from pathlib import Path
import os, configparser, logging, sys
from muffinbite.utils.abstracts import AbstractSession

BASE_DIR = Path.cwd()
config = configparser.ConfigParser()

CLIENT_SECRET_FILE = BASE_DIR/'credentials.json'

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".muffinbite")
TOKENS_DIR = os.path.join(CONFIG_DIR, "tokens")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

os.makedirs(TOKENS_DIR, exist_ok=True)

config = configparser.ConfigParser()

if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)

class Session(AbstractSession):

    """Provides run time session to keep the CLI interactive and live"""

    def __init__(self):
        self.debug = False
        self.data_files = []
        self.test_data_files = []
        self.logger = None
        self.load()
        self.setup_logger()

    def load(self):

        """loads the session variables"""

        self.debug = config.getboolean("settings", "debug", fallback=False)

        try:

            self.data_files = [
                filename for filename in os.listdir(BASE_DIR/ 'DataFiles')
                if filename.lower().endswith(('.csv', '.xls', '.xlsx'))
                and not filename.lower().startswith('test')
            ]

            self.test_data_files = [
                filename for filename in os.listdir(BASE_DIR/ 'DataFiles')
                if filename.lower().startswith('test')
            ]

        except Exception:

            self.data_files = []
            self.test_data_files = []

    def setup_logger(self):
        """Sets up the logger if debug is enabled"""

        if not self.debug:
            self.logger = None
            return

        logger = logging.getLogger("email_logger")
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler
        log_file = BASE_DIR / "Logs" / "errors.log"
        os.makedirs(log_file.parent, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self.logger = logger
    def reload_config(self):
        config.clear()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE)

    def refresh(self):
        self.reload_config()
        self.load()
        self.setup_logger()
        return self

session = Session()