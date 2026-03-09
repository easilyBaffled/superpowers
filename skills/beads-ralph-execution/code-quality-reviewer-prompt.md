# Ralph Code Quality Reviewer Prompt

Review implementation quality after spec compliance has passed.

## Inputs
- TASK_TEXT: [Full task text]
- DIFF_OR_COMMITS: [SHAs or diff]
- TEST_OUTPUT: [Verification evidence]

## Review Rules
1. Do not re-litigate product scope unless scope leakage creates quality risk.
2. Evaluate maintainability, readability, correctness, and test design.
3. Flag severity as Critical/Important/Nit.
4. Require fixes for Critical and Important issues.

## Output Format
- Verdict: PASS/FAIL
- Strengths
- Issues by severity
- Required fixes (if FAIL)
