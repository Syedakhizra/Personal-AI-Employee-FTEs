# AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This is a **Bronze Tier** implementation of the Personal AI Employee Hackathon - a autonomous AI agent that manages personal and business affairs 24/7 using **Qwen Code** as the reasoning engine and **Obsidian** as the dashboard.

---

## 🏆 Bronze Tier Deliverables Checklist

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (File System monitoring)
- [x] Qwen Code successfully reading from and writing to the vault
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] All AI functionality implemented as [Agent Skills](./AI_Employee_Vault/Agent_Skills.md)

---

## 📁 Project Structure

```
Personal-AI-Employee-FTEs/
├── AI_Employee_Vault/              # Obsidian Vault (your AI's memory)
│   ├── Dashboard.md                # Real-time status dashboard
│   ├── Company_Handbook.md         # Rules of Engagement
│   ├── Business_Goals.md           # Objectives and metrics
│   ├── Agent_Skills.md             # Skill documentation
│   ├── Inbox/                      # Drop files here for processing
│   ├── Needs_Action/               # Items awaiting processing
│   ├── Plans/                      # Multi-step task plans
│   ├── Pending_Approval/           # Awaiting human approval
│   ├── Approved/                   # Approved actions ready to execute
│   ├── Rejected/                   # Rejected actions
│   ├── Done/                       # Completed tasks archive
│   ├── Logs/                       # System audit logs
│   ├── Accounting/                 # Financial records
│   ├── Briefings/                  # Daily/weekly briefings
│   └── watchers/                   # Python watcher scripts
│       ├── base_watcher.py         # Abstract base class
│       ├── filesystem_watcher.py   # File drop monitor (Bronze)
│       └── orchestrator.py         # Master process
└── README.md                       # This file
```

---

## 🚀 Quick Start

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Qwen Code](https://claude.ai/qwen-code) | Latest | AI reasoning engine |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Dashboard/Knowledge base |

### Installation

1. **Clone or download this repository**

2. **Verify Qwen Code is installed:**
   ```bash
   qwen --version
   ```

3. **Open the vault in Obsidian:**
   - Launch Obsidian
   - Click "Open folder as vault"
   - Select: `AI_Employee_Vault`

### Running the AI Employee

#### Option 1: Start the Orchestrator (Recommended)

```bash
cd AI_Employee_Vault
python watchers/orchestrator.py .
```

This starts:
- File System Watcher (monitors `/Inbox` for new files)
- Main orchestration loop (processes items every 30 seconds)
- Dashboard auto-updates

#### Option 2: Run Watcher Separately

```bash
# Terminal 1: Start the file watcher
python watchers/filesystem_watcher.py .

# Terminal 2: Process items manually
python watchers/orchestrator.py . process
```

#### Option 3: Use Qwen Code Directly

```bash
# Navigate to vault
cd AI_Employee_Vault

# Ask Qwen Code to process pending items
qwen "Check /Needs_Action folder and process any pending items. Create plans for complex tasks and move completed items to /Done."
```

---

## 📖 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR AI EMPLOYEE                         │
├─────────────────────────────────────────────────────────────┤
│  Perception (Watchers) → Reasoning (Qwen) → Action          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📥 Inbox         →  📋 Needs_Action  →  🧠 Qwen Code      │
│       ↓                  ↓                    ↓              │
│  File Drop        →  Action Files    →  Plans/Approval      │
│                                             ↓               │
│  ✅ Done  ←  Move after complete  ←  Human Approval         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### The Watcher Pattern

**Watchers** are lightweight Python scripts that run continuously, monitoring for new inputs:

1. **File System Watcher** (Bronze Tier): Monitors `/Inbox` folder for dropped files
2. Future tiers: Gmail Watcher, WhatsApp Watcher, Finance Watcher

When a file is detected:
1. File is copied to `/Needs_Action/`
2. Metadata `.md` file is created
3. Orchestrator triggers Claude Code to process

### Human-in-the-Loop (HITL)

For sensitive actions, the AI:
1. Creates approval request in `/Pending_Approval/`
2. Waits for human to move file to `/Approved/`
3. Executes the action
4. Logs result and moves to `/Done/`

---

## 📝 Usage Guide

### Processing a File

1. **Drop a file in `/Inbox/`**
   - Any file type: documents, images, text, etc.
   
2. **Watcher detects and creates action file**
   - File moved to `/Needs_Action/`
   - Metadata `.md` file created

3. **Qwen Code processes**
   - Reads and analyzes content
   - Creates plan in `/Plans/` if needed
   - Executes or requests approval

4. **Task completes**
   - Files moved to `/Done/`
   - Dashboard updated
   - Log entry created

### Example Workflow

```bash
# 1. User drops invoice.pdf in /Inbox/

# 2. Watcher creates:
#    /Needs_Action/FILE_20260228_103000_invoice.pdf
#    /Needs_Action/FILE_20260228_103000_invoice.pdf.md

# 3. Qwen Code processes:
qwen "Process the invoice file:
- Extract vendor, amount, date
- Categorize as expense
- Create approval request if amount > $500
- Log to /Accounting/"

# 4. If approval needed:
#    Creates: /Pending_Approval/PAYMENT_vendor_20260228.md

# 5. Human approves (moves to /Approved/)

# 6. Qwen executes and moves to /Done/
```

---

## 🛠️ Commands Reference

### Orchestrator

```bash
# Start orchestrator (continuous mode)
python watchers/orchestrator.py .

# Process pending items once
python watchers/orchestrator.py . process

# Show system status
python watchers/orchestrator.py . status
```

### File System Watcher

```bash
# Start watcher (standalone)
python watchers/filesystem_watcher.py .

# Custom check interval (seconds)
python watchers/filesystem_watcher.py . --interval 10
```

### Qwen Code Integration

```bash
# Process all pending items
qwen "Process all files in /Needs_Action. For each:
1. Read and categorize
2. Create action plan
3. Execute or request approval
4. Move to /Done when complete"

# Generate daily briefing
qwen "Generate a daily briefing in /Briefings/ summarizing:
- Files processed today
- Tasks completed
- Pending items
- Recommendations"

# Update dashboard
qwen "Update Dashboard.md with current stats and recent activity"
```

---

## 📊 Folder Reference

| Folder | Purpose | Auto-Created |
|--------|---------|--------------|
| `/Inbox/` | Drop files here for processing | ✅ |
| `/Needs_Action/` | Items awaiting processing | ✅ |
| `/Plans/` | Multi-step task plans | ✅ |
| `/Pending_Approval/` | Awaiting human decision | ✅ |
| `/Approved/` | Ready to execute | ✅ |
| `/Rejected/` | Declined actions | ✅ |
| `/Done/` | Completed tasks archive | ✅ |
| `/Logs/` | System audit logs | ✅ |
| `/Accounting/` | Financial records | ✅ |
| `/Briefings/` | Daily/weekly summaries | ✅ |

---

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Custom drop folder
export DROP_FOLDER="/path/to/drop"

# Optional: Dry run mode (no external actions)
export DRY_RUN="true"

# Optional: Log level
export LOG_LEVEL="INFO"
```

### Watcher Settings

Edit `watchers/filesystem_watcher.py`:

```python
# Check interval (seconds)
check_interval = 5  # Default: 5 seconds

# Folders to watch
self.watch_folder = self.inbox
self.drop_folder = Path(os.getenv('DROP_FOLDER', self.watch_folder))
```

---

## 📈 Monitoring

### Check System Status

```bash
python watchers/orchestrator.py . status
```

### View Logs

```bash
# Today's orchestrator log
cat Logs/2026-02-28_orchestrator.log

# Watcher logs
cat Logs/2026-02-28_FilesystemWatcher.log
```

### Dashboard

Open `Dashboard.md` in Obsidian for real-time status.

---

## 🔒 Security

### Credential Management

- **Never** store credentials in the vault
- Use environment variables for API keys
- Create `.env` file (add to `.gitignore`)

```bash
# .env example (NEVER commit)
GMAIL_CLIENT_ID=your_client_id
BANK_API_TOKEN=your_token
```

### Approval Thresholds

See [[Company_Handbook]] for approval rules:

| Action | Auto-Approve | Requires Approval |
|--------|--------------|-------------------|
| Email replies | ❌ | Always |
| Payments | ❌ | Always |
| File operations | Read/Create | Delete/Move |

---

## 🐛 Troubleshooting

### Qwen Code Not Found

```bash
# Install Qwen Code
npm install -g @anthropic/qwen-code

# Verify installation
qwen --version
```

### Watcher Not Detecting Files

1. Check watcher is running: `python watchers/orchestrator.py . status`
2. Verify folder permissions
3. Check logs: `cat Logs/*.log`

### Files Not Processing

1. Ensure files have `.md` extension for metadata
2. Check file isn't locked by another process
3. Run orchestrator in process mode: `python watchers/orchestrator.py . process`

---

## 📚 Documentation

- [[Dashboard]] - Real-time status
- [[Company_Handbook]] - Rules of Engagement
- [[Business_Goals]] - Objectives and Metrics
- [[Agent_Skills]] - Capability Documentation

---

## 🎯 Next Steps (Silver Tier)

Upgrade to Silver Tier by adding:

- [ ] Gmail Watcher (email monitoring)
- [ ] WhatsApp Watcher (message monitoring)
- [ ] MCP Server for email sending
- [ ] Scheduled tasks (cron/Task Scheduler)
- [ ] Human-in-the-loop approval workflow automation

---

## 📞 Resources

- **Hackathon Blueprint:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Weekly Meeting:** Wednesdays 10:00 PM PKT
- **Zoom:** https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- **YouTube:** https://www.youtube.com/@panaversity

---

## 📄 License

This project is part of the Personal AI Employee Hackathon 2026.

---

*Built with ❤️ by AI Employee v0.1 (Bronze Tier)*
