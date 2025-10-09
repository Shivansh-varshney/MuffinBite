import subprocess, os, sys

from muffinbite.utils.helpers import create_directories, setup_user_config, log_error
from muffinbite.management.settings  import CLIENT_SECRET_FILE, BASE_DIR

def build(silent=False):
    """
    Create the necessary directories and files for the working of the project
    """
    try:
        print()
        if not silent:
            create_directories()
        setup_user_config()
        if not silent:
            print("Setup completed successfully !!\n")

        if not os.path.exists(CLIENT_SECRET_FILE):
            print(f"""
\tPlease provide default credentials via, `credentials.json` file in the {BASE_DIR},
\tYou can get it from google cloud console for gmail api.
\tFor further details, please visit: https://console.cloud.google.com/ and search for Gmail API
""")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {e}")
    except Exception as e:
        log_error(f"Unexpected error: {e}")