from pathlib import Path
import os, configparser, argparse
from prompt_toolkit import prompt
from colorama import Fore, Style, init
from prompt_toolkit.styles import Style as promptStyle
from muffinbite.utils.helpers import only_alnum, chain_validators, campaign_exists, argparse_alnum_validator

init(autoreset=True)
style = promptStyle.from_dict({
    'prompt': 'ansiyellow bold',
    '': 'ansigreen bold'
})

campaign_name_validator = chain_validators([
    only_alnum,
    campaign_exists
])

only_alnum_validator = chain_validators([
    only_alnum
])

def create():
    """
    Create a new campaign
    """

    config = configparser.ConfigParser()
    campaigns_dir = "./Campaigns"

    campaign_name = prompt(f"\nEnter name for the campaign: ", style=style, validator=campaign_name_validator)
    campaign_file = os.path.join(campaigns_dir, campaign_name + ".ini")
    subject = prompt(f"\nEnter subject line for the email: ", style=style, validator=only_alnum_validator)
    template = prompt(f"\nEnter template name you want to use: ", style=style, validator=only_alnum_validator)
    attachments = prompt("\nEnter attachments, (separated by commas if more than one): ", style=style)
    cc_emails = prompt("\nEnter CC emails, (separated by commas if more than one): ", style=style)
    bcc_emails = prompt("\nEnter BCC emails, (separated by commas if more than one): ", style=style)
    print()

    config['campaign'] = {
        'name': campaign_name,
        'subject_line': subject,
        'template': template + '.html',
        'attachments': attachments,
        'cc_emails': cc_emails,
        'bcc_email': bcc_emails
    }

    with open(campaign_file, 'w') as file:
        config.write(file)

    return campaign_file

def read(campaign):
    """
    shows a specific campaign details
    """
    campaign_dir = "./Campaigns/"
    file = campaign_dir + campaign + ".ini"

    if os.path.exists(file):
        config = configparser.ConfigParser()
        config.read(file)
        for section in config.sections():
            print(Fore.GREEN + Style.BRIGHT + f"\nDetails for: {campaign}\n")
            print(Fore.BLUE + Style.BRIGHT +f"[{section}]")
            for key, value in config[section].items():
                print(Fore.YELLOW + Style.BRIGHT +f"{key} = {Fore.WHITE + Style.BRIGHT}{value}")
            print()

    else:
        print(Fore.RED + Style.BRIGHT +"\nCampaign not found.\n")

def delete(campaign):
    """
    delete a campaign
    """

    campaigns_dir = "./Campaigns/"
    file = campaigns_dir + campaign + '.ini'

    if os.path.exists(file):
        os.remove(file)
        print(Fore.GREEN + Style.BRIGHT +"\nCampaign deleted successfully!!\n")
    else:
        print(Fore.RED + Style.BRIGHT +"\nCampaign not found.\n")

def read_list():
    """
    list all the campaigns available
    """
    print(Fore.GREEN + Style.BRIGHT +"\nAll the available campaigns:\n")
    campaign_dir = Path("./Campaigns")
    for index, file in enumerate(campaign_dir.iterdir(), start=1):
        if file.is_file():
            print(Fore.YELLOW + Style.BRIGHT +f"\t{index}. {file.stem}")

    print()

def campaign_command(*args):
    """
    Maintains campaign
        Example:
            camp --create                   (creates new campaign)
            camp --show   'campaign_name'   (shows a specific campaign)
            camp --delete 'campaign_name'   (delete a specific campaign)
            camp --list                     (list all the campaigns)
    """

    parser = argparse.ArgumentParser(prog="camp", description="Maintains campaign")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--create", action="store_true", help="create new campaign")
    group.add_argument("--show", metavar="CAMPAIGN_NAME", help="shows a specific campaign")
    group.add_argument("--delete", type=argparse_alnum_validator, metavar="CAMPAIGN_NAME", help="delete a specific campaign")
    group.add_argument("--list", action="store_true", help="list all the campaigns")

    try:
        parsed = parser.parse_args(args)

    except SystemExit:
        return

    if parsed.create:
        create()

    if parsed.delete:
        campaign = parsed.delete
        delete(campaign)

    if parsed.list:
        read_list()

    if parsed.show:
        campaign = parsed.show
        read(campaign)