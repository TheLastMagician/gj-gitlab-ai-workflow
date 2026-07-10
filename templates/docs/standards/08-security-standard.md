# Security Standard

- Do not send secrets, tokens, certificates, customer private data, or raw
  production logs to AI.
- Mask sensitive values before writing comments or docs.
- Auth, permission, and orchestrator changes cannot use `flow::fast`. Require
  Standard or Hotfix evidence and a human with merge permission to make the
  final merge decision.
