# WhatsApp Watcher Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **WhatsApp Watcher Skill** enables the AI Employee to monitor WhatsApp Web for urgent messages containing specific keywords and automatically create actionable task files.

---

## 🎯 Purpose

Monitor WhatsApp Web 24/7 using browser automation, detect urgent messages based on keywords, and create actionable Markdown files for AI processing.

---

## ⚡ Quick Start

```bash
# Start WhatsApp Watcher
python watchers/whatsapp_watcher.py AI_Employee_Vault

# Process messages with AI
qwen "Process all WhatsApp messages in Needs_Action. Draft replies for urgent ones." --approval-mode yolo
```

---

## 🔧 Configuration

### Setup Requirements

1. **Install Playwright:**
   ```bash
   npm install -D @playwright/test
   npx playwright install chromium
   ```

2. **Python Dependencies:**
   ```bash
   pip install playwright
   ```

3. **First Run:**
   - Run watcher script
   - Browser opens WhatsApp Web
   - Scan QR code with WhatsApp mobile app
   - Session saved automatically

---

## 📁 File Structure

```
AI_Employee_Vault/
├── watchers/
│   ├── whatsapp_watcher.py      # Main watcher script
│   └── whatsapp_session/        # Browser session (never commit!)
├── Needs_Action/
│   └── WHATSAPP_20260327_103000_ContactName.md  # New message files
└── Logs/
    └── 2026-03-27_WhatsAppWatcher.log  # Watcher logs
```

---

## 📥 Input

| Parameter | Type | Description |
|-----------|------|-------------|
| WhatsApp Web | Browser | Automated via Playwright |
| Check Interval | int | Seconds between checks (default: 30) |
| Keywords | list | Urgent keywords to detect |

### Default Urgent Keywords

```python
URGENT_KEYWORDS = [
    'urgent',
    'asap',
    'invoice',
    'payment',
    'help',
    'important',
    'deadline',
    'emergency',
    'call back',
    'reply soon'
]
```

---

## 📤 Output

Creates Markdown files in `/Needs_Action/`:

```markdown
---
type: whatsapp
chat: John Doe
received: 2026-03-27T10:30:00
priority: high
keywords: urgent, invoice
status: pending
---

# WhatsApp Message

## Details
- **From:** John Doe
- **Received:** 2026-03-27T10:30:00
- **Priority:** High (urgent keywords detected)
- **Keywords:** urgent, invoice

---

## Message Content

Hi, I need the invoice sent urgently. Payment is due today.

---

## Suggested Actions

- [ ] Read and understand message
- [ ] Determine urgency level
- [ ] Draft reply (if needed)
- [ ] Take required action
- [ ] Mark as read in WhatsApp
- [ ] Archive after processing

---
*Detected by WhatsApp Watcher at 2026-03-27T10:30:00*

## Urgent Keywords Detected
- urgent
- invoice
```

---

## 🎓 Usage Examples

### Example 1: Process All WhatsApp Messages

```bash
# Start watcher
python watchers/whatsapp_watcher.py AI_Employee_Vault &

# Process messages
qwen "Process all WHATSAPP_*.md files. 
For messages with 'invoice' or 'payment':
1. Create approval request
2. Draft response
3. Move to Done" --approval-mode yolo
```

### Example 2: Urgent Message Handling

```bash
qwen "Find WhatsApp messages with priority: high.
These need immediate response. Draft replies now." --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. WhatsApp Watcher runs every 30 sec   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Opens WhatsApp Web (headless)        │
│    Uses saved session if available      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. Scans chat list for unread messages  │
│    Checks for urgent keywords           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. For each urgent message:             │
│    - Extract chat name                  │
│    - Extract message text               │
│    - Match keywords                     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 5. Creates action file                  │
│    WHATSAPP_timestamp_chat.md           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 6. AI processes message                 │
│    - Drafts reply                       │
│    - Takes action                       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 7. Moves to Done after processing       │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **Session privacy** | `whatsapp_session/` contains login - never commit |
| **Add to .gitignore** | `watchers/whatsapp_session/*` |
| **Local only** | Session never synced to cloud |
| **WhatsApp ToS** | Be aware of WhatsApp terms of service |

---

## 🛠️ Troubleshooting

### Issue: "QR code not scanned"

**Solution:**
- Keep browser window open during first run
- Scan QR code within 60 seconds
- Check internet connection

### Issue: "No messages detected"

**Solution:**
- Ensure WhatsApp Web is logged in
- Check if messages contain urgent keywords
- Review logs in `Logs/` folder

### Issue: "Browser crashes"

**Solution:**
```bash
# Reinstall Playwright
npx playwright install chromium --force
```

---

## 📊 Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **Response Drafting** | Draft WhatsApp replies |
| **HITL Approval** | Approval for sensitive responses |
| **Daily Briefing** | Summarize WhatsApp messages |

---

## ✅ Testing Checklist

- [ ] Playwright installed
- [ ] Chromium browser installed
- [ ] First run QR code scanned
- [ ] Session saved
- [ ] Send test WhatsApp message with "urgent"
- [ ] Watcher detects message
- [ ] Action file created
- [ ] AI processes message
- [ ] Moved to Done

---

*WhatsApp Watcher Skill v1.0 - Silver Tier*
