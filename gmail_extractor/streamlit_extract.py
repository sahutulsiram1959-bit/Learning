import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd
from email.utils import parsedate_to_datetime
import tempfile
import os

st.set_page_config(page_title="📧 Gmail Extractor", page_icon="📩", layout="centered")
st.title("📩 Gmail Email Extractor")

st.write("Upload your **Gmail API token.json** file to extract email details safely using Google API.")

# Upload token
token_file = st.file_uploader("Upload your token.json", type=["json"])

if token_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_file:
        tmp_file.write(token_file.read())
        token_path = tmp_file.name

    creds = Credentials.from_authorized_user_file(token_path)
    service = build('gmail', 'v1', credentials=creds)

    max_emails = st.number_input("Number of emails to extract", min_value=10, max_value=500, step=10, value=100)

    if st.button("Extract Emails"):
        st.info("⏳ Extracting emails... please wait")

        results = service.users().messages().list(userId='me', maxResults=max_emails, labelIds=['INBOX']).execute()
        messages = results.get('messages', [])

        email_data = []

        for msg in messages:
            msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='metadata',
                                                        metadataHeaders=['From', 'Subject', 'Date']).execute()

            headers = msg_detail['payload']['headers']
            data = {'From': '', 'Subject': '', 'Date': ''}
            for header in headers:
                if header['name'] in data:
                    data[header['name']] = header['value']

            try:
                data['Date'] = parsedate_to_datetime(data['Date']).strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

            data['Snippet'] = msg_detail.get('snippet', '')
            email_data.append(data)

        df = pd.DataFrame(email_data)
        excel_path = "gmail_emails.xlsx"
        df.to_excel(excel_path, index=False)

        st.success("✅ Emails extracted successfully!")
        st.dataframe(df.head())

        with open(excel_path, "rb") as file:
            st.download_button(
                label="📥 Download Excel File",
                data=file,
                file_name="gmail_emails.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
else:
    st.warning("⚠️ Please upload your token.json first.")
