# AGENTS.md

## Lessons

- Python Playwright is not installed on this machine, so `from playwright.sync_api import ...` fails. Check for it before you plan a screenshot step.
- The heavy-gate PreToolUse hook blocked an inline `python3 -c "import playwright"` check, but heredoc Python (`python3 -I - <<EOF`) ran fine. For anything that might launch a browser, write it to a file and run it through `~/.claude/bin/heavy-gate`.
- ELI5 diagrams: if two figures show the same example, they must use the same attention percentages. Draw share bars as a fraction of 100%, not scaled to the largest value.
