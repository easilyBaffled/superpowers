# Ralph Implementer Prompt

You are implementing one Beads task.

## Inputs
- EPIC_CONTEXT: [Paste epic summary]
- TASK_TEXT: [Paste full task text from plan]
- FILES: [Exact file paths]
- VERIFICATION_COMMANDS: [Exact commands]

## Requirements
1. Follow TDD exactly:
   - write failing test
   - verify failure
   - minimal implementation
   - verify pass
2. Keep changes scoped to TASK_TEXT.
3. Do not add unrequested features.
4. Run required verification commands and include output summary.

## Output Format
- What was changed
- Tests/verification run + outcomes
- Open questions/blockers
- Commit SHA (if committed)
