#!/usr/bin/env python3
"""Minimal command router for the GJ GitLab AI workflow."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any


COMMAND_TO_SKILL = {
    "/ai-next": "gj-workflow-next",
    "/ai-plan": "gj-plan-change",
    "/ai-develop": "gj-develop-change",
    "/ai-review": "gj-mr-review",
    "/ai-release": "gj-release-readiness",
    "/ai-close": "gj-close-loop",
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
        flow_labels = labels & {"flow::fast", "flow::standard", "flow::hotfix"}
        if "type-hotfix" in labels and "flow::hotfix" in flow_labels:
            return Route(event=event, skill="gj-develop-change", reason="confirmed hotfix issue")
        if "type-bug" in labels and len(flow_labels) == 1:
            return Route(event=event, skill="gj-develop-change", reason="bug issue with confirmed flow")
        if "type-bug" in labels:
            return Route(event=event, skill="gj-workflow-next", reason="bug issue needs flow confirmation")
        if "type-requirement" in labels:
            return Route(event=event, skill="gj-plan-change", reason="requirement issue needs a change plan")
        return Route(event=event, skill="gj-workflow-next", reason="issue needs workflow routing")

    if event == "merge_request":
        attrs = payload.get("object_attributes", {})
        if attrs.get("work_in_progress") is False or attrs.get("draft") is False:
            return Route(event=event, skill="gj-mr-review", reason="merge request ready for review")

    if event == "pipeline":
        attrs = payload.get("object_attributes", {})
        if attrs.get("status") == "failed":
            return Route(event=event, skill="gj-workflow-next", reason="pipeline failed")

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
