# Personal AI Employee FTEs - Project Context

## Project Overview

This is a **hackathon project** for building **Autonomous AI Employees (Digital FTEs)** - AI agents that work 24/7 to manage personal and business affairs. The project uses **Claude Code** as the reasoning engine and **Obsidian** (local Markdown) as the dashboard/memory system.

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Claude Code | Reasoning engine for decision-making |
| **Memory/GUI** | Obsidian Vault | Dashboard, knowledge base, task tracking |
| **Senses (Watchers)** | Python Scripts | Monitor Gmail, WhatsApp, filesystems to trigger AI |
| **Hands (MCP)** | Model Context Protocol Servers | External actions (email, browser automation, payments) |
| **Persistence** | Ralph Wiggum Loop | Stop hook pattern for autonomous multi-step tasks |

### Key Concepts

- **Digital FTE**: An AI agent priced/operated like a human employee (works 168 hrs/week vs human's 40 hrs)
- **Watcher Pattern**: Lightweight Python scripts that monitor inputs and create `.md` files in `/Needs_Action` folder
- **Human-in-the-Loop**: Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
- **Business Handover**: Autonomous weekly audits generating "Monday Morning CEO Briefing"

## Directory Structure

```
Personal-AI-Employee-FTEs/
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main blueprint
├── skills-lock.json          # Skill dependencies tracking
├── .qwen/skills/             # Qwen skill integrations
│   └── browsing-with-playwright/
│       ├── SKILL.md          # Browser automation skill documentation
│       ├── references/
│       │   └── playwright-tools.md  # MCP tool reference (22 tools)
│       └── scripts/
│           ├── mcp-client.py      # Universal MCP client (HTTP + stdio)
│           ├── start-server.sh    # Start Playwright MCP server
│           ├── stop-server.sh     # Stop Playwright MCP server
│           └── verify.py          # Server health check
└── .git/
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers |
| GitHub Desktop | Latest | Version control |

### Playwright MCP Server (Browser Automation)

```bash
# Start server (keeps browser context alive)
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Verify server is running
python .qwen/skills/browsing-with-playwright/scripts/verify.py

# Stop server (closes browser + process)
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh
```

### MCP Client Usage

```bash
# List available tools
python scripts/mcp-client.py list -u http://localhost:8808

# Navigate to URL
python scripts/mcp-client.py call -u http://localhost:8808 \
  -t browser_navigate -p '{"url": "https://example.com"}'

# Take page snapshot (accessibility tree)
python scripts/mcp-client.py call -u http://localhost:8808 \
  -t browser_snapshot -p '{}'

# Click element
python scripts/mcp-client.py call -u http://localhost:8808 \
  -t browser_click -p '{"element": "Submit", "ref": "e42"}'

# Type text
python scripts/mcp-client.py call -u http://localhost:8808 \
  -t browser_type -p '{"element": "Search", "ref": "e15", "text": "hello"}'
```

### Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hrs | Obsidian dashboard, 1 watcher, basic Claude integration |
| **Silver** | 20-30 hrs | Multiple watchers, MCP servers, HITL approval, scheduling |
| **Gold** | 40+ hrs | Full integration, Odoo accounting, social media, Ralph Wiggum loop |
| **Platinum** | 60+ hrs | Cloud deployment, work-zone specialization, A2A upgrade |

## Development Conventions

### File-Based Communication

Agents communicate via Markdown files in structured folders:

```
Vault/
├── Inbox/              # Raw incoming items
├── Needs_Action/       # Items requiring processing
├── In_Progress/<agent>/ # Claimed by specific agent
├── Pending_Approval/   # Awaiting human approval
├── Approved/           # Approved actions (triggers execution)
├── Done/               # Completed tasks
└── Dashboard.md        # Real-time status summary
```

### Claim-by-Move Rule

First agent to move an item from `/Needs_Action` to `/In_Progress/<agent>/` owns it; other agents must ignore it.

### Security Rules

- Secrets never sync (`.env`, tokens, WhatsApp sessions, banking credentials)
- Cloud agents draft only; Local agents execute sensitive actions
- Single-writer rule for `Dashboard.md` (Local only)

### Watcher Script Pattern

```python
from base_watcher import BaseWatcher
from pathlib import Path

class MyWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        # Return list of new items to process
        pass

    def create_action_file(self, item) -> Path:
        # Create .md file in Needs_Action folder
        content = f'''---
type: my_type
source: {item['source']}
status: pending
---

## Content
{item['content']}

## Suggested Actions
- [ ] Process item
'''
        filepath = self.needs_action / f'TYPE_{item["id"]}.md'
        filepath.write_text(content)
        return filepath
```

## Available MCP Tools (Playwright)

22 tools available for browser automation:

| Category | Tools |
|----------|-------|
| **Navigation** | `browser_navigate`, `browser_navigate_back`, `browser_tabs` |
| **Snapshot** | `browser_snapshot`, `browser_take_screenshot` |
| **Interaction** | `browser_click`, `browser_type`, `browser_fill_form`, `browser_hover`, `browser_drag` |
| **Forms** | `browser_select_option`, `browser_file_upload`, `browser_handle_dialog` |
| **Wait** | `browser_wait_for` |
| **Advanced** | `browser_evaluate`, `browser_run_code`, `browser_console_messages`, `browser_network_requests` |
| **Utility** | `browser_close`, `browser_resize`, `browser_press_key`, `browser_install` |

## Key Workflows

### Form Submission
1. Navigate to page
2. Get snapshot to find element refs
3. Fill form fields using refs
4. Click submit
5. Wait for confirmation
6. Screenshot result

### Data Extraction
1. Navigate to page
2. Get snapshot (contains text content)
3. Use `browser_evaluate` for complex extraction
4. Process results

### Human-in-the-Loop Approval
```markdown
<!-- /Vault/Pending_Approval/PAYMENT_Client_A_2026-01-07.md -->
---
type: approval_request
action: payment
amount: 500.00
recipient: Client A
status: pending
---

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder.
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not responding | `bash scripts/stop-server.sh && bash scripts/start-server.sh` |
| Element not found | Run `browser_snapshot` first to get current refs |
| Click fails | Try `browser_hover` first, then click |
| Form not submitting | Use `"submit": true` with `browser_type` |
| Verification fails | Check process: `pgrep -f "@playwright/mcp"` |

## Resources

- **Main Blueprint**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Ralph Wiggum Pattern**: https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum
- **MCP Servers**: https://github.com/modelcontextprotocol/servers
- **Weekly Research Meeting**: Wednesdays 10:00 PM PKT on Zoom
