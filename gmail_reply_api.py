#!/usr/bin/env python3
"""Gmail Auto-Reply - Direct Gmail API (No Browser Automation)"""

from pathlib import Path
import base64
from email.mime.text import MIMEText
import time

# Gmail API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    print("❌ Gmail API not installed!")
    print("\nInstall with:")
    print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    exit(1)

VAULT_PATH = Path(__file__).parent / "AI_Employee_Vault"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
DONE_FOLDER = VAULT_PATH / "Done"
SESSION_FILE = Path(__file__).parent / "gmail_send_token.json"
CREDENTIALS_FILE = VAULT_PATH / "watchers" / "credentials.json"

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def find_latest_email():
    """Find latest email in Needs_Action"""
    email_files = list(NEEDS_ACTION.glob("EMAIL_*.md"))
    if not email_files:
        return None
    return sorted(email_files)[-1]

def extract_email_data(content):
    """Extract email fields from markdown"""
    data = {}
    for line in content.split('\n'):
        if ':' in line and not line.startswith('#'):
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value = parts[1].strip()
                if key in ['from', 'to', 'subject', 'email_id', 'received']:
                    data[key] = value
    return data

def generate_reply(email_data):
    """Generate reply content"""
    subject = email_data.get('subject', 'No Subject')
    from_email = email_data.get('from', 'Unknown')
    email_id = email_data.get('email_id', 'unknown')
    
    reply_subject = f"Re: {subject}" if not subject.startswith("Re:") else subject
    
    reply_body = f"""Hi,

Thank you for your email. This is an automated response from the AI Employee system.

Your email has been received and processed successfully.

Email ID: {email_id}
Processed at: {time.strftime("%Y-%m-%d %H:%M:%S")}

Best regards,
AI Employee"""
    
    return reply_subject, reply_body

def get_gmail_service():
    """Authenticate and get Gmail service"""
    creds = None
    
    # Load existing token
    if SESSION_FILE.exists():
        creds = Credentials.from_authorized_user_file(SESSION_FILE, SCOPES)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print("\n❌ credentials.json not found!")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Save token
            SESSION_FILE.write_text(creds.to_json())
            print("✅ Credentials saved!")
    
    return build('gmail', 'v1', credentials=creds)

def send_reply(email_file):
    """Send Gmail reply using Gmail API"""
    
    # Read email data
    email_content = email_file.read_text(encoding='utf-8')
    email_data = extract_email_data(email_content)
    
    print(f"\n📧 Processing email from: {email_data.get('from', 'Unknown')}")
    print(f"📝 Subject: {email_data.get('subject', 'No Subject')}")
    
    # Generate reply
    reply_subject, reply_body = generate_reply(email_data)
    
    print(f"\n📝 Reply Subject: {reply_subject}")
    print(f"📝 Reply Body: {reply_body[:100]}...")
    
    # Get Gmail service
    print("\n🔐 Authenticating with Gmail API...")
    service = get_gmail_service()
    
    if not service:
        print("\n❌ Authentication failed!")
        return False
    
    print("✅ Authenticated!")
    
    # Extract recipient email
    to_email = email_data.get('from', '')
    if '<' in to_email and '>' in to_email:
        to_email = to_email.split('<')[1].split('>')[0]
    
    # Create message
    print(f"\n📤 Sending reply to: {to_email}")
    message = MIMEText(reply_body)
    message['to'] = to_email
    message['subject'] = reply_subject
    
    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    try:
        # Send via Gmail API
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"\n✅ EMAIL SENT!")
        print(f"   Message ID: {sent_message['id']}")
        print(f"   Thread ID: {sent_message['threadId']}")
        
        # Move email to Done
        print(f"\n📁 Moving email to Done folder...")
        DONE_FOLDER.mkdir(parents=True, exist_ok=True)
        email_file.rename(DONE_FOLDER / email_file.name)
        print(f"   ✅ Moved: {email_file.name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📧 GMAIL AUTO-REPLY (Direct API)")
    print("=" * 60)
    
    if not GMAIL_AVAILABLE:
        print("\n❌ Gmail API not installed!")
        print("\nInstall:")
        print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        input("\nPress Enter to exit...")
        exit(1)
    
    # Find latest email
    email_file = find_latest_email()
    
    if not email_file:
        print("\n❌ No emails found in Needs_Action!")
        print("\nRun Gmail Watcher:")
        print("  python AI_Employee_Vault/watchers/gmail_watcher.py AI_Employee_Vault")
        input("\nPress Enter to exit...")
        exit(1)
    
    # Send reply
    success = send_reply(email_file)
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 GMAIL REPLY SENT SUCCESSFULLY!")
        print("=" * 60)
    else:
        print("\n⚠️  Reply not sent. Check errors above.")
    
    input("\nPress Enter to exit...")
