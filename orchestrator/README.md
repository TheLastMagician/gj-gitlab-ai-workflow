# Orchestrator Skeleton

This directory contains a minimal, dependency-free routing skeleton for GitLab
webhook events and slash commands. It is intentionally not production-ready yet.

Production work still needed:

- Authenticate webhook requests.
- Fetch Issue, MR, diff, pipeline, and comments through GitLab API.
- Load `.gj/workflow.yml` and `.gj/context.yml`.
- Call an AI gateway with redaction, timeout, retry, and audit logging.
- Write comments back to GitLab.
- Keep workflow status labels mutually exclusive.
