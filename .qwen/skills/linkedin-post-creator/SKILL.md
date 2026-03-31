# LinkedIn Post Creator Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **LinkedIn Post Creator Skill** enables the AI Employee to automatically create, schedule, and post LinkedIn content for business promotion and sales generation.

---

## 🎯 Purpose

Generate professional LinkedIn posts automatically, schedule them for optimal posting times, and manage social media presence with human approval workflow.

---

## ⚡ Quick Start

```bash
# Create LinkedIn post
qwen "Create a LinkedIn post about our AI Employee project. 
Focus on automation benefits. Keep it professional." --approval-mode yolo

# Schedule post
qwen "Schedule this LinkedIn post for Monday 9 AM" --approval-mode yolo
```

---

## 🔧 Configuration

### Setup Requirements

1. **LinkedIn API Access:**
   - LinkedIn Developer Account
   - Create App at https://www.linkedin.com/developers/
   - Get API credentials

2. **MCP Server:**
   ```bash
   npm install -g @modelcontextprotocol/server-linkedin
   ```

3. **Configure MCP:**
   ```json
   ~/.config/claude-code/mcp.json
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

## 📁 File Structure

```
AI_Employee_Vault/
├── Social_Media/
│   ├── LinkedIn_Drafts/
│   │   └── LinkedIn_2026-03-27_AI_Automation.md
│   └── LinkedIn_Scheduled/
│       └── LinkedIn_2026-03-28_09-00_Post.md
├── Approved/
│   └── Social_Media/
│       └── LinkedIn_Approved_Post.md
└── Logs/
    └── 2026-03-27_LinkedIn.log
```

---

## 📤 Output

### Draft Post Template

```markdown
---
type: linkedin_post
topic: AI Automation
created: 2026-03-27T10:30:00
status: draft
scheduled_for: 2026-03-28T09:00:00
author: AI Employee
---

# LinkedIn Post Draft

## Content

🚀 Exciting update from our company!

We're helping businesses automate their workflows with AI-powered solutions.

Key benefits:
✅ 24/7 operation
✅ 90% cost reduction
✅ Zero errors

#AI #Automation #Business #Technology

---
*Drafted by AI Employee - Requires approval before posting*

## To Approve
Move this file to /Approved/Social_Media/ folder.

## To Reject
Move this file to /Rejected/ folder.
```

---

## 🎓 Usage Examples

### Example 1: Create Post

```bash
qwen "Create LinkedIn post about our AI Employee Hackathon.
Include:
- Project overview
- Key features
- Call to action
Use emojis and hashtags. Keep under 300 words." --approval-mode yolo
```

### Example 2: Schedule Post

```bash
qwen "Schedule this LinkedIn post for next Monday at 9 AM.
Create scheduled file in Social_Media/LinkedIn_Scheduled/" --approval-mode yolo
```

### Example 3: Post After Approval

```bash
qwen "Post the approved LinkedIn content from Approved/Social_Media folder.
Use LinkedIn MCP to publish." --approval-mode yolo
```

---

## 📅 Posting Schedule

| Day | Time | Content Type |
|-----|------|--------------|
| Monday | 9:00 AM | Business update |
| Wednesday | 12:00 PM | Industry insight |
| Friday | 3:00 PM | Weekly summary |

---

## 🏷️ Content Guidelines

### Do's
- ✅ Professional tone
- ✅ Clear value proposition
- ✅ Relevant hashtags (3-5)
- ✅ Engaging opening
- ✅ Call to action

### Don'ts
- ❌ Overly promotional
- ❌ Too many hashtags
- ❌ Long paragraphs
- ❌ Controversial topics

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. Scheduler triggers (Monday 9 AM)     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. AI creates post draft                │
│    - Writes content                     │
│    - Adds hashtags                      │
│    - Sets schedule time                 │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. Saves to Social_Media/LinkedIn_Drafts│
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. Auto-approved (scheduled post)       │
│    Moves to Approved/Social_Media       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 5. At scheduled time, LinkedIn MCP posts│
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 6. Logs and archives in Done            │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **API tokens** | Never commit LinkedIn API credentials |
| **Approval required** | All posts require human approval |
| **Draft only** | AI creates drafts, human approves |

---

## 📊 Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **Social Media MCP** | Post to LinkedIn via MCP |
| **HITL Approval** | Approval before posting |
| **Task Scheduler** | Weekly auto-scheduling |
| **Daily Briefing** | Report on post performance |

---

## ✅ Testing Checklist

- [ ] LinkedIn API credentials obtained
- [ ] MCP server configured
- [ ] Test post created
- [ ] Approval workflow tested
- [ ] Post published successfully
- [ ] Logged in Done

---

*LinkedIn Post Creator Skill v1.0 - Silver Tier*
