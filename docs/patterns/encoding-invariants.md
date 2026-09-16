# DeepInterview Encoding Invariants

Use this pattern to convert an accepted architecture, reliability, security, or
quality rule into repository-native validation. The repository remains the
system of record; a check enforces policy but does not create it.

Follow the authority gate in the [DeepInterview workflow](../WORKFLOW.md)
before editing.

## 1. Establish Authority

Locate an accepted document or explicit owner decision that says what must be
true. Record its path and exact rule. Code organization, repeated patterns,
tests, tool defaults, configurable examples, and undocumented preferences show
current behavior or convention; they do not authorize a new invariant.

Stop before editing when no accepted authority exists or when two materially
different boundaries fit the words. Ask for the smallest missing choice.

Example: the DeepInterview cross-language boundary is ambiguous until the
accepted contract owner identifies the source and all mirrors. The maintained
contract sequence is:

```text
packages/shared/src
  -> apps/agent/shared_models.py
  -> packages/shared/schema
  -> TypeScript round-trip/invariant tests
  -> Python parity/round-trip tests
  -> persisted fixture/default compatibility
```

When an owner accepts a rule for that boundary, it is mechanical enough to
encode only across the named scope. A repeated import pattern or a default in
`apps/agent` is not authority to invent a new contract.

## 2. Define The Boundary

Write the invariant before choosing a tool:

| Field | Required content |
| --- | --- |
| Authority | Accepted source and exact rule |
| Scope | Files, modules, configuration, or runtime objects covered |
| Allowed | At least one conforming example |
| Forbidden | The precise structure or behavior to reject |
| Exceptions | Only exceptions stated by the same authority |
| Diagnostic | Violating item, broken rule, authority pointer, and next action |

Keep adjacent preferences outside the check. If authority forbids one dependency
direction, do not also enforce naming, layout, or style conventions.

## 3. Reuse Native Validation

Find DeepInterview's existing validation owner: for example, its test target,
task runner, build command, linter configuration, policy scanner, or validation
script. Integrate there so maintainers discover and run one normal command.

Implement the smallest deterministic check at the lowest layer that can inspect
the whole accepted scope. Reuse an existing rule mechanism when it expresses the
boundary clearly. Do not introduce a new framework, language, linter, or service
just because it could enforce the rule.

The failure must be actionable. Prefer a diagnostic such as:

```text
public/orders imports internal/storage: public packages must not import internal
packages (docs/architecture.md). Depend on the public storage interface instead.
```

Avoid bare messages such as `validation failed` or diagnostics that require the
reader to reverse-engineer the rule.

## 4. Prove Both Directions

Run proof through the repository-native owner:

- **Positive proof:** a known allowed case passes. This catches checks that ban
  valid behavior or scan the wrong scope.
- **Negative proof:** a targeted forbidden fixture or temporary test mutation
  fails, and the assertion verifies the intended diagnostic or rule identifier.

Keep negative proof isolated and recoverable. Do not leave a violating product
file in the DeepInterview working tree. A passing repository with no exercised
violation does not prove that the guard can detect recurrence.

## 5. Discover And Report Enforcement

Inspect how validation is reached without changing external state:

| Level | What can be claimed |
| --- | --- |
| Local validation | The owning command exists; state whether it was run and passed |
| Optional hook | A convenience entrypoint may run the command; do not install or require it without authority |
| CI | A checked-in workflow invokes the command, or no invocation was found |
| Branch protection | Required checks or merge blocking are verified externally, or remain unverified |

A checked-in CI job does not prove that it ran on the current revision. A green
job does not prove branch protection requires it. Never claim merge blocking
from workflow text alone. Do not install hooks, select a CI provider, prescribe a
merge policy, or mutate branch protection as part of encoding a repository rule.

## Handback

Report, in order:

1. accepted authority and encoded scope;
2. validation owner and smallest check added;
3. positive and negative proof with observed results;
4. local, optional-hook, CI, and branch-protection levels separately; and
5. gaps, exceptions, and unverified external enforcement.
