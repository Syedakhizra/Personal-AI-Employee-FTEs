---
version: 0.1
tier: bronze
last_updated: 2026-02-28
---

# Agent Skills

This document defines the **Agent Skills** for the AI Employee - reusable capabilities that Qwen Code can invoke to perform specific tasks.

## 📚 Available Skills

### 1. File Processing Skill

**Purpose:** Process files dropped in the `/Inbox` or `/Needs_Action` folder.

**Trigger:** File detected by File System Watcher

**Actions:**
- Read file content
- Analyze file type and purpose
- Categorize the file
- Suggest next actions

**Usage with Qwen Code:**
```bash
qwen "Process all files in /Needs_Action folder. For each file:
1. Read and analyze the content
2. Categorize it (document, invoice, task, etc.)
3. Create a plan in /Plans if multi-step action needed
4. Move to /Done when complete"
```

---

### 2. Task Planning Skill

**Purpose:** Break down complex requests into actionable steps.

**Trigger:** New item in `/Needs_Action` requiring multiple actions

**Output:** Creates a `Plan.md` file with checkboxes

**Template:**
```markdown
---
created: YYYY-MM-DDTHH:MM:SS
status: pending
source: [[filename.md]]
type: action_plan
---

# Action Plan

## Objective
[Clear statement of what needs to be accomplished]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Required Approvals
- [ ] Approval type (if any)

## Notes
[Any relevant context]
```

**Usage with Qwen Code:**
```bash
qwen "Create a detailed action plan for processing: [filename.md]"
```

---

### 3. Approval Request Skill

**Purpose:** Request human approval for sensitive actions.

**Trigger:** Action requires human-in-the-loop

**Output:** Creates file in `/Pending_Approval`

**Template:**
```markdown
---
type: approval_request
action: [action_type]
created: YYYY-MM-DDTHH:MM:SS
status: pending
---

# Approval Required

## Action Details
- **Action:** [Description]
- **Target:** [Who/what is affected]
- **Reason:** [Why this is needed]

## To Approve
Move this file to `/Approved` folder.

## To Reject
Move this file to `/Rejected` folder.
```

**Usage with Qwen Code:**
```bash
qwen "This action requires approval. Create an approval request file in /Pending_Approval with all relevant details."
```

---

### 4. Dashboard Update Skill

**Purpose:** Keep the [[Dashboard]] current with latest status.

**Trigger:** After any significant action

**Actions:**
- Update last_updated timestamp
- Refresh file counts
- Log recent activity
- Update system health status

**Usage with Qwen Code:**
```bash
qwen "Update the Dashboard.md to reflect:
- Current file counts in each folder
- Recent completed actions
- System status"
```

---

### 5. Log Entry Skill

**Purpose:** Create audit log entries for all actions.

**Trigger:** Every action taken by the AI

**Output:** JSON log entry in `/Logs/YYYY-MM-DD.json`

**Template:**
```json
{
  "timestamp": "2026-02-28T10:30:00Z",
  "action_type": "file_process",
  "actor": "qwen_code",
  "target": "filename.md",
  "parameters": {"category": "document"},
  "approval_status": "not_required",
  "result": "success",
  "notes": "File categorized and moved to Done"
}
```

**Usage with Qwen Code:**
```bash
qwen "Log this action: [describe action] to /Logs/today.json"
```

---

### 6. File Categorization Skill

**Purpose:** Automatically categorize incoming files.

**Categories:**
- `document` - General documents
- `invoice` - Billing/invoice files
- `task` - Task requests
- `communication` - Emails, messages
- `financial` - Bank statements, receipts
- `reference` - Reference materials

**Usage with Qwen Code:**
```bash
qwen "Categorize this file and add appropriate metadata:
- Determine the file type
- Extract key information (dates, amounts, names)
- Add category tag to frontmatter"
```

---

### 7. Response Drafting Skill

**Purpose:** Draft responses to communications.

**Trigger:** Communication file in `/Needs_Action`

**Output:** Draft response in same file or linked file

**Guidelines:**
- Professional tone
- Concise and clear
- Include relevant context
- Mark as AI-drafted

**Template:**
```markdown
## Draft Response

**To:** [Recipient]
**Subject:** Re: [Original Subject]

[Response content]

---
*Drafted by AI Employee - Review before sending*
```

**Usage with Qwen Code:**
```bash
qwen "Draft a professional response to this communication. Keep it concise and helpful."
```

---

### 8. Daily Briefing Skill

**Purpose:** Generate daily summary of activities.

**Trigger:** Scheduled (daily) or on-demand

**Output:** Briefing file in `/Briefings/YYYY-MM-DD_Briefing.md`

**Template:**
```markdown
---
generated: YYYY-MM-DDTHH:MM:SS
period: YYYY-MM-DD
---

# Daily Briefing

## Summary
- Files processed: X
- Tasks completed: Y
- Pending approvals: Z

## Completed Today
[List of completed tasks]

## Pending
[Items awaiting action/approval]

## Tomorrow's Priorities
[Suggested focus areas]
```

**Usage with Qwen Code:**
```bash
qwen "Generate a daily briefing summarizing:
- All files processed today
- Tasks completed
- Items still pending
- Recommendations for tomorrow"
```

---

## 🔧 Skill Implementation Guide

### Creating a New Skill

1. **Define the purpose:** What problem does this skill solve?
2. **Identify the trigger:** When should this skill be used?
3. **Specify the output:** What does the skill produce?
4. **Document usage:** How does Qwen Code invoke this skill?

### Skill Registration

Add new skills to this document with:
- Clear name and purpose
- Trigger conditions
- Input/output specifications
- Example usage with Qwen Code

---

## 📖 Skill Usage Examples

### Example 1: Processing a Dropped File

```bash
# User drops a file in /Inbox
# File System Watcher detects and moves to /Needs_Action

# Qwen Code processes:
qwen "Process the new file in /Needs_Action:
1. Read and understand the content
2. Categorize it appropriately
3. Create an action plan if needed
4. Execute or request approval
5. Move to /Done when complete"
```

### Example 2: Multi-Step Task

```bash
# Complex request requiring multiple actions
qwen "Create a plan for this request:
1. Break down into individual steps
2. Identify which steps need approval
3. Execute auto-approved steps
4. Create approval requests for others
5. Track progress in the plan file"
```

### Example 3: Approval Workflow

```bash
# Action requires human approval
qwen "This payment requires approval:
1. Create approval request in /Pending_Approval
2. Include all payment details
3. Explain why approval is needed
4. Provide clear approve/reject instructions"

# After human approves (moves to /Approved):
qwen "Execute the approved action and log the result"
```

---

## 🎯 Best Practices

### For Skill Users (Qwen Code)

1. **Always log actions** - Every action should be traceable
2. **Request approval when unsure** - Better to over-communicate
3. **Update Dashboard** - Keep status current
4. **Move files appropriately** - Maintain folder hygiene
5. **Document decisions** - Explain why actions were taken

### For Skill Developers

1. **Keep skills focused** - One responsibility per skill
2. **Make skills composable** - Skills should work together
3. **Handle errors gracefully** - Don't crash, log and continue
4. **Document thoroughly** - Clear usage examples
5. **Test edge cases** - What happens with invalid input?

---

## 🔄 Skill Evolution

Skills should evolve as the AI Employee matures:

| Tier | Skills Focus |
|------|--------------|
| Bronze | Basic file processing, planning, logging |
| Silver | Email integration, social media, scheduling |
| Gold | Full autonomy, accounting, multi-domain |
| Platinum | Cloud deployment, A2A communication |

---

*This document is maintained as part of the Bronze Tier deliverables.*
*Update as new skills are developed.*
