from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style
import os, sys, configparser, argparse, platform

from muffinbite.utils.helpers import load_limits, save_limits
from muffinbite.management.settings import CONFIG_FILE, CONFIG_DIR

init(autoreset=True)

config = configparser.ConfigParser()
if os.path.exists(CONFIG_FILE):
    config.read(CONFIG_FILE)

def write_value(section, key, value):

    if value is None:
        return
    if section not in config:
        config.add_section(section)
    if key == "time_delay" and float(value) < 0.42:
        print(Fore.RED + Style.BRIGHT +"\nTime gap can not be less than 0.42 seconds.")
        return

    if key == "email":
        limits = load_limits()

        if value not in limits:
            limits[value] = {
                "last_send":datetime.now().isoformat(),
                "count": 0
            }

        save_limits(limits)

    config[section][key] = str(value)

def show_config():

    if os.path.exists(CONFIG_FILE):
        print(Fore.GREEN + Style.BRIGHT +"\nCurrent MuffinBite Configuration:\n")
        for section in config.sections():
            print(Fore.BLUE + Style.BRIGHT +f"[{section}]")
            for key, value in config[section].items():
                print(Fore.YELLOW + Style.BRIGHT +f"{key} = {Fore.WHITE + Style.BRIGHT}{value}")
            print()
    else:
        print(Fore.RED + Style.BRIGHT +"\nconfig not set-up, please run: build\n")
    return

def signature(html):

    if os.path.exists(CONFIG_FILE):
        email = config.get("user", "email", fallback=None)

        if email:
            file_name = email.replace("@", "_at_").replace(".", "_") + ".html"

        signatures_dir = Path(CONFIG_DIR)/'signatures'
        os.makedirs(signatures_dir, exist_ok=True)
        location = signatures_dir/file_name

        with open(location, 'w') as signature_file:
            signature_file.write(html)

def signature_on():
    if os.path.exists(CONFIG_FILE):
        config['settings']['signature'] = "True"

def signature_off():
    if os.path.exists(CONFIG_FILE):
        config['settings']['signature'] = "False"

def configure_command(*args):
    """
    Configure settings.
        Example:
            config --user-name name                             (resets user name)
            config --user-email firstname.lastname@example.com  (resets the user email)
            config --service-provider-name provider_name        (resets service provider name)
            config --service-provider-server server_address     (resets service provider server address)
            config --service-provider-login login               (resets service provider login ID)
            config --service-provider-port 000                  (resets service provider port number)
            config --signature "<html>"                         (add signature to all the outgoing mails)
            config --signature-on                               (turn signatures ON)
            config --signature-off                              (turn signatures OFF)
            config --time-delay 0.00                            (time gap between two emails)
            config --show                                       (shows the current configurations)
            config --debug True/False                           (switches debug mode for error logs)
    """

    parser = argparse.ArgumentParser(prog="config", description="Configure the user or service provider.")

    parser.add_argument("--user-name", type=str, help="set user name")
    parser.add_argument("--user-email", type=str, help="set user email")
    parser.add_argument("--service-provider-name", type=str, help="set service provider name")
    parser.add_argument("--service-provider-server", type=str, help="set service provider server")
    parser.add_argument("--service-provider-login", type=str, help="set service provider login")
    parser.add_argument("--service-provider-port", type=str, help="set service provider port")
    parser.add_argument("--show", action="store_true", help="show current configuration")
    parser.add_argument("--debug", type=str, help="switch debug mode for error logs")
    parser.add_argument("--time-delay", type=str, help="time gap between two emails")
    parser.add_argument("--signature", type=str, help="add signature to all the outgoing mails")
    parser.add_argument("--signature-on", action="store_true", help="turn signatures ON")
    parser.add_argument("--signature-off", action="store_true", help="turn signatures OFF")

    try:
        parsed = parser.parse_args(args)
    except SystemExit:
        return

    if parsed.signature:
        signature(parsed.signature)
    elif parsed.show:
        show_config()
    elif parsed.signature_on:
        signature_on()
    elif parsed.signature_off:
        signature_off()

    if not any(vars(parsed).values()):
        print(Fore.RED + Style.BRIGHT +"\nError: No flags provided. Use --help to see options.\n")
        return

    write_value("user", "name", parsed.user_name)
    write_value("user", "email", parsed.user_email)
    write_value("settings", "debug", parsed.debug)
    write_value("settings", "time_delay", parsed.time_delay)
    write_value("service_provider", "provider", parsed.service_provider_name)
    write_value("service_provider", "server", parsed.service_provider_server)
    write_value("service_provider", "login", parsed.service_provider_login)
    write_value("service_provider", "port", int(parsed.service_provider_port) if parsed.service_provider_port else None)

    updates = {k: v for k, v in vars(parsed).items() if k != "show"}

    if any(updates.values()):
        with open(CONFIG_FILE, "w") as file:
            config.write(file)
        print(Fore.GREEN + Style.BRIGHT +"\nConfiguration updated successfully !!\n")

        if platform.system() == "Linux":
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print(Fore.GREEN + Style.BRIGHT +"Please restart CLI to apply changes!!\n")
            return