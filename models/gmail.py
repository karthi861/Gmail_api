from __future__ import print_function
import os.path
import base64
import email
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

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


def get_email():
    service = get_service()
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])
    return messages


def get_mail(msg_id):
    service = get_service()
    results = service.users().messages().get(userId='me', id=msg_id).execute()
    msg_str = base64.urlsafe_b64decode(results['raw'])
    mime_msg = email.message_from_bytes(msg_str)
    data = {'to': mime_msg['To'], 'from': mime_msg['From'], 'date': mime_msg['Date'], 'subject': mime_msg['Subject']}
    return data


if __name__ == '__main__':
    get_mail('17a466be847c7eda')
