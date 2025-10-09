import os, configparser, argparse
from prompt_toolkit import prompt
from pathlib import Path

from muffinbite.utils.helpers import only_alnum, chain_validators, campaign_exists, argparse_alnum_validator

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

    campaign_name = prompt("Enter name for the campaign: ", validator=campaign_name_validator)
    campaign_file = os.path.join(campaigns_dir, campaign_name + ".ini")

    subject = prompt("Enter subject line for the email: ", validator=only_alnum_validator)
    template = prompt("Enter template name you want to use: ", validator=only_alnum_validator)
    attachments = input("Enter attachments, (separated by commas if more than one): ")
    cc_emails = input("Enter CC emails, (separated by commas if more than one): ")
    bcc_emails = input("Enter BCC emails, (separated by commas if more than one): ")

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
        with open(file, 'r') as file:
            content = file.read()
        print(f"\nDetails for: {campaign}\n")
        print(content)
    
    else:
        print("\nCampaign not found.\n")

def delete(campaign):
    """
    delete a campaign
    """

    campaigns_dir = "./Campaigns/"
    file = campaigns_dir + campaign + '.ini'
    
    if os.path.exists(file):
        os.remove(file)
        print("\nCampaign deleted successfully!!\n")
    else:
        print("\nCampaign not found.\n")

def read_list():
    """
    list all the campaigns available
    """
    print("\nAll the available campaigns:\n")
    campaign_dir = Path("./Campaigns")
    for file in campaign_dir.iterdir():
        if file.is_file():
            print(f"\t{file.stem}")
    
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