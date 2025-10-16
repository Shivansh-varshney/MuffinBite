import os
from colorama import init, Fore, Style
from muffinbite.management.settings import CONFIG_FILE
init(autoreset=True)
def reset_user_config():
    """
    Deletes the config file
    """

    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(Fore.GREEN + Style.BRIGHT +"\nConfig file deleted. You can set it up again.\n")
    else:
        print(Fore.RED + Style.BRIGHT +"\nNo config file found.\n")