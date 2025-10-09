import pandas as pd
from pathlib import Path
from datetime import date
from colorama import init, Fore, Style
from email.message import EmailMessage
import csv, sys, time, configparser, mimetypes, base64, re

from muffinbite.utils.abstracts import AbstractSender
from muffinbite.management.settings import session, BASE_DIR, CONFIG_FILE, CONFIG_DIR

init(autoreset=True)
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

class Sender(AbstractSender):
    
    def __init__(self, data_files, config, provider):
        self.data_files = data_files
        self.config = config
        self.provider = provider

    @staticmethod
    def read_file(file):

        filePath = BASE_DIR/'DataFiles'/file

        if file.endswith('.csv'):
            data = pd.read_csv(filePath)
        elif file.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(filePath)
        else:
            raise ValueError("\nFile must be a CSV or Excel (.xls/.xlsx)\n")

        data.columns = data.columns.str.strip()
        data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
        return data

    def send_single_mail(self, message):

        try:

            esp = self.provider
            esp.send(message)

            del message["to"]
            return True, None
        
        except Exception as error:
            if session.debug:
                session.logger.error(f"\nEmail could not be sent to because: {error}\n\n", exc_info=True)
            return False, error

    def email_logs(self, data, file):
        try:
            with open(file, 'a', newline='') as file:
                writer = csv.writer(file)
                for key, value in data.items():
                    row = [
                        value[0],
                        f" {date.today()}",
                        f" {time.strftime("%I:%M:%S %p", time.localtime())}"
                    ]
                    writer.writerow(row)

        except Exception as error:
            if session.debug:
                session.logger.error(f"\nCould not write to {file} due to: {error}\n\n", exc_info=True)

    def embed_images(self, html):
        def replace_img_src(match):
            src = match.group(1)
            path = Path(src)
            if path.exists():
                mime, _ = mimetypes.guess_type(path)
                with open(path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                return f'<img src="data:{mime};base64,{encoded}"'
            else:
                return match.group(0)

        return re.sub(r'<img\s+src="([^"]+)"', replace_img_src, html)

    def format_email_body(self, body_content, row):
        def replacer(match):
                key = match.group(1).strip()
                if key in row:
                    return str(row[key])
                else:
                    print(Fore.RED + f"     Error: column '{key}' is missing in the data\n" + Style.RESET_ALL)
                    sys.exit(1)

        return re.sub(r"\{\{\s*(\w+)\s*\}\}", replacer, body_content)

    def add_signature(self, html_content):
        
        email = config['user']['email']
        file_name = email.replace("@", "_at_").replace(".", "_") + ".html"

        location = CONFIG_DIR+'/signatures/'+file_name

        with open(location, 'r') as sign:
            signature = sign.read()

        return html_content + signature


    def attach(self, message, attachments):

        if len(attachments):
            for file in attachments.split(","):
                location = BASE_DIR/"Attachments"/(file.strip())
                with open(location, "rb") as file:         
                    file_data = file.read()
                    file_name = file.name
                    file_type, _ = mimetypes.guess_type(file_name)
                    if file_type is None:
                        file_type = 'application/octet-stream'
                    maintype, subtype = file_type.split('/', 1)
                    original_name = Path(file.name).name
                    message.add_attachment(file_data, maintype = maintype, subtype =subtype, filename= original_name)

        return message

    def clean_emails(self, raw: str) -> str:
        EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not raw:
            return ""
        emails = [e.strip() for e in raw.split(",") if e.strip()]
        valid = [e for e in emails if re.match(EMAIL_REGEX, e)]
        return ", ".join(valid)

    def send_bulk_email(self, **kwargs):
        try:
            print()
            for file in self.data_files:
                print(Fore.GREEN+'Sending emails from: '+Fore.YELLOW+file)
                print(Style.RESET_ALL)

                data = self.read_file(file)
            
                successful = {}
                writeind = {}

                body_content = kwargs['body_content']
                
                for index, item in data.iterrows():

                    # structure message
                    message = EmailMessage()
                    message['subject'] = self.format_email_body(kwargs['subject'], item)
                    message['from'] = kwargs['from_']
                    body_content = self.format_email_body(body_content, item)
                    message.set_content(body_content)

                    html_content = self.format_email_body(kwargs['html_content'], item)
                    html_content = self.embed_images(html_content)

                    if config.getboolean("settings", "signature", fallback=False):
                        html_content = self.add_signature(html_content)

                    message.add_alternative(html_content, subtype='html')

                    cc = self.clean_emails(kwargs.get('cc_emails', ''))

                    bcc = self.clean_emails(kwargs.get('bcc_emails', ''))

                    if cc:
                        message['Cc'] = cc
                    if bcc:
                        message['Bcc'] = bcc

                    message = self.attach(message, kwargs['attachments'])
                    if not item['Email'] or '@' not in item['Email']:
                        print(Fore.RED +f"      Invalid email: {item['Email']}\n" + Style.RESET_ALL)
                        sys.exit(1)
                    message['to'] = item['Email']

                    # send email
                    email_sent, error = self.send_single_mail(message)

                    if email_sent:
                        successful[index] = [item["Email"]]
                        print(Fore.GREEN+'      sent to: '+Fore.YELLOW+item["Email"])
                        print(Style.RESET_ALL)
                        del message
                    elif not email_sent:
                        writeind[index] = [item["Email"]]
                        print(Fore.RED+'      could not send to: '+Fore.YELLOW+item["Email"])
                        print(Style.RESET_ALL)
                        del message
                    else:
                        if session.debug:
                            ("\nPlease report about the error on issues tab of github.\n\n")
                    
                    time.sleep(float(config['settings']['time_delay']))
                
                self.email_logs(successful, kwargs['success_emails_file'])
                
                if len(writeind) > 0:
                    self.email_logs(writeind, kwargs['failed_emails_file'])
            
            print(Fore.GREEN+'ALl Done !!')
            print(Style.RESET_ALL)
            return True

        except Exception as error:
            if session.debug:
                session.logger.error(f"\nProgram could not start because: {error}\n\n", exc_info=True)