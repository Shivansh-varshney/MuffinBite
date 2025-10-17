from pathlib import Path
from bs4 import BeautifulSoup
import os, re, argparse, sys, configparser

from muffinbite.management.settings import CONFIG_DIR, CONFIG_FILE
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style as promptStyle
from prompt_toolkit.validation import Validator, ValidationError

init(autoreset=True)
style = promptStyle.from_dict({
    "prompt": "ansiyellow bold",
    "": "ansigreen bold"
})

dirs_to_create = ["Attachments", "DataFiles", "EmailStatus", "Templates", "Campaigns"]

# validation related utility functions
def campaign_does_not_exists(text):
    """
    Throws error if the entered campaign name is not found
    """
    path = "./Campaigns"
    
    if not os.path.exists(os.path.join(path, text + '.ini')):
        raise ValidationError(message="No campaign with that name")

def campaign_exists(text):
    """
    Throws error if the entered campaign name is found
    """
    path = "./Campaigns"
    if os.path.exists(os.path.join(path, text + ".ini")):
        raise ValidationError(message="Campaign already exists")

def only_alnum(text):
    """
    Throws error if the user enters prohibited characters
    """
    if not re.match(r'[A-Za-z0-9 ,}{]', text):
        raise ValidationError(message="Only letters and numbers are allowed")

def chain_validators(validators):
    """
    Applies the validators to user inputs
    """
    def _validate(text):
        for v in validators:
            v(text)
        return True
    return Validator.from_callable(_validate)

def argparse_alnum_validator(text):

    if not re.match(r'[A-Za-z0-9 ,]', text):
        raise argparse.ArgumentTypeError("Only letters and numbers are allowed")
    return text

# campaign related utility functions
def get_campaign():
    """
    Retrieves the campaign from the database
    """

    DIR = './Campaigns'
    config = configparser.ConfigParser()

    validator = chain_validators([
        only_alnum,
        campaign_does_not_exists
    ])

    campaign_name = prompt("\nEnter the campaign name you want to use: ", style=style, validator=validator)

    FILE = os.path.join(DIR, campaign_name + '.ini')

    if os.path.exists(FILE):
        config.read(FILE)
        return config['campaign']
    
    return 
    
def get_html(template):

    """
    Retrieves the html content from the template file
    """
    
    with open(f"./Templates/{template}", 'r') as file:
        content = file.read()

    return content

def get_text_from_html(html):

    """
    Retrieves the pure text from html content for fallback
    """

    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup(['script', 'style']):
        tag.extract()

    return soup.get_text(separator="\n", strip=True)

# build related utility functions
def setup_user_config():
    """
    Configures the initial config file for muffinbite with user details
    """
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    if 'user' not in config or 'name' not in config['user'] or 'email' not in config['user']:
        print(Fore.GREEN + Style.BRIGHT +"Let's set up your MuffinBite user info:\n")
        name = input(Fore.YELLOW + Style.BRIGHT +"Enter your name: " + Fore.GREEN + Style.BRIGHT ).strip()
        email = input(Fore.YELLOW + Style.BRIGHT +"Enter your email: " + Fore.GREEN + Style.BRIGHT ).strip()
        config['user'] = {'name': name, 'email': email}

    if 'email' not in config or 'provider' not in config['service_provider']:
        print(Fore.YELLOW + Style.BRIGHT +"\nChoose your email provider:")
        print(Fore.YELLOW + Style.BRIGHT +f"  1. {Fore.BLUE + Style.BRIGHT}Gmail (recommended)")
        print(Fore.YELLOW + Style.BRIGHT +f"  2. {Fore.BLUE + Style.BRIGHT}Other SMTP service")
        choice = input(Fore.YELLOW + Style.BRIGHT +"Provider (enter 1 or 2): " + Fore.GREEN + Style.BRIGHT ).strip()

        if choice == '1':
            config['service_provider'] = {'provider': 'gmail'}
            print(Fore.GREEN + Style.BRIGHT +"\nGmail token will be generated separately via OAuth flow.")
        else:
            provider_name = input(Fore.YELLOW + Style.BRIGHT +"Enter provider name (any custom name): " + Fore.GREEN + Style.BRIGHT).strip()
            smtp_server = input(Fore.YELLOW + Style.BRIGHT +"SMTP server (e.g., smtp.example.com): " + Fore.GREEN + Style.BRIGHT).strip()
            port = input(Fore.YELLOW + Style.BRIGHT +"SMTP port (usually 587): " + Fore.GREEN + Style.BRIGHT).strip()
            login = input(Fore.YELLOW + Style.BRIGHT +"Login email/username: " + Fore.GREEN + Style.BRIGHT).strip()

            config['service_provider'] = {
                'provider': provider_name,
                'server': smtp_server,
                'port': port,
                'login': login,
            }
    
    if 'settings' not in config:
        config['settings'] = {
            'debug': False,
            'signature': False,
            'time_delay': 0.42
            }

    with open(CONFIG_FILE, 'w') as file:
        config.write(file)
        print(Fore.GREEN + Style.BRIGHT +"\nUser configuration saved successfully!\n")

    return config

def log_error(msg):
    print(Fore.RED + Style.BRIGHT +f"[ERROR] {msg}", file=sys.stderr)
   
def create_directories():
    print(Fore.YELLOW + Style.BRIGHT +"Checking for directories...\n")
    for dir_name in dirs_to_create:
        path = Path(dir_name)
        if not path.exists():
            path.mkdir(exist_ok=True)
            print(Fore.GREEN + Style.BRIGHT +f"    Created: {Fore.BLUE + Style.BRIGHT}{path}")
        else:
            print(Fore.BLUE + Style.BRIGHT +f"    {path}{Fore.GREEN + Style.BRIGHT} already exists")
    
    print()
