from abc import ABC, abstractmethod

class AbstractESP(ABC):
    """
    Abstract class for service provider
    """

    def __init__(self):
        pass
    
    # get the user credentials send the messages
    @abstractmethod
    def get_credentials(self):
        pass
    
    # get the actual instance which will send the email
    @abstractmethod
    def get_service(self):
        pass

    # it sends the actual message
    @abstractmethod
    def send(self):
        pass

class AbstractSender(ABC):
    """
    Abstract class for sender
    """
    
    def __init__(self, data_files, config, provider):
        pass
    
    # read the data file single time for all the instances
    @staticmethod
    def read_file(file):
        pass

    # single mail sending functionality
    @abstractmethod
    def send_single_mail(self, message):
        pass
    
    # successfull and failed email logs
    @abstractmethod
    def email_logs(self, data, fileName):
        pass
    
    # insert all the variables in the email body from the data row
    @abstractmethod
    def format_email_body(self, body_content, row):
        pass
    
    # attach any files
    @abstractmethod
    def attach(self, message):
        pass
    
    # calls the send_single_mail for each row after formatting the message properly
    @abstractmethod
    def send_bulk_email(self, **kwargs):
        pass

class AbstractSession(ABC):

    """Abstract class for session"""

    def __init__(self):
        pass

    # load the session variables 
    @abstractmethod
    def load(self):
        pass

    # debug logger
    @abstractmethod
    def setup_logger(self):
        pass

    # refresh the session
    @abstractmethod
    def refresh(self):
        pass
