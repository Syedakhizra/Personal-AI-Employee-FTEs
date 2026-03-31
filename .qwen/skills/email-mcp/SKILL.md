# Email MCP Integration Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Email MCP Integration Skill** enables the AI Employee to send emails via Gmail using Model Context Protocol (MCP) server for external action.

---

## 🎯 Purpose

Send, draft, and manage emails through MCP server integration, with human-in-the-loop approval for sensitive actions.

---

## ⚡ Quick Start

```bash
# Send email directly
qwen "Send email to client@example.com with subject 'Invoice Attached'" --approval-mode yolo

# Draft for approval
qwen "Draft email to team about project update. Save to Pending_Approval" --approval-mode yolo
```

---

## 🔧 Configuration

### MCP Server Setup

1. **Install Email MCP:**
   ```bash
   npm install -g @modelcontextprotocol/server-email
   ```

2. **Configure MCP:**
   ```json
   ~/.config/claude-code/mcp.json
   {
     "mcpServers": {
       "email": {
         "command": "email-mcp",
         "env": {
           "GMAIL_API_KEY": "your-api-key",
           "SMTP_HOST": "smtp.gmail.com",
           "SMTP_PORT": "587"
         }
       }
     }
   }
   ```

3. **Gmail API Setup:**
   - Enable Gmail API
   - Create service account
   - Download credentials

---

## 📥 Available Actions

| Action | Description | Approval Required |
|--------|-------------|-------------------|
| `send_email` | Send email immediately | Yes (new recipients) |
| `draft_email` | Create draft without sending | No |
| `search_emails` | Search inbox | No |
| `reply_email` | Reply to existing email | Yes |
| `forward_email` | Forward email | Yes |

---

## 🎓 Usage Examples

### Example 1: Send Email

```bash
qwen "Send email using Email MCP:
To: client@example.com
Subject: Invoice #123 Attached
Body: Dear Client, Please find attached invoice...
Attachment: /Invoices/invoice_123.pdf" --approval-mode yolo
```

### Example 2: Draft Email

```bash
qwen "Draft email for approval:
To: team@company.com
Subject: Weekly Update
Body: Here's this week's progress...
Save to Pending_Approval folder" --approval-mode yolo
```

### Example 3: Search Emails

```bash
qwen "Search emails from last week containing 'invoice'
Summarize results" --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. AI receives email task               │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Check if approval required           │
│    - Known contact = Auto               │
│    - New contact = Approval             │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│ Auto-approve  │       │ Create        │
│ Send via MCP  │       │ Approval File │
└───────────────┘       └───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ Human approves│
                        │ (moves file)  │
                        └───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ Send via MCP  │
                        └───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ Log & Done    │
                        └───────────────┘
```

---

## 📊 Approval Thresholds

| Action Type | Auto-Approve | Require Approval |
|-------------|--------------|------------------|
| Reply to known contact | ✅ Yes | ❌ No |
| Reply to new contact | ❌ No | ✅ Yes |
| Send attachment | ❌ No | ✅ Yes |
| Forward email | ❌ No | ✅ Yes |
| Internal team email | ✅ Yes | ❌ No |
| External client email | ❌ No | ✅ Yes |

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **API keys** | Never commit credentials |
| **Approval for external** | Always approve external emails |
| **Log all sent** | Keep audit trail |
| **No auto-payment** | Never send payment auto-approve |

---

## 🛠️ Troubleshooting

### Issue: "MCP server not connected"

**Solution:**
```bash
# Check MCP configuration
cat ~/.config/claude-code/mcp.json

# Restart MCP server
email-mcp --restart
```

### Issue: "Authentication failed"

**Solution:**
- Verify Gmail API credentials
- Check service account permissions
- Review MCP logs

---

## ✅ Testing Checklist

- [ ] MCP server installed
- [ ] Configuration complete
- [ ] Test email drafted
- [ ] Test email sent
- [ ] Approval workflow works
- [ ] Logs created

---

*Email MCP Integration Skill v1.0 - Silver Tier*
