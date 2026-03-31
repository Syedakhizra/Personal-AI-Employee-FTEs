# Gmail Watcher Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Gmail Watcher Skill** enables the AI Employee to monitor Gmail for new important/unread emails and automatically create actionable task files for processing.

---

## 🎯 Purpose

Monitor Gmail inbox 24/7 and convert new emails into actionable Markdown files that the AI can process, draft replies for, and take actions on.

---

## ⚡ Quick Start

```bash
# Start Gmail Watcher
python watchers/gmail_watcher.py AI_Employee_Vault

# Process new emails with AI
qwen "Process all new emails in Needs_Action folder. Draft replies for urgent ones." --approval-mode yolo
```

---

## 🔧 Configuration

### Setup Requirements

1. **Enable Gmail API:**
   - Go to https://console.cloud.google.com/
   - Create new project or select existing
   - Enable "Gmail API"

2. **Create OAuth Credentials:**
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: "Other"
   - Download `credentials.json`

3. **Install Dependencies:**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

4. **Place Credentials:**
   - Copy `credentials.json` to `AI_Employee_Vault/watchers/credentials.json`

5. **First Run Authorization:**
   - Run watcher script
   - Browser will open for OAuth authorization
   - Sign in with Gmail account
   - Grant permissions
   - Token saved automatically

---

## 📁 File Structure

```
AI_Employee_Vault/
├── watchers/
│   ├── gmail_watcher.py       # Main watcher script
│   ├── credentials.json       # OAuth credentials (never commit!)
│   └── token.json            # Auth token (auto-generated, never commit!)
├── Needs_Action/
│   └── EMAIL_20260327_103000_Invoice_Payment.md  # New email action files
└── Logs/
    └── 2026-03-27_GmailWatcher.log  # Watcher logs
```

---

## 📥 Input

| Parameter | Type | Description |
|-----------|------|-------------|
| Gmail API | OAuth 2.0 | Authenticated Gmail access |
| Check Interval | int | Seconds between checks (default: 120) |
| Filter | string | Gmail query (default: `is:unread -in:chats`) |

---

## 📤 Output

Creates Markdown files in `/Needs_Action/`:

```markdown
---
type: email
from: client@example.com
to: me@company.com
subject: Invoice Payment Required
received: 2026-03-27T10:30:00
email_date: Fri, 27 Mar 2026 10:25:00 +0500
priority: high
status: pending
email_id: 18f4a2b3c4d5e6f7
---

# Email

## Headers
- **From:** client@example.com
- **To:** me@company.com
- **Subject:** Invoice Payment Required
- **Date:** Fri, 27 Mar 2026 10:25:00 +0500

---

## Content

Dear Team,

Please find attached the invoice for services rendered...

---

## Suggested Actions

- [ ] Read and understand email
- [ ] Draft reply (if needed)
- [ ] Take required action
- [ ] Archive after processing

---
*Detected by Gmail Watcher at 2026-03-27T10:30:00*
```

---

## 🎓 Usage Examples

### Example 1: Process All New Emails

```bash
# Start watcher in background
python watchers/gmail_watcher.py AI_Employee_Vault &

# Process emails with AI
qwen "Process all EMAIL_*.md files in Needs_Action. 
For each email:
1. Read and categorize
2. Draft reply if response needed
3. Create approval request for sensitive actions
4. Move to Done when complete" --approval-mode yolo
```

### Example 2: Urgent Email Handling

```bash
# AI processes only high priority emails
qwen "Find all emails with priority: high in Needs_Action.
Draft urgent replies and flag for immediate attention." --approval-mode yolo
```

### Example 3: Email + Approval Workflow

```bash
# Process email requiring payment approval
qwen "Process EMAIL_Invoice_Payment.md.
This requires approval before sending payment.
Create approval request in Pending_Approval folder." --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. Gmail Watcher runs every 2 minutes                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Checks Gmail API for: is:unread -in:chats            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. For each new email:                                  │
│    - Fetch full content                                 │
│    - Extract headers (From, To, Subject, Date)          │
│    - Detect urgent keywords                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Creates action file in /Needs_Action/                │
│    EMAIL_YYYYMMDD_HHMMSS_Subject.md                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 5. AI Employee processes the email                      │
│    - Categorizes                                        │
│    - Drafts reply                                       │
│    - Creates approval if needed                         │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Moves to /Done/ after processing                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🏷️ Priority Detection

Emails are automatically categorized by priority:

| Priority | Keywords |
|----------|----------|
| **High** | urgent, asap, invoice, payment, important, deadline, emergency |
| **Normal** | All other emails |

---

## ⚙️ Customization

### Change Check Interval

```python
# In gmail_watcher.py main():
watcher = GmailWatcher(str(vault_path), check_interval=60)  # Check every 60 seconds
```

### Modify Email Filter

```python
# In check_for_updates():
results = self.service.users().messages().list(
    userId='me',
    q='is:unread from:important@client.com',  # Custom filter
    maxResults=10
).execute()
```

### Add Custom Keywords

```python
# In create_action_file():
urgent_keywords = ['urgent', 'asap', 'invoice', 'payment', 
                   'your_keyword', 'another_keyword']
```

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **Never commit** | `credentials.json` and `token.json` |
| **Add to .gitignore** | `watchers/credentials.json`, `watchers/token.json` |
| **Read-only scope** | Uses `gmail.readonly` - cannot send emails |
| **Local storage** | All data stored locally, not synced to cloud |

---

## 🛠️ Troubleshooting

### Issue: "credentials.json not found"

**Solution:**
```bash
# Download from Google Cloud Console
# Save to: AI_Employee_Vault/watchers/credentials.json
```

### Issue: "Token expired"

**Solution:**
```bash
# Delete old token
del watchers/token.json

# Re-run watcher to re-authorize
python watchers/gmail_watcher.py AI_Employee_Vault
```

### Issue: "No emails detected"

**Solution:**
- Check Gmail filter in code
- Verify OAuth permissions
- Check Gmail API quota
- Review watcher logs in `Logs/` folder

---

## 📊 Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **Email MCP** | Send replies via Gmail API |
| **HITL Approval** | Require approval before sending sensitive emails |
| **Task Planning** | Create multi-step plans for complex email tasks |
| **Daily Briefing** | Summarize emails processed today |

---

## ✅ Testing Checklist

- [ ] Gmail API enabled
- [ ] OAuth credentials downloaded
- [ ] Dependencies installed
- [ ] First run authorization complete
- [ ] Token file created
- [ ] Test email sent to Gmail
- [ ] Watcher detects email
- [ ] Action file created in Needs_Action
- [ ] AI processes email
- [ ] Email moved to Done

---

## 📚 Related Documents

- [[Agent_Skills_Silver_Tier]] - Full Silver Tier skills list
- [[Company_Handbook]] - Email response guidelines
- [[Dashboard]] - Monitor email processing status

---

## 🚀 Next Steps

After implementing Gmail Watcher:

1. **WhatsApp Watcher** - Monitor WhatsApp Web
2. **Email MCP** - Send emails via MCP server
3. **HITL Approval** - Approval workflow for sensitive emails
4. **Daily Briefing** - Email summary reports

---

*Gmail Watcher Skill v1.0 - Silver Tier*
*Part of Personal AI Employee Hackathon 0*
