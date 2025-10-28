from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pandas as pd
from email.utils import parsedate_to_datetime
import base64

# --- Load credentials ---
creds = Credentials.from_authorized_user_file("token.json")

# --- Connect to Gmail API ---
service = build('gmail', 'v1', credentials=creds)

# --- Get the 100 most recent emails ---
results = service.users().messages().list(
    userId='me',
    maxResults=100,
    labelIds=['INBOX']
).execute()
messages = results.get('messages', [])

email_data = []

if not messages:
    print("No messages found.")
else:
    for msg in messages:
        msg_id = msg['id']

        # Get full message data
        msg_detail = service.users().messages().get(
            userId='me', id=msg_id, format='full'
        ).execute()

        headers = msg_detail['payload']['headers']
        data = {'From': '', 'Subject': '', 'Date': '', 'Snippet': '', 'Body': ''}

        # Extract From, Subject, Date
        for header in headers:
            name = header['name']
            value = header['value']
            if name in data:
                data[name] = value

        # Add short snippet
        data['Snippet'] = msg_detail.get('snippet', '')

        # Extract plain text body (if available)
        def get_body(payload):
            body = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    body += get_body(part)
            else:
                data_b64 = payload.get('body', {}).get('data')
                if data_b64:
                    body += base64.urlsafe_b64decode(data_b64).decode('utf-8', errors='ignore')
            return body

        data['Body'] = get_body(msg_detail['payload'])

        # Format date
        try:
            data['Date'] = parsedate_to_datetime(data['Date']).strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

        email_data.append(data)

# --- Save to Excel ---
df = pd.DataFrame(email_data)
df.to_excel("gmail_emails_full.xlsx", index=False)

print("✅ Extracted 100 emails (with full body) saved to gmail_emails_full.xlsx")
