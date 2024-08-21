import os.path
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def search_emails(service, query):
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    if not messages:
        print("No messages found.")
        return None
    else:
        print(f"Found {len(messages)} message(s).")
        return messages

def get_email_content(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = message['payload']
    return extract_message_body(payload)

def extract_message_body(payload):
    parts = payload.get('parts')
    if parts:
        for part in parts:
            mime_type = part.get('mimeType')
            if mime_type == 'text/plain':
                if 'data' in part['body']:
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
            elif mime_type == 'multipart/alternative':
                return extract_message_body(part)
    else:
        if 'data' in payload['body']:
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')

    return None
import webbrowser
def find_and_click_link(email_content):
    # print(email_content)
    urls = re.findall(r'Download<(\S+\.xlsx)>', email_content)
    if urls:
        print(f"Found URL: {urls[0]}")
        # Example: Open the link in a browser (ensure it's safe to do so)

        webbrowser.open(urls[0])
    else:
        print("No URL found in the email.")

def main():
    service = authenticate_gmail()
    emails = search_emails(service, "to:alexanderkwok125+zapier@gmail.com")
    if emails:
        for email in emails:
            content = get_email_content(service, email['id'])
            if content:
                find_and_click_link(content)
            else:
                print("No content found in the email.")

if __name__ == '__main__':
    main()
