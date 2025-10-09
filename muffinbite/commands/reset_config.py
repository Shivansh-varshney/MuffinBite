import os

from muffinbite.management.settings import CONFIG_FILE

def reset_user_config():
    """
    Deletes the config file
    """

    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print("\nConfig file deleted. You can set it up again.\n")
    else:
        print("\nNo config file found.\n")