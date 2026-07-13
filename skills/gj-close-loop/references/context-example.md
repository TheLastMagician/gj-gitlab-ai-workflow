# Demo Run Reference

Context outputs from the first run:

- `examples/demo-run/iteration-docs/ai-context-summary.md`
- `docs/iterations/2026-07-v1.0-order-approval/ai-context-summary.md`
- `docs/context/current-state.md`
- `docs/modules/order.md`
- `.gj/context.yml`

Durable facts extracted:

- Self-approval is forbidden.
- Docker executor is the stable CI runner path for this demo.
- Local token helpers are ignored and must not be packaged.

Historical-only facts:

- The first failed policy job was a runner pull-policy issue, not a workflow
  policy failure.
