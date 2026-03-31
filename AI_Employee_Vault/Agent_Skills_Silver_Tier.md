---
version: 0.2
tier: silver
last_updated: 2026-03-27
---

# Agent Skills - Silver Tier

This document defines the **Agent Skills** for the AI Employee - Silver Tier capabilities.
Silver Tier adds: **Multiple Watchers, Social Media Posting, MCP Integration, HITL Approval, and Scheduling**.

---

## 📚 Bronze Tier Skills (Already Implemented)

| # | Skill | Status |
|---|-------|--------|
| 1 | File Processing | ✅ Complete |
| 2 | Task Planning | ✅ Complete |
| 3 | Approval Request | ✅ Complete |
| 4 | Dashboard Update | ✅ Complete |
| 5 | Log Entry | ✅ Complete |
| 6 | File Categorization | ✅ Complete |
| 7 | Response Drafting | ✅ Complete |
| 8 | Daily Briefing | ✅ Complete |

---

## 🆕 Silver Tier Skills (New)

### 9. Gmail Watcher Skill

**Purpose:** Monitor Gmail for new important/unread emails and create action files.

**Trigger:** Every 2 minutes (configurable)

**Input:**
- Gmail API credentials
- Filter: `is:unread is:important`

**Output:** Creates `.md` file in `/Needs_Action/EMAIL_{message_id}.md`

**Template:**
```markdown
---
type: email
from: sender@example.com
subject: Email Subject
received: 2026-03-27T10:30:00
priority: high
status: pending
---

## Email Content

{email body text}

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
```

**Usage with Qwen Code:**
```bash
# Start Gmail Watcher
python AI_Employee_Vault/watchers/gmail_watcher.py AI_Employee_Vault

# Process new emails
qwen "Process all emails in Needs_Action folder. Draft replies for urgent ones." --approval-mode yolo
```

**Setup Requirements:**
1. Enable Gmail API
2. Create OAuth credentials
3. Store in `.env` (never commit!)

---

### 10. WhatsApp Watcher Skill

**Purpose:** Monitor WhatsApp Web for urgent messages containing keywords.

**Trigger:** Every 30 seconds (configurable)

**Keywords:** `['urgent', 'asap', 'invoice', 'payment', 'help']`

**Output:** Creates `.md` file in `/Needs_Action/WHATSAPP_{chat_id}_{timestamp}.md`

**Template:**
```markdown
---
type: whatsapp
chat: Contact Name
received: 2026-03-27T10:30:00
priority: high
keywords: ['urgent', 'invoice']
status: pending
---

## WhatsApp Message

{message text}

## Suggested Actions
- [ ] Reply via WhatsApp
- [ ] Take action on request
- [ ] Archive after processing
```

**Usage with Qwen Code:**
```bash
# Start WhatsApp Watcher (requires browser session)
python AI_Employee_Vault/watchers/whatsapp_watcher.py AI_Employee_Vault

# Process messages
qwen "Process WhatsApp messages. Draft replies for urgent ones." --approval-mode yolo
```

**Setup Requirements:**
1. Install Playwright: `npm install -D @playwright/test`
2. Run: `playwright install chromium`
3. Session stored in `/watchers/whatsapp_session/`

---

### 11. LinkedIn Post Creator Skill

**Purpose:** Automatically create and schedule LinkedIn posts for business promotion.

**Trigger:** Scheduled (daily/weekly) or on-demand

**Output:** Creates draft post in `/Social_Media/LinkedIn_Drafts/`

**Template:**
```markdown
---
type: linkedin_post
topic: Business Update
created: 2026-03-27T10:30:00
status: draft
scheduled_for: 2026-03-28T09:00:00
---

# LinkedIn Post Draft

## Content

🚀 Exciting update from our company!

We're helping businesses automate their workflows with AI-powered solutions.

#AI #Automation #Business #Technology

---
*Drafted by AI Employee - Requires approval before posting*

## To Approve
Move this file to /Approved/Social_Media/ folder.

## To Reject
Move this file to /Rejected/ folder.
```

**Usage with Qwen Code:**
```bash
# Generate LinkedIn post
qwen "Create a LinkedIn post about our AI Employee project. 
Focus on automation benefits. Keep it professional and engaging." --approval-mode yolo

# Post after approval (via MCP)
qwen "Post the approved LinkedIn content" --approval-mode yolo
```

---

### 12. Email MCP Integration Skill

**Purpose:** Send emails via Gmail using MCP server.

**Trigger:** Approved email draft in `/Approved/Email/`

**MCP Server:** `email-mcp` (Node.js/Python)

**Actions:**
- `send_email(to, subject, body, attachments?)`
- `draft_email(to, subject, body)`
- `search_emails(query, limit)`

**Configuration:**
```json
// ~/.config/claude-code/mcp.json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_API_KEY": "your-key"
      }
    }
  }
}
```

**Usage with Qwen Code:**
```bash
# Send email directly
qwen "Send email to client@example.com with subject 'Invoice Attached' 
and attach the invoice from Needs_Action folder" --approval-mode yolo

# Draft for approval
qwen "Draft email to team about project update. Save to Pending_Approval" --approval-mode yolo
```

---

### 13. Browser MCP Integration Skill

**Purpose:** Automate browser actions (login, fill forms, click buttons) via MCP.

**Trigger:** Task requiring web interaction

**MCP Server:** `@anthropic/browser-mcp` or `playwright-mcp`

**Actions:**
- `browser_navigate(url)`
- `browser_click(selector)`
- `browser_type(selector, text)`
- `browser_snapshot()`
- `browser_fill_form(fields)`

**Usage with Qwen Code:**
```bash
# Login to portal
qwen "Navigate to https://portal.example.com, login with credentials, 
and download the latest report" --approval-mode yolo

# Fill payment form (requires approval first!)
qwen "Fill payment form for invoice #123. Stop before submit for approval." --approval-mode yolo
```

**Security Note:** Never auto-approve payment submissions. Always require HITL approval.

---

### 14. Human-in-the-Loop (HITL) Approval Skill

**Purpose:** Require human approval for sensitive actions before execution.

**Trigger:** Actions matching approval rules (see Company_Handbook.md)

**Approval Thresholds:**

| Action Type | Auto-Approve | Require Approval |
|-------------|--------------|------------------|
| Email replies | Known contacts | New recipients |
| Social media | Scheduled posts | Replies, DMs |
| Payments | None | All payments |
| File operations | Internal folders | External sharing |

**Output:** Creates file in `/Pending_Approval/`

**Template:**
```markdown
---
type: approval_request
action: email_send
created: 2026-03-27T10:30:00
priority: high
status: pending
---

# Approval Required

## Action Details
- **Action:** Send Email
- **To:** client@example.com
- **Subject:** Invoice #123 Attached
- **Reason:** Client requested invoice

## Content Preview

Dear Client,

Please find attached invoice #123 for services rendered.

Best regards,
AI Employee

---

## To Approve
Move this file to `/Approved/` folder.

## To Reject
Move this file to `/Rejected/` folder.

## Deadline
Please respond within 24 hours.
```

**Workflow:**
```
1. AI detects action requiring approval
2. Creates file in /Pending_Approval/
3. Human reviews and moves to /Approved/ or /Rejected/
4. Orchestrator detects approved file
5. Executes action via MCP
6. Moves to /Done/ and logs
```

**Usage with Qwen Code:**
```bash
# Create approval request
qwen "This email requires approval. Create approval request in Pending_Approval 
with all details and clear approve/reject instructions" --approval-mode yolo

# Execute approved action
qwen "Execute all approved actions in Approved folder" --approval-mode yolo
```

---

### 15. Task Scheduler Skill

**Purpose:** Schedule recurring tasks via Windows Task Scheduler or cron.

**Trigger:** Time-based (daily, weekly, monthly)

**Scheduled Tasks:**

| Task | Frequency | Time |
|------|-----------|------|
| Gmail check | Every 2 min | Continuous |
| WhatsApp check | Every 30 sec | Continuous |
| LinkedIn post | Weekly | Monday 9 AM |
| Daily briefing | Daily | 6 PM |
| Dashboard update | Hourly | Every hour |

**Setup Commands:**

**Windows Task Scheduler:**
```powershell
# Create scheduled task for LinkedIn posting
schtasks /create /tn "AI_Employee_LinkedIn" /tr "python AI_Employee_Vault/watchers/linkedin_scheduler.py" /sc weekly /d MON /st 09:00

# Create task for daily briefing
schtasks /create /tn "AI_Employee_Daily_Briefing" /tr "qwen 'Generate daily briefing'" /sc daily /st 18:00
```

**Linux/Mac cron:**
```bash
# Edit crontab
crontab -e

# Add entries
*/2 * * * * python /path/to/gmail_watcher.py
0 9 * * 1 python /path/to/linkedin_scheduler.py
0 18 * * * qwen "Generate daily briefing"
```

**Usage with Qwen Code:**
```bash
# Setup all scheduled tasks
qwen "Configure Windows Task Scheduler for all AI Employee tasks. 
Create tasks for watchers, daily briefing, and weekly LinkedIn posts" --approval-mode yolo
```

---

### 16. Social Media MCP Integration Skill

**Purpose:** Post to LinkedIn, Twitter, Facebook via MCP servers.

**Trigger:** Approved social media post in `/Approved/Social_Media/`

**MCP Servers:**
- `linkedin-mcp` - LinkedIn posting
- `twitter-mcp` - Twitter/X posting
- `facebook-mcp` - Facebook posting

**Actions:**
- `post_update(platform, content, images?, schedule?)`
- `get_analytics(platform, date_range)`
- `schedule_post(platform, content, publish_time)`

**Usage with Qwen Code:**
```bash
# Post to LinkedIn (after approval)
qwen "Post the approved LinkedIn content from Approved/Social_Media folder" --approval-mode yolo

# Schedule post for later
qwen "Schedule this Twitter post for tomorrow at 10 AM" --approval-mode yolo

# Get analytics
qwen "Get LinkedIn analytics for last 30 days" --approval-mode yolo
```

**Setup:**
```bash
# Install LinkedIn MCP
npm install -g @modelcontextprotocol/server-linkedin

# Configure in mcp.json
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp",
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

---

### 17. Multi-Step Reasoning Skill (Claude Loop)

**Purpose:** Enable Claude to think, plan, and execute multi-step tasks autonomously.

**Trigger:** Complex task in `/Needs_Action/` requiring multiple actions

**Process:**
1. Read task file
2. Analyze requirements
3. Create detailed plan in `/Plans/`
4. Execute auto-approved steps
5. Create approval requests for sensitive steps
6. Wait for approvals
7. Continue execution
8. Update plan with progress
9. Move to `/Done/` when complete

**Plan Template:**
```markdown
---
created: 2026-03-27T10:30:00
status: in_progress
source: [[TASK_Client_Onboarding.md]]
type: multi_step_plan
---

# Multi-Step Action Plan

## Objective
Onboard new client with complete setup

## Steps
- [x] Read client requirements
- [x] Create welcome email draft
- [ ] Send welcome email (pending approval)
- [ ] Create project folder
- [ ] Schedule kickoff meeting
- [ ] Send calendar invite
- [ ] Setup invoicing (pending approval)

## Approval Queue
- Welcome email: Pending
- Calendar invite: Not started
- Invoicing setup: Not started

## Notes
Client prefers morning meetings. Timezone: EST
```

**Usage with Qwen Code:**
```bash
# Start multi-step task
qwen "Process this multi-step task. Create a detailed plan, 
execute auto-approved steps, and request approval for sensitive ones" --approval-mode yolo

# Continue in-progress plan
qwen "Continue execution of PLAN_Client_Onboarding.md. 
Check for approved items and proceed" --approval-mode yolo
```

---

## 🔧 Silver Tier Skill Implementation Guide

### Prerequisites

```bash
# Install Playwright for browser automation
npm install -D @playwright/test
playwright install chromium

# Install MCP servers
npm install -g @modelcontextprotocol/servers

# Install Python dependencies
pip install google-api-python-client
pip install playwright
pip install schedule
```

### Skill Registration

Add new skills to this document with:
- Clear name and purpose
- Trigger conditions
- Input/output specifications
- Example usage with Qwen Code
- Setup requirements

---

## 📖 Silver Tier Workflow Examples

### Example 1: Email + Approval + Send

```bash
# 1. Gmail Watcher detects new email
# Creates: Needs_Action/EMAIL_abc123.md

# 2. Qwen processes email
qwen "Process EMAIL_abc123.md. Draft reply and send for approval" --approval-mode yolo

# 3. Creates: Pending_Approval/EMAIL_REPLY_abc123.md

# 4. Human moves to Approved folder

# 5. Orchestrator executes
qwen "Execute approved email send" --approval-mode yolo

# 6. Moves to Done and logs
```

### Example 2: LinkedIn Auto-Posting

```bash
# 1. Scheduler triggers (Monday 9 AM)
python watchers/linkedin_scheduler.py

# 2. Qwen creates post
qwen "Create LinkedIn post about AI Employee project" --approval-mode yolo

# 3. Creates: Social_Media/LinkedIn_Drafts/post_2026-03-27.md

# 4. Auto-approved (scheduled post)
# Moves to: Approved/Social_Media/

# 5. LinkedIn MCP posts
qwen "Post approved LinkedIn content" --approval-mode yolo

# 6. Logs and archives
```

### Example 3: Multi-Step Client Onboarding

```bash
# 1. Task file created
# Needs_Action/TASK_Client_Onboarding.md

# 2. Qwen creates plan
qwen "Create multi-step plan for client onboarding" --approval-mode yolo

# 3. Creates: Plans/PLAN_Client_Onboarding.md

# 4. Executes auto-approved steps
# - Create welcome folder ✓
# - Draft welcome email ✓

# 5. Creates approval requests
# Pending_Approval/WELCOME_EMAIL.md
# Pending_Approval/CALENDAR_INVITE.md

# 6. Human approves

# 7. Continues execution
qwen "Continue client onboarding. Execute approved steps" --approval-mode yolo

# 8. Completes all steps
# Moves to Done
```

---

## 🎯 Silver Tier Completion Checklist

| Requirement | Skill | Status |
|-------------|-------|--------|
| 2+ Watcher scripts | Gmail, WhatsApp | 🆕 To Implement |
| LinkedIn auto-posting | LinkedIn Post Creator | 🆕 To Implement |
| MCP server integration | Email MCP, Browser MCP | 🆕 To Implement |
| HITL approval workflow | Approval Request Skill | ✅ Enhanced |
| Task scheduling | Task Scheduler | 🆕 To Implement |
| Multi-step reasoning | Claude Loop | 🆕 To Implement |

---

## 📋 Next Steps

1. **Implement Gmail Watcher** - Create `gmail_watcher.py`
2. **Implement WhatsApp Watcher** - Create `whatsapp_watcher.py`
3. **Setup Email MCP** - Configure Gmail API + MCP server
4. **Create LinkedIn Scheduler** - Weekly post automation
5. **Configure Task Scheduler** - Windows/cron jobs
6. **Test HITL Workflow** - End-to-end approval flow

---

*This document is maintained as part of the Silver Tier deliverables.*
*Update as new skills are developed and implemented.*
