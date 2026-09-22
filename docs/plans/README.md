# DeepInterview Execution Plans

Execution plans are Git-native working memory for complex DeepInterview tasks.
They preserve enough outcome, authority, scope, approach, risk, progress, and
validation context for another agent or human to resume without reconstructing
intent from chat history or a partial diff.

## When To Create A Plan

Use an ephemeral plan for bounded, single-session work. Create one durable plan
under [`active/`](active/) when work spans sessions, coordinates contributors,
has meaningful dependencies or ordering, requires recovery, or would be unsafe
to resume from the diff alone.

Use [`../templates/exec-plan.md`](../templates/exec-plan.md). For an explicitly
authorized baseline-to-rerun Harness experiment, use
[`../templates/harness-improvement.md`](../templates/harness-improvement.md)
and keep its fresh-rerun status explicit.

## Lifecycle

```text
docs/plans/active/<slug>.md
  -> update progress, decisions, and validation during implementation
  -> (pause: record date, reason, and resume condition)
     docs/plans/deferred/<slug>.md
  -> (resume: move back and set Status to Active)
     docs/plans/active/<slug>.md
  -> (complete: record the verified result)
     docs/plans/completed/<slug>.md
```

Plans in `active/` are the current durable task artifacts. A plan in
`deferred/` is intentionally paused working memory, not a current instruction;
it must state why it is paused and what permits resumption. Promote a lasting
product or architecture decision into [`../decisions/`](../decisions/); keep
task-local choices in the plan. Move a plan to `completed/` only after its
requested outcome and evidence are recorded. Completed plans are historical
evidence, not default task instructions.

## Plan Indexes

- [`active/README.md`](active/README.md): where current durable plans live.
- [`deferred/README.md`](deferred/README.md): paused plans and resumption rules.
- [`completed/README.md`](completed/README.md): lifecycle and historical-plan
  retention guidance.
