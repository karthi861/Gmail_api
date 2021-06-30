from __future__ import print_function

import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from models.gmail import get_service

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def all_labels():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


def create_label():
    service = get_service()
    label = {
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
        "name": "imp"
    }
    results = service.users().labels().create(userId='me', body=label).execute()
    print(results)


def move_msg_to_label():
    rules = json.load(open('rules.json'))
    for rule in rules["rule1"]['fields']:
        print(rule['name'], rule['value'])
    service = get_service()
    service.users().messages().modify(userId='me', id='17a46732ac59fcb9',
                                      body={'removeLabelIds': ['STARRED']}).execute()


if __name__ == '__main__':
    move_msg_to_label()
# all_labels()
