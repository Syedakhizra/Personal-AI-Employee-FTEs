#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail Watcher - Silver Tier
Monitors Gmail for new important/unread emails and creates action files.

Usage:
    python gmail_watcher.py /path/to/vault

Requirements:
    - credentials.json in watchers/ folder
    - google-api-python-client installed
"""

import os
import sys
import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher, sanitize_filename

# Gmail API imports
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    GMAIL_AVAILABLE = True
except ImportError as e:
    GMAIL_AVAILABLE = False
    print(f"Error: Gmail API not available - {e}")
    print("Install with: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")


class GmailWatcher(BaseWatcher):
    """Monitor Gmail for new important/unread emails."""

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, vault_path: str, check_interval: int = 120):
        """
        Initialize Gmail Watcher.
        
        Args:
            vault_path: Path to Obsidian vault
            check_interval: Seconds between checks (default: 2 minutes)
        """
        super().__init__(vault_path, check_interval)
        
        if not GMAIL_AVAILABLE:
            self.logger.error("Gmail API not available")
            self.service = None
            return
        
        # OAuth credentials paths
        self.watchers_dir = self.vault_path / 'watchers'
        self.credentials_path = self.watchers_dir / 'credentials.json'
        self.token_path = self.watchers_dir / 'token.json'
        
        # Authenticate and build service
        self.service = self._authenticate()
        self.processed_ids: set = set()
        
        self.logger.info(f"Gmail Watcher initialized. Interval: {check_interval}s")

    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None
        
        # Load existing token
        if self.token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
                self.logger.info("Loaded existing credentials")
            except Exception as e:
                self.logger.warning(f"Could not load token: {e}")
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.logger.info("Refreshed credentials")
                except Exception as e:
                    self.logger.error(f"Could not refresh: {e}")
                    return None
            else:
                if not self.credentials_path.exists():
                    self.logger.error(f"credentials.json not found at {self.credentials_path}")
                    return None
                
                try:
                    self.logger.info("Starting OAuth flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES)
                    creds = flow.run_local_server(port=0, open_browser=True)
                    
                    # Save token
                    self.token_path.write_text(creds.to_json())
                    self.logger.info(f"Saved token to {self.token_path}")
                except Exception as e:
                    self.logger.error(f"OAuth failed: {e}")
                    return None
        
        try:
            service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Gmail service initialized")
            return service
        except Exception as e:
            self.logger.error(f"Could not build service: {e}")
            return None

    def _get_email_content(self, msg_id: str) -> Dict[str, Any]:
        """Fetch full email content."""
        try:
            message = self.service.users().messages().get(
                userId='me', id=msg_id, format='full'
            ).execute()
            
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            
            # Get body
            body = ''
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        break
            
            return {
                'id': msg_id,
                'from': headers.get('From', 'Unknown'),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', 'No Subject'),
                'date': headers.get('Date', ''),
                'body': body,
                'snippet': message.get('snippet', ''),
            }
        except Exception as e:
            self.logger.error(f"Error fetching email: {e}")
            return {
                'id': msg_id,
                'from': 'Unknown',
                'subject': 'Error fetching',
                'body': str(e),
            }

    def check_for_updates(self) -> list:
        """Check for new unread emails."""
        if not self.service:
            return []
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread -in:chats',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            new_emails = []
            
            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    self.logger.info(f"New email: {msg['id']}")
                    new_emails.append({'id': msg['id']})
            
            return new_emails
        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []

    def create_action_file(self, item) -> Path:
        """Create action file for email."""
        email_id = item['id']
        email_data = self._get_email_content(email_id)
        
        safe_subject = sanitize_filename(email_data['subject'][:50])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        action_file = self.needs_action / f'EMAIL_{timestamp}_{safe_subject}.md'
        
        # Detect priority
        text = (email_data['subject'] + ' ' + email_data['body']).lower()
        urgent = ['urgent', 'asap', 'invoice', 'payment', 'important', 'deadline']
        priority = 'high' if any(kw in text for kw in urgent) else 'normal'
        
        content = f'''---
type: email
from: {email_data['from']}
to: {email_data['to']}
subject: {email_data['subject']}
received: {datetime.now().isoformat()}
email_date: {email_data['date']}
priority: {priority}
status: pending
email_id: {email_id}
---

# Email

## Headers
- **From:** {email_data['from']}
- **To:** {email_data['to']}
- **Subject:** {email_data['subject']}
- **Date:** {email_data['date']}

---

## Content

{email_data['body'] if email_data['body'] else email_data['snippet']}

---

## Suggested Actions

- [ ] Read and understand email
- [ ] Draft reply (if needed)
- [ ] Take required action
- [ ] Archive after processing

---
*Detected by Gmail Watcher at {datetime.now().isoformat()}*
'''
        
        action_file.write_text(content, encoding='utf-8')
        self.processed_ids.add(email_id)
        
        self.logger.info(f"Created: {action_file.name}")
        return action_file


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        vault_path = Path(__file__).parent.parent
    else:
        vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        print(f"Error: Vault not found: {vault_path}")
        sys.exit(1)
    
    if not GMAIL_AVAILABLE:
        print("Error: Install Gmail API dependencies")
        sys.exit(1)
    
    watcher = GmailWatcher(str(vault_path), check_interval=120)
    
    if not watcher.service:
        print("Error: Could not initialize Gmail service")
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print("Gmail Watcher Started (Silver Tier)")
    print(f"{'='*50}")
    print(f"Vault: {vault_path}")
    print(f"Check Interval: 120 seconds")
    print(f"Output: {watcher.needs_action}")
    print(f"\nPress Ctrl+C to stop.\n")
    
    watcher.run()


if __name__ == "__main__":
    main()
