import csv
import time
import base64
import mimetypes
import pandas as pd
import sys
from pathlib import Path
from datetime import date
from email.message import EmailMessage
from colorama import init, Fore, Style

from .googleConfiguration import Configure
from .logger_config import logger
from settings import BASE_DIR, ATTACHMENTS

init(autoreset=True)

class AutoEmail():
    
    def __init__(self, data_files, attachments = ATTACHMENTS):
        self.data_files = data_files
        self.attachments = attachments

    def send_single_mail(self, message):

        try:

            service = Configure(scope='SEND').get_service()

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            is_email_sent = service.users().messages().send(userId='me', body={'raw': encoded_message}).execute()

            del message["to"]
            return True, None
        
        except Exception as error:
            logger.error(f"Email could not be sent to because: {error}", exc_info=True)
            return False, error

    def email_logs(self, data, fileName):
        filePath = BASE_DIR/'EmailStatus'/fileName
        try:
            with open(filePath, 'a', newline='') as file:
                writer = csv.writer(file)
                for key, value in data.items():
                    row = [
                        value[0],
                        f" {date.today()}",
                        f" {time.strftime("%I:%M:%S %p", time.localtime())}"
                    ]
                    writer.writerow(row)

        except Exception as error:
            logger.error(f"Could not write to {filePath} due to: {error}", exc_info=True)

    def format_email_body(self, body_content, row):
        try:
            return body_content.format(**row)
        except KeyError as e:
            missing_key = e.args[0]
            print(Fore.RED + f"     Error: column '{missing_key}' is missing in the data\n" + Style.RESET_ALL)
            sys.exit(1)

    def attach(self, message):
        #if we want to attach something

        if len(self.attachments):
            for file in self.attachments:
                location = BASE_DIR/"Attachments"/file
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

    @staticmethod
    def read_file(file):

        filePath = BASE_DIR/'DataFiles'/file

        if file.endswith('.csv'):
            data = pd.read_csv(filePath)
        elif file.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(filePath)
        else:
            raise ValueError("File must be a CSV or Excel (.xls/.xlsx)")

        data.columns = data.columns.str.strip()
        data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
        return data

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

                    name = kwargs.get('name', False)

                    # structure message
                    message = EmailMessage()
                    message['subject'] = kwargs['subject']
                    message['from'] = kwargs['from_']
                    body_content = self.format_email_body(body_content, item)
                    message.set_content(body_content)

                    if kwargs['has_HTML']:
                        html_content = self.format_email_body(kwargs['html_content'], item)
                        message.add_alternative(html_content, subtype='html')

                    message = self.attach(message)
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
                        writeind[index] = [error]
                        print(Fore.RED+'      sent to: '+Fore.YELLOW+item["Email"])
                        print(Style.RESET_ALL)
                        del message
                    else:
                        logger.error("Please report about the error on issues tab of github.")
                    
                    time.sleep(0.42)
                
                self.email_logs(successful, 'successful_emails.csv')
                
                if len(writeind) > 0:
                    self.email_logs(writeind, 'failed_emails.csv')
            
            print(Fore.GREEN+'ALl Done !!')
            print(Style.RESET_ALL)
            return True

        except Exception as error:
            logger.error(f"Program could not start because: {error}", exc_info=True)