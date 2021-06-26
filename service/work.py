from __future__ import print_function
from main import db
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from models.gmail import get_mail

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def get_service():
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def store():
    engine = db.create_engine('sqlite:///user.db', echo=True)
    conn = engine.connect()
    result = get_mail('17a466be847c7eda')
    conn.execute('INSERT INTO mail(description,thId) VALUES(:description,:thId)',
                 (result['snippet']), result['threadId'])
    print("entered successfully")
    conn.close()


if __name__ == '__main__':
    store()
