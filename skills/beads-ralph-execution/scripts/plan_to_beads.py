#!/usr/bin/env python3
"""Convert a Superpowers implementation plan markdown file into Beads import JSON.

Usage:
  python skills/beads-ralph-execution/scripts/plan_to_beads.py docs/plans/plan.md
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TASK_HEADER_RE = re.compile(r"^###\s+Task\s+(\d+):\s+(.+)$")
STEP_RE = re.compile(r"^\*\*Step\s+(\d+):\s+(.+)\*\*$")


def parse_plan(markdown: str) -> list[dict]:
    tasks: list[dict] = []
    current: dict | None = None

    for raw_line in markdown.splitlines():
        line = raw_line.strip()

        task_match = TASK_HEADER_RE.match(line)
        if task_match:
            if current:
                tasks.append(current)
            current = {
                "task_number": int(task_match.group(1)),
                "title": task_match.group(2).strip(),
                "steps": [],
            }
            continue

        if current is None:
            continue

        step_match = STEP_RE.match(line)
        if step_match:
            current["steps"].append(
                {
                    "step_number": int(step_match.group(1)),
                    "instruction": step_match.group(2).strip(),
                }
            )

    if current:
        tasks.append(current)

    return tasks


def build_beads_payload(plan_path: Path, tasks: list[dict]) -> dict:
    epic_title = plan_path.stem
    return {
        "epics": [
            {
                "title": epic_title,
                "source_plan": str(plan_path),
                "tasks": [
                    {
                        "external_id": f"task-{task['task_number']}",
                        "title": task["title"],
                        "description": "\n".join(
                            [f"Step {s['step_number']}: {s['instruction']}" for s in task["steps"]]
                        ),
                        "acceptance_criteria": [
                            "Task steps completed in order",
                            "Verification commands executed with evidence",
                        ],
                    }
                    for task in tasks
                ],
            }
        ]
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "Usage: python skills/beads-ralph-execution/scripts/plan_to_beads.py <plan.md>",
            file=sys.stderr,
        )
        return 1

    plan_path = Path(sys.argv[1])
    if not plan_path.exists():
        print(f"Plan not found: {plan_path}", file=sys.stderr)
        return 2

    markdown = plan_path.read_text(encoding="utf-8")
    tasks = parse_plan(markdown)
    if not tasks:
        print("No tasks found. Expected headings like: ### Task N: Title", file=sys.stderr)
        return 3

    payload = build_beads_payload(plan_path, tasks)
    json.dump(payload, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
