import argparse, configparser, os, csv

from muffinbite.sender.sender import Sender
from muffinbite.management.settings import session, CONFIG_FILE
from muffinbite.utils.helpers import get_html, get_campaign, get_text_from_html
from muffinbite.commands.build import build
from muffinbite.esp.smtp_esp import SmtpESP
from muffinbite.esp.google_esp import GoogleESP

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

def get_esp():
        
        provider = config['service_provider']['provider']

        if provider.lower() == "gmail":
            return GoogleESP(config=config)
        else:
            return SmtpESP()
    
def create_email_structure():

    campaign = get_campaign()
    subject = campaign['subject_line']
    cc_emails = ''
    bcc_emails = ''
    success_emails_file = "./EmailStatus/" + campaign['name'] + '_successfull_emails.csv'
    failed_emails_file = "./EmailStatus/" + campaign['name'] + '_failed_emails.csv'

    if not os.path.exists(success_emails_file):
        with open(success_emails_file, 'w') as file:
            writer = csv.writer(file)
            row = ["Email", "Date", "Time"]
            writer.writerow(row)
    
    if not os.path.exists(failed_emails_file):
        with open(failed_emails_file, 'w') as file:
            writer = csv.writer(file)
            row = ["Email", "Date", "Time"]
            writer.writerow(row)

    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        build(silent=True)
        return False, None

    provider = config['service_provider']['provider']
    if provider.lower() == "gmail":
        from_ = config['user']['email']
    else:
        from_ = f"{config['user']['name']} <{config['user']['email']}>"
    
    cc_emails = (campaign.get("cc_emails") or "").strip()
    bcc_emails = (campaign.get("bcc_emails") or "").strip()
    attachments = (campaign.get("attachments") or "").strip()

    html_content = get_html(campaign['template'])
    body_content = get_text_from_html(html_content)

    return {
        "subject": subject,
        "from_": from_,
        "html_content": html_content,
        "body_content": body_content,
        "cc_emails": cc_emails,
        "bcc_emails": bcc_emails,
        "attachments":attachments,
        "success_emails_file": success_emails_file,
        "failed_emails_file": failed_emails_file,
    }

def send_test():
    
    if not session.test_data_files:
        print("\nPlease provide test data to send emails.\n")
        return

    email = Sender(data_files=session.test_data_files, config=config, provider=get_esp())
    email.send_bulk_email(**create_email_structure())

def send_real():

    if not session.data_files:
        print("\nPlease provide data files to send emails.\n")
        return
    
    email = Sender(data_files=session.data_files, config=config, provider=get_esp())
    email.send_bulk_email(**create_email_structure())

def send_command(*args):

    """
    Sends emails 
        Example:
            send --test (sends emails from test data)
            send --real (sends emails from real data)
    """

    parser = argparse.ArgumentParser(prog="send", description="sends emails")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--test", action="store_true", help="send test emails")
    group.add_argument("--real", action="store_true", help="send real emails")

    try:
        parsed = parser.parse_args(args)

    except SystemExit:
        return
    
    if parsed.test:
        send_test()

    elif parsed.real:
        send_real()