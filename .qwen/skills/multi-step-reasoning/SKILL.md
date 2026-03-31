# Multi-Step Reasoning Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Multi-Step Reasoning Skill** enables the AI Employee to break down complex tasks into actionable steps, execute autonomously, and track progress through completion.

---

## 🎯 Purpose

Handle complex multi-step tasks that require planning, execution, approval requests, and progress tracking with autonomous reasoning.

---

## ⚡ Quick Start

```bash
# Start multi-step task
qwen "Process this complex task. Create detailed plan, execute auto-approved steps, request approval for sensitive ones" --approval-mode yolo

# Continue in-progress plan
qwen "Continue execution of PLAN_Client_Onboarding.md. Check approved items and proceed" --approval-mode yolo
```

---

## 📁 Plan Template

```markdown
---
created: 2026-03-27T10:30:00
status: in_progress
source: [[TASK_Client_Onboarding.md]]
type: multi_step_plan
estimated_completion: 2026-03-28
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
| Item | Status | Created |
|------|--------|---------|
| Welcome email | Pending | 2026-03-27 10:30 |
| Calendar invite | Not started | - |
| Invoicing setup | Not started | - |

## Progress
- Completed: 2/7 (28%)
- Pending approval: 1
- Blocked: 0

## Notes
Client prefers morning meetings. Timezone: EST.
Contact: john@client.com

## Blockers
None currently.
```

---

## 🎓 Usage Examples

### Example 1: Client Onboarding

```bash
qwen "Process TASK_Client_Onboarding.md.

Create multi-step plan:
1. Read client requirements
2. Create welcome email (approval needed)
3. Setup project folder (auto)
4. Schedule kickoff meeting (approval needed)
5. Create invoicing account (approval needed)

Execute auto-approved steps, create approval requests for others.
Update plan with progress." --approval-mode yolo
```

### Example 2: Event Planning

```bash
qwen "Plan company event for 50 people.

Steps:
1. Research venues (auto)
2. Get quotes (auto)
3. Select venue (approval needed)
4. Send invitations (approval needed)
5. Book catering (approval needed)
6. Confirm arrangements (auto)

Create plan, execute, track progress." --approval-mode yolo
```

### Example 3: Monthly Reporting

```bash
qwen "Generate monthly business report.

Steps:
1. Collect financial data (auto)
2. Gather project updates (auto)
3. Analyze metrics (auto)
4. Create report draft (auto)
5. Send for review (approval needed)
6. Distribute final (approval needed)

Execute all steps autonomously." --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. AI receives complex task             │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Analyzes requirements                │
│    - Identifies all steps               │
│    - Determines dependencies            │
│    - Estimates time                     │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. Creates detailed plan                │
│    - All steps with checkboxes          │
│    - Approval requirements              │
│    - Progress tracking                  │
│    - Notes section                      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. Executes auto-approved steps         │
│    - Marks complete [x]                 │
│    - Updates progress                   │
│    - Logs actions                       │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 5. Creates approval requests            │
│    - Saves to Pending_Approval/         │
│    - Updates plan with approval status  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 6. Waits for approvals                  │
│    (Orchestrator monitors)              │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 7. Continues execution after approval   │
│    - Executes approved actions          │
│    - Updates progress                   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 8. Completes all steps                  │
│    - Marks plan complete                │
│    - Moves to Done                      │
│    - Logs summary                       │
└─────────────────────────────────────────┘
```

---

## 📊 Plan Status

| Status | Description | Action |
|--------|-------------|--------|
| `pending` | Plan created, not started | Begin execution |
| `in_progress` | Some steps complete | Continue execution |
| `blocked` | Waiting for approval | Monitor approvals |
| `completed` | All steps done | Archive in Done |
| `cancelled` | Task cancelled | Archive with reason |

---

## 🏷️ Step Categories

### Auto-Approved Steps
- Reading files
- Creating drafts
- Data analysis
- Internal folder operations
- Report generation

### Requires Approval
- Sending external communications
- Payments/financial
- Calendar invites to external
- File sharing externally
- System configuration changes

---

## 📈 Progress Tracking

### Progress Calculation
```
Progress % = (Completed Steps / Total Steps) × 100
```

### Status Updates
- After each step completion
- After each approval received
- When blockers are resolved
- On status change

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **Never skip approval** | Always create approval file |
| **Log all steps** | Complete audit trail |
| **Track blockers** | Document what's blocking |
| **Progress updates** | Keep plan current |

---

## 🛠️ Troubleshooting

### Issue: "Plan not progressing"

**Solution:**
```bash
# Check approval status
qwen "Check Pending_Approval folder for items related to PLAN_Client_Onboarding"

# Continue after approval
qwen "Continue PLAN_Client_Onboarding. Execute newly approved steps"
```

### Issue: "Steps out of order"

**Solution:**
- Review step dependencies
- Reorder plan if needed
- Document dependency changes

---

## ✅ Testing Checklist

- [ ] Plan template created
- [ ] Steps identified
- [ ] Auto-approved steps execute
- [ ] Approval requests created
- [ ] Progress tracked
- [ ] Plan completes successfully
- [ ] All steps logged

---

*Multi-Step Reasoning Skill v1.0 - Silver Tier*
