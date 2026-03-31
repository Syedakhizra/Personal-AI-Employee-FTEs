# HITL Approval Skill

**Tier:** Silver  
**Version:** 1.0  
**Created:** 2026-03-27  
**Status:** Ready to Implement

---

## 📋 Overview

The **Human-in-the-Loop (HITL) Approval Skill** enables the AI Employee to request human approval before executing sensitive actions, ensuring safe and controlled autonomy.

---

## 🎯 Purpose

Create approval request files for sensitive actions, wait for human decision (approve/reject), and execute only approved actions.

---

## ⚡ Quick Start

```bash
# Create approval request
qwen "This payment requires approval. Create approval request in Pending_Approval folder" --approval-mode yolo

# Execute approved actions
qwen "Execute all approved actions in Approved folder" --approval-mode yolo
```

---

## 📁 Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/
│   └── PAYMENT_Client_A_2026-03-27.md    # Awaiting approval
├── Approved/
│   └── PAYMENT_Client_A_2026-03-27.md    # Approved, ready to execute
├── Rejected/
│   └── PAYMENT_Client_A_2026-03-27.md    # Rejected
└── Done/
    └── PAYMENT_Client_A_2026-03-27.md    # Completed
```

---

## 📤 Approval Request Template

```markdown
---
type: approval_request
action: payment
created: 2026-03-27T10:30:00
priority: high
status: pending
amount: 500.00
recipient: Client A
---

# Approval Required

## Action Details
- **Action:** Send Payment
- **To:** Client A (client@example.com)
- **Amount:** $500.00
- **Invoice:** #123
- **Reason:** Payment for services rendered
- **Due Date:** 2026-03-30

## Payment Details
- **Bank:** ABC Bank
- **Account:** ****1234
- **Reference:** INV-123

## Why Approval is Needed
Company policy requires human approval for all payments over $100.

---

## To Approve
Move this file to `/Approved/` folder.

## To Reject
Move this file to `/Rejected/` folder.

## Deadline
Please respond within 24 hours or this will be escalated.

---
*Created by AI Employee at 2026-03-27T10:30:00*
```

---

## 🎓 Usage Examples

### Example 1: Payment Approval

```bash
qwen "This invoice payment of $500 requires approval.
Create approval request with:
- Recipient details
- Amount
- Invoice reference
- Reason for payment
Save to Pending_Approval" --approval-mode yolo
```

### Example 2: Email Approval

```bash
qwen "This email to new client requires approval.
Create approval request with email preview.
Save to Pending_Approval/Email/" --approval-mode yolo
```

### Example 3: Execute Approved

```bash
qwen "Check Approved folder for pending actions.
Execute each approved action:
1. Read approval file
2. Perform the action
3. Move to Done
4. Log the result" --approval-mode yolo
```

---

## 🔄 Workflow

```
┌─────────────────────────────────────────┐
│ 1. AI detects action requiring approval │
│    (payment, new contact, sensitive)    │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Creates approval request file        │
│    - Action details                     │
│    - Why approval needed                │
│    - Clear approve/reject instructions  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 3. Saves to Pending_Approval/           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 4. Human reviews decision               │
│    Approve → Move to Approved/          │
│    Reject → Move to Rejected/           │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│ Approved      │       │ Rejected      │
│ Execute action│       │ Log & archive │
└───────────────┘       └───────────────┘
        │
        ▼
┌───────────────┐
│ Move to Done  │
│ Log result    │
└───────────────┘
```

---

## 🏷️ Approval Thresholds

| Action Category | Auto-Approve | Require Approval |
|-----------------|--------------|------------------|
| **Email replies** | Known contacts | New recipients |
| **Social media** | Scheduled posts | Replies, DMs |
| **Payments** | ❌ Never | ✅ All payments |
| **File operations** | Internal folders | External sharing |
| **Calendar** | Internal meetings | External meetings |
| **Data changes** | Read-only | Write/delete |

---

## 📊 Approval Status

| Status | Location | Action |
|--------|----------|--------|
| `pending` | Pending_Approval/ | Awaiting human |
| `approved` | Approved/ | Ready to execute |
| `rejected` | Rejected/ | Archive with reason |
| `completed` | Done/ | Executed and logged |

---

## 🔒 Security Notes

| Rule | Description |
|------|-------------|
| **Never bypass** | Always create approval file |
| **Clear details** | Include all action details |
| **Deadline** | Set response deadline |
| **Audit trail** | Log all approvals |
| **Escalation** | Escalate if no response |

---

## 🛠️ Troubleshooting

### Issue: "Approval file not detected"

**Solution:**
- Check file is in correct folder
- Verify status: pending
- Check orchestrator is running

### Issue: "Action executed without approval"

**Solution:**
- Review approval thresholds
- Add more strict rules
- Enable additional logging

---

## ✅ Testing Checklist

- [ ] Approval request created
- [ ] File saved to Pending_Approval
- [ ] Human can approve (move file)
- [ ] Approved action executes
- [ ] Rejected action archives
- [ ] Logs created

---

*HITL Approval Skill v1.0 - Silver Tier*
