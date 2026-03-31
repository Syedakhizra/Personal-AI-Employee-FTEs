# Task Scheduler Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Task Scheduler Skill** enables the AI Employee to schedule and run recurring tasks automatically via Windows Task Scheduler or cron.

---

## 🎯 Purpose

Automate recurring tasks like daily briefings, weekly reports, watcher monitoring, and scheduled social media posts.

---

## ⚡ Quick Start

```bash
# Windows: Create scheduled task
schtasks /create /tn "AI_Employee_Daily_Briefing" /tr "qwen 'Generate daily briefing'" /sc daily /st 18:00

# Linux/Mac: Add cron job
crontab -e
0 18 * * * qwen "Generate daily briefing"
```

---

## 🔧 Configuration

### Windows Task Scheduler

**Create Task:**
```powershell
# Daily briefing at 6 PM
schtasks /create /tn "AI_Employee_Daily_Briefing" ^
  /tr "qwen 'Generate daily briefing'" ^
  /sc daily /st 18:00 ^
  /ru SYSTEM

# Weekly LinkedIn post (Monday 9 AM)
schtasks /create /tn "AI_Employee_LinkedIn" ^
  /tr "python watchers/linkedin_scheduler.py" ^
  /sc weekly /d MON /st 09:00 ^
  /ru SYSTEM

# Gmail watcher (every 2 minutes)
schtasks /create /tn "AI_Employee_Gmail" ^
  /tr "python watchers/gmail_watcher.py" ^
  /sc minute /mo 2 ^
  /ru SYSTEM
```

**List Tasks:**
```powershell
schtasks /query /tn "AI_Employee_*"
```

**Delete Task:**
```powershell
schtasks /delete /tn "AI_Employee_Daily_Briefing" /f
```

### Linux/Mac Cron

**Edit crontab:**
```bash
crontab -e
```

**Add entries:**
```bash
# Daily briefing at 6 PM
0 18 * * * qwen "Generate daily briefing"

# Weekly LinkedIn post (Monday 9 AM)
0 9 * * 1 python /path/to/linkedin_scheduler.py

# Gmail watcher (every 2 minutes)
*/2 * * * * python /path/to/gmail_watcher.py

# Hourly dashboard update
0 * * * * qwen "Update Dashboard.md"
```

**List cron jobs:**
```bash
crontab -l
```

---

## 📅 Scheduled Tasks

| Task | Frequency | Time | Command |
|------|-----------|------|---------|
| Gmail check | Every 2 min | Continuous | `gmail_watcher.py` |
| WhatsApp check | Every 30 sec | Continuous | `whatsapp_watcher.py` |
| LinkedIn post | Weekly | Monday 9 AM | `linkedin_scheduler.py` |
| Daily briefing | Daily | 6 PM | `qwen "Generate briefing"` |
| Dashboard update | Hourly | Every hour | `qwen "Update Dashboard"` |
| Weekly audit | Weekly | Friday 5 PM | `qwen "Weekly audit"` |

---

## 🎓 Usage Examples

### Example 1: Setup All Tasks

```bash
qwen "Configure Windows Task Scheduler for all AI Employee tasks.
Create tasks for:
1. Gmail watcher (every 2 min)
2. WhatsApp watcher (every 30 sec)
3. Daily briefing (6 PM daily)
4. LinkedIn post (Monday 9 AM)
5. Dashboard update (hourly)
6. Weekly audit (Friday 5 PM)" --approval-mode yolo
```

### Example 2: Create Daily Briefing Task

```bash
# Windows
schtasks /create /tn "AI_Employee_Daily_Briefing" ^
  /tr "qwen 'Generate daily briefing summarizing:
  - Files processed today
  - Tasks completed
  - Pending items
  - Tomorrow priorities'" ^
  /sc daily /st 18:00
```

### Example 3: Verify Scheduled Tasks

```bash
qwen "List all scheduled AI Employee tasks.
Verify they are running correctly.
Report any failures." --approval-mode yolo
```

---

## 📊 Task Status

| Task | Status | Last Run | Next Run |
|------|--------|----------|----------|
| Gmail Watcher | ✅ Running | 2 min ago | 1 min |
| WhatsApp Watcher | ✅ Running | 30 sec ago | 30 sec |
| Daily Briefing | ✅ Running | Yesterday 6 PM | Today 6 PM |
| LinkedIn Post | ✅ Running | Last Monday | Next Monday |

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. Task Scheduler triggers at scheduled │
│    time (cron/Task Scheduler)           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Executes command/script              │
│    - Python watcher                     │
│    - Qwen command                       │
│    - Custom script                      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. AI Employee performs task            │
│    - Process emails                     │
│    - Generate briefing                  │
│    - Create social post                 │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. Logs result                          │
│    - Success → Log + Done               │
│    - Failure → Log + Alert              │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **Run as SYSTEM** | Tasks run with system privileges |
| **No passwords** | Never store passwords in tasks |
| **Secure credentials** | Use environment variables |
| **Log all runs** | Keep audit trail |

---

## 🛠️ Troubleshooting

### Issue: "Task not running"

**Solution:**
```powershell
# Check task status
schtasks /query /tn "AI_Employee_Daily_Briefing" /v

# Run task manually
schtasks /run /tn "AI_Employee_Daily_Briefing"

# Check task history
Get-ScheduledTask -TaskName "AI_Employee_Daily_Briefing"
```

### Issue: "Cron job not executing"

**Solution:**
```bash
# Check cron service
sudo systemctl status cron

# Check cron logs
grep CRON /var/log/syslog

# Verify crontab
crontab -l
```

---

## ✅ Testing Checklist

- [ ] Task Scheduler accessible
- [ ] Test task created
- [ ] Task runs at scheduled time
- [ ] Logs created
- [ ] All AI tasks scheduled
- [ ] Failures logged

---

*Task Scheduler Skill v1.0 - Silver Tier*
