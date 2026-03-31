#!/usr/bin/env python3
"""Gmail Auth - Get SEND Permission"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

CREDENTIALS_FILE = Path(__file__).parent / "AI_Employee_Vault" / "watchers" / "credentials.json"
TOKEN_FILE = Path(__file__).parent / "gmail_send_token.json"

# Scopes for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

print("\n📧 Gmail API - SEND Permission")
print("=" * 60)

if not CREDENTIALS_FILE.exists():
    print("\n❌ credentials.json not found!")
    exit(1)

print(f"\n✅ Found: {CREDENTIALS_FILE}")

print("\n🔐 Starting OAuth flow...")
flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)

# Save token
TOKEN_FILE.write_text(creds.to_json())
print(f"\n✅ Token saved: {TOKEN_FILE}")

print("\n🎉 SUCCESS! Now you can send emails!")
print("\nRun:")
print("  python gmail_reply_api.py")

input("\nPress Enter to exit...")
