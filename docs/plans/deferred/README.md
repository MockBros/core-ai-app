# Deferred DeepInterview Execution Plans

This directory holds plans that are intentionally paused before their outcome
and evidence are complete. Deferred plans preserve recovery context, but they
are not current work instructions.

To defer a plan:

1. Set its status to `Deferred`.
2. Record the date, reason, and concrete resume condition in its `Deferral`
   section.
3. Move it from [`../active/`](../active/) into this directory without
   discarding progress, decisions, validation, or risks.

To resume a plan, move it back to [`../active/`](../active/), set its status to
`Active`, and update progress and validation before continuing. Move it to
[`../completed/`](../completed/) only after the requested outcome and evidence
are recorded.
