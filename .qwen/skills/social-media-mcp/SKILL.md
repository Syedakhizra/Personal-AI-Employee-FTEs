# Social Media MCP Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Social Media MCP Skill** enables the AI Employee to post content to LinkedIn, Twitter/X, and Facebook via MCP servers for automated social media management.

---

## 🎯 Purpose

Publish approved social media content across multiple platforms automatically, with scheduling and analytics capabilities.

---

## ⚡ Quick Start

```bash
# Post to LinkedIn
qwen "Post the approved LinkedIn content from Approved/Social_Media/" --approval-mode yolo

# Schedule Twitter post
qwen "Schedule this Twitter post for tomorrow at 10 AM" --approval-mode yolo

# Get analytics
qwen "Get LinkedIn analytics for last 30 days" --approval-mode yolo
```

---

## 🔧 Configuration

### MCP Servers Setup

**1. LinkedIn MCP:**
```bash
npm install -g @modelcontextprotocol/server-linkedin
```

**2. Twitter MCP:**
```bash
npm install -g @modelcontextprotocol/server-twitter
```

**3. Facebook MCP:**
```bash
npm install -g @modelcontextprotocol/server-facebook
```

**4. Configure MCP:**
```json
~/.config/claude-code/mcp.json
{
  "mcpServers": {
    "linkedin": {
      "command": "linkedin-mcp",
      "env": {
        "LINKEDIN_ACCESS_TOKEN": "your-token"
      }
    },
    "twitter": {
      "command": "twitter-mcp",
      "env": {
        "TWITTER_API_KEY": "your-key",
        "TWITTER_API_SECRET": "your-secret"
      }
    },
    "facebook": {
      "command": "facebook-mcp",
      "env": {
        "FACEBOOK_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

---

## 📥 Available Actions

| Platform | Actions | Approval Required |
|----------|---------|-------------------|
| **LinkedIn** | post, schedule, analytics | Yes (before posting) |
| **Twitter** | tweet, reply, schedule | Yes (before posting) |
| **Facebook** | post, schedule, insights | Yes (before posting) |

---

## 🎓 Usage Examples

### Example 1: Post to LinkedIn

```bash
qwen "Post to LinkedIn using MCP:
Content: 🚀 Exciting news! Our AI Employee project...
Hashtags: #AI #Automation #Business
Image: /Social_Media/images/ai_employee.png
Save to Approved/Social_Media/ first" --approval-mode yolo
```

### Example 2: Schedule Twitter Thread

```bash
qwen "Create and schedule Twitter thread:
Tweet 1: Introducing our AI Employee...
Tweet 2: Key features include...
Tweet 3: Try it now at...
Schedule for Wednesday 12 PM" --approval-mode yolo
```

### Example 3: Cross-Platform Post

```bash
qwen "Post same content to all platforms:
- LinkedIn (professional tone)
- Twitter (concise, hashtags)
- Facebook (engaging, image)
Create approval request for each" --approval-mode yolo
```

### Example 4: Get Analytics

```bash
qwen "Get social media analytics:
- LinkedIn: Last 30 days impressions, engagement
- Twitter: Follower growth, top tweets
- Facebook: Page insights, reach
Create summary report" --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. AI creates social media post draft   │
│    - Content                            │
│    - Hashtags                           │
│    - Images                             │
│    - Schedule time                      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Creates approval request             │
│    Saves to Pending_Approval/Social/    │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. Human approves (moves to Approved/)  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. At scheduled time, Social Media MCP  │
│    posts to platforms                   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 5. Logs results, archives in Done       │
└─────────────────────────────────────────┘
```

---

## 📊 Posting Schedule

| Platform | Best Time | Frequency |
|----------|-----------|-----------|
| **LinkedIn** | Tue-Thu 9 AM | 3x/week |
| **Twitter** | Mon-Fri 12 PM | 5x/week |
| **Facebook** | Wed-Fri 1 PM | 3x/week |

---

## 🏷️ Content Guidelines

### LinkedIn
- ✅ Professional tone
- ✅ Industry insights
- ✅ Company updates
- ✅ 3-5 hashtags

### Twitter
- ✅ Concise (280 chars)
- ✅ Engaging questions
- ✅ Trending hashtags
- ✅ Thread for long content

### Facebook
- ✅ Visual content
- ✅ Engaging stories
- ✅ Community focus
- ✅ Call to action

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **API tokens** | Never commit credentials |
| **Approval required** | All posts require approval |
| **Draft only** | AI creates drafts, human approves |
| **Log all posts** | Keep audit trail |

---

## 📈 Analytics Tracking

| Metric | Platform | Frequency |
|--------|----------|-----------|
| Impressions | All | Weekly |
| Engagement rate | All | Weekly |
| Follower growth | All | Weekly |
| Click-through rate | LinkedIn | Weekly |
| Top performing post | All | Weekly |

---

## 🛠️ Troubleshooting

### Issue: "MCP server not connected"

**Solution:**
```bash
# Check MCP configuration
cat ~/.config/claude-code/mcp.json

# Restart MCP servers
linkedin-mcp --restart
twitter-mcp --restart
```

### Issue: "Post failed"

**Solution:**
- Check API credentials valid
- Verify content meets platform guidelines
- Review MCP logs for error details

---

## ✅ Testing Checklist

- [ ] LinkedIn MCP configured
- [ ] Twitter MCP configured
- [ ] Facebook MCP configured
- [ ] Test post drafted
- [ ] Approval workflow works
- [ ] Post published successfully
- [ ] Analytics retrieved

---

*Social Media MCP Skill v1.0 - Silver Tier*
