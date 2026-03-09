---
name: beads-ralph-execution
description: Use when a written implementation plan should be converted into Beads epics/tasks and executed by Ralph-managed fresh Claude/Cursor instances with strict TDD + verification gates
---

# Beads + Ralph Execution

Execute implementation plans by converting tasks into Beads epics/tasks, then dispatching fresh Ralph-managed Claude/Cursor instances per task with mandatory spec and quality review loops.

**Core principle:** Plan-first execution with deterministic task tracking (Beads), fresh task context (Ralph instances), and strict quality gates.

**Announce at start:** "I'm using the beads-ralph-execution skill to run this plan through Beads and Ralph."

## Default Selection Rule

This is the default execution skill whenever a plan is ready for implementation and Beads/Ralph is available.

Only defer to `subagent-driven-development` or `executing-plans` when the user explicitly opts out or infrastructure is unavailable.

## Required Inputs

- Plan file path: `docs/plans/YYYY-MM-DD-<feature>.md`
- Beads project/repo context
- Ralph execution command/API available in environment

## Process

### Step 1: Load and Validate Plan
1. Read the plan once.
2. Extract epics and tasks from `### Task N` sections.
3. Confirm each task has:
   - files to touch
   - explicit verification command(s)
   - acceptance criteria
4. If gaps exist, stop and ask for clarification before execution.

### Step 2: Convert Plan to Beads Work Items
Use `scripts/plan_to_beads.py` to convert plan markdown into structured JSON for Beads import.

```bash
python skills/beads-ralph-execution/scripts/plan_to_beads.py docs/plans/<plan>.md > /tmp/beads-import.json
```

Then import into Beads using your environment's Beads CLI/API.

### Step 3: Execute Tasks via Ralph (One Task at a Time)
For each task in dependency order:
1. Mark task `in_progress` in Beads
2. Dispatch Ralph implementer instance with:
   - full task text
   - surrounding epic context
   - required TDD constraints
3. Run **spec compliance review** (separate Ralph reviewer)
4. If spec fails, loop back to implementer fixes, then re-review
5. Run **code quality review** (separate Ralph reviewer)
6. If quality fails, loop back to implementer fixes, then re-review
7. Run verification commands from task and capture evidence
8. Mark task `done` in Beads only after all gates pass

## Gate Order (Mandatory)

1. Implement
2. Spec compliance review ✅
3. Code quality review ✅
4. Verification evidence ✅
5. Mark task complete

Never run code quality review before spec compliance is approved.

## Verification Requirements

Before any claim like "done", "fixed", or "ready":
- Run the exact verification command(s) from the task
- Read full output and exit code
- Report evidence, not assumptions

Use `superpowers:verification-before-completion` as a hard gate for every task completion and epic completion claim.

## Epic Completion

When all tasks in an epic are done and verified:
1. Re-run epic-level verification bundle
2. Announce readiness
3. Invoke `superpowers:finishing-a-development-branch` to choose merge/PR/keep/discard path

## Prompt Templates

Use these templates when dispatching Ralph instances:
- `./implementer-prompt.md`
- `./spec-reviewer-prompt.md`
- `./code-quality-reviewer-prompt.md`

## Red Flags

**Never:**
- Execute multiple Ralph implementers in parallel on same branch
- Mark Beads task complete before verification evidence
- Skip re-review loops after fixes
- Accept "close enough" on spec compliance
- Start work on main/master without explicit approval

## Integration

**Required workflow skills:**
- `superpowers:using-git-worktrees` - isolate execution workspace first
- `superpowers:writing-plans` - source plan generation
- `superpowers:test-driven-development` - implementer discipline
- `superpowers:verification-before-completion` - evidence gate before claims
- `superpowers:finishing-a-development-branch` - completion and integration choice

**Replaces for this workflow:**
- `superpowers:subagent-driven-development` when execution is handled by Ralph-managed external instances
