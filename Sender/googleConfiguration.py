import os

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from settings import TOKEN_PATH, CLIENT_SECRET_FILE

SCOPES = {
    "ACTION_COMPOSE": "https://www.googleapis.com/auth/gmail.addons.current.action.compose",
    "MESSAGE_ACTION": "https://www.googleapis.com/auth/gmail.addons.current.message.action",
    "MESSAGE_METDATA": "https://www.googleapis.com/auth/gmail.addons.current.message.metadata",
    "MESSAGE_READONLY": "https://www.googleapis.com/auth/gmail.addons.current.message.readonly",
    "LABELS": "https://www.googleapis.com/auth/gmail.labels",
    "SEND": "https://www.googleapis.com/auth/gmail.send",
    "READONLY": "https://www.googleapis.com/auth/gmail.readonly",
    "COMPOSE": "https://www.googleapis.com/auth/gmail.compose",
    "INSERT": "https://www.googleapis.com/auth/gmail.insert",
    "MODIFY": "https://www.googleapis.com/auth/gmail.modify",
    "METADATA": "https://www.googleapis.com/auth/gmail.metadata",
    "SETTINGS_BASIC": "https://www.googleapis.com/auth/gmail.settings.basic",
    "SETTINGS_SHARING": "https://www.googleapis.com/auth/gmail.settings.sharing",
    "DELETE_PERMANENT": "https://mail.google.com/"
}

class Configure():

    def __init__(self, scope='SEND'):

        self.scope = [SCOPES[scope]]

    def get_credentials(self):
        """Get credentials for the user"""
        creds = ''
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, self.scope)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, self.scope)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_service(self):

        credentials = self.get_credentials()
        service = build('gmail', 'v1', credentials=credentials)

        return service