import smtplib, pwinput, configparser

from muffinbite.utils.abstracts import AbstractESP
from muffinbite.management.settings import session, CONFIG_FILE

class SmtpESP(AbstractESP):

    def __init__(self):
        self.service = ''

    def get_credentials(self):

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        
        service_provider = config['service_provider']

        provider = service_provider['provider']
        login = service_provider['login']
        server = service_provider['server']
        port = service_provider['port']

        password = pwinput.pwinput(f"\tEnter password for {server}: ", mask="*")

        return provider, server, port, login, password
    
    def get_service(self):
        
        provider, server, port, login, password = self.get_credentials()

        self.service = smtplib.SMTP(server, port)
        self.service.starttls()
        self.service.login(login, password)

        return self.service

    def send(self, message):

        if not self.service:
            self.get_service()
        try:
            self.service.send_message(message)
            return True, None
        except Exception as error:
            if session.debug:
                session.logger.error(f"Error: {error}\n\n")

            print("\nError: ", error)