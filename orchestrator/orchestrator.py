#!/usr/bin/env python3
"""Minimal command router for the GJ GitLab AI workflow."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any


COMMAND_TO_SKILL = {
    "/ai-triage": "gj-workflow-triage",
    "/ai-analyze": "gj-requirement-refine",
    "/ai-draft-solution": "gj-solution-plan",
    "/ai-split-tasks": "gj-issue-split",
    "/ai-load-context": "gj-dev-context",
    "/ai-update-context": "gj-context-extract",
    "/ai-review-mr": "gj-mr-review",
    "/ai-bug-fix": "gj-bug-fix",
    "/ai-hotfix": "gj-hotfix",
    "/ai-test-cases": "gj-test-design",
    "/ai-release-note": "gj-release-prep",
    "/ai-retro": "gj-retro-learnings",
}


@dataclass(frozen=True)
class Route:
    event: str
    skill: str
    reason: str


def command_from_text(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in COMMAND_TO_SKILL:
            return stripped
    return None


def route_event(payload: dict[str, Any]) -> Route | None:
    event = str(payload.get("object_kind") or payload.get("event_type") or "unknown")

    if event == "note":
        note = payload.get("object_attributes", {}).get("note", "")
        command = command_from_text(note)
        if command:
            return Route(event=event, skill=COMMAND_TO_SKILL[command], reason=f"comment command {command}")

    if event == "issue":
        labels = {label.get("title") for label in payload.get("labels", []) if isinstance(label, dict)}
        if "type-bug" in labels:
            return Route(event=event, skill="gj-bug-fix", reason="issue opened with type-bug")
        if "type-hotfix" in labels:
            return Route(event=event, skill="gj-hotfix", reason="issue opened with type-hotfix")
        if "type-requirement" in labels:
            return Route(event=event, skill="gj-requirement-refine", reason="issue opened with type-requirement")

    if event == "merge_request":
        attrs = payload.get("object_attributes", {})
        if attrs.get("work_in_progress") is False or attrs.get("draft") is False:
            return Route(event=event, skill="gj-mr-review", reason="merge request ready for review")

    if event == "pipeline":
        attrs = payload.get("object_attributes", {})
        if attrs.get("status") == "failed":
            return Route(event=event, skill="gj-workflow-triage", reason="pipeline failed")

    return None


def main() -> int:
    payload = json.load(sys.stdin)
    route = route_event(payload)
    if route is None:
        print(json.dumps({"route": None}, ensure_ascii=False))
        return 0

    print(json.dumps(route.__dict__, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
