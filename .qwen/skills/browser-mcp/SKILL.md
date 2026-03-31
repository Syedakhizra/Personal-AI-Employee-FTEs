# Browser MCP Integration Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Browser MCP Integration Skill** enables the AI Employee to automate browser actions (navigate, click, fill forms) using Playwright-based MCP server.

---

## 🎯 Purpose

Automate web interactions like logging into portals, filling forms, downloading reports, and navigating websites through MCP-controlled browser automation.

---

## ⚡ Quick Start

```bash
# Navigate and extract data
qwen "Navigate to https://portal.example.com, login, download latest report" --approval-mode yolo

# Fill form (stop before submit)
qwen "Fill payment form for invoice #123. Stop before submit for approval" --approval-mode yolo
```

---

## 🔧 Configuration

### MCP Server Setup

1. **Install Playwright MCP:**
   ```bash
   npm install -g @anthropic/browser-mcp
   ```

2. **Configure MCP:**
   ```json
   ~/.config/claude-code/mcp.json
   {
     "mcpServers": {
       "browser": {
         "command": "browser-mcp",
         "env": {
           "HEADLESS": "true",
           "TIMEOUT": "30000"
         }
       }
     }
   }
   ```

3. **Install Playwright:**
   ```bash
   npx playwright install chromium
   ```

---

## 📥 Available Actions

| Action | Description | Approval Required |
|--------|-------------|-------------------|
| `browser_navigate` | Go to URL | No |
| `browser_click` | Click element | No |
| `browser_type` | Type text | No |
| `browser_fill_form` | Fill form fields | Yes (before submit) |
| `browser_snapshot` | Get page snapshot | No |
| `browser_download` | Download file | Yes |
| `browser_submit` | Submit form | **Always** |

---

## 🎓 Usage Examples

### Example 1: Login and Download

```bash
qwen "Use Browser MCP:
1. Navigate to https://bank.example.com
2. Login with credentials (from secure store)
3. Navigate to Statements
4. Download last month's statement
5. Save to /Accounting/" --approval-mode yolo
```

### Example 2: Fill Payment Form

```bash
qwen "Fill payment form:
- Invoice: #123
- Amount: $500
- Recipient: Vendor ABC
Fill all fields but DO NOT submit.
Create approval request for submission." --approval-mode yolo
```

### Example 3: Data Extraction

```bash
qwen "Navigate to https://analytics.example.com
Extract last 30 days traffic data
Save to /Reports/traffic_analysis.md" --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. AI receives web automation task      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Check if action requires approval    │
│    - Navigation = Auto                  │
│    - Form fill = Auto                   │
│    - Form submit = Approval ALWAYS      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. Browser MCP executes actions         │
│    - Launches headless browser          │
│    - Navigates to URL                   │
│    - Performs interactions              │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. For form submit:                     │
│    - Fill all fields                    │
│    - Stop before submit                 │
│    - Create approval file               │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 5. Human approves submission            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 6. Browser MCP submits form             │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 7. Log and archive in Done              │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **Never auto-submit** | All form submissions require approval |
| **Credentials** | Store in secure vault, never in code |
| **Payment forms** | Always require human approval |
| **Session cookies** | Never sync to cloud |
| **Screenshots** | Log all actions for audit |

---

## 🏷️ Approval Rules

### Auto-Approved Actions
- Navigation to known URLs
- Reading page content
- Taking snapshots
- Downloading public files

### Requires Approval
- Form submissions
- Payment transactions
- Login to sensitive sites
- File uploads
- Data modifications

---

## 🛠️ Troubleshooting

### Issue: "Browser won't launch"

**Solution:**
```bash
# Reinstall Playwright browsers
npx playwright install chromium --force
```

### Issue: "Element not found"

**Solution:**
- Use `browser_snapshot` to get current page state
- Check element selectors
- Add wait time for page load

---

## ✅ Testing Checklist

- [ ] Browser MCP installed
- [ ] Configuration complete
- [ ] Test navigation works
- [ ] Test form fill works
- [ ] Approval workflow tested
- [ ] Form submit with approval works

---

*Browser MCP Integration Skill v1.0 - Silver Tier*
