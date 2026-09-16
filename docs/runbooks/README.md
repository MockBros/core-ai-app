# DeepInterview Runbook Index

Runbooks are maintained DeepInterview operating guidance. Use only a path whose
prerequisites, owner, interface, evidence boundary, and cleanup behavior are
documented by the linked source. A template heading is not proof that a command
or credential is approved.

## Verified Sources

| Surface | Source | Evidence boundary |
| --- | --- | --- |
| Offline/mock development and tests | [`../../README.md`](../../README.md), [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md) | Local deterministic code and mock-provider behavior without external provider credentials. |
| Local model processes | [`../LOCAL_MODELS.md`](../LOCAL_MODELS.md) | Separately started local model and real-time transport paths; read its caveats before calling a run fully offline. |
| Compose and deployment | [`../DEPLOY.md`](../DEPLOY.md) | Compose syntax, image/build behavior, or an explicitly owned stack; configuration output is not runtime/provider/hosted readiness. |
| Agent surface | [`../../apps/agent/AGENTS.md`](../../apps/agent/AGENTS.md) | Current agent API/worker notes and their stated offline limits. |
| Knowledge sidecar | [`../../services/lightrag/README.md`](../../services/lightrag/README.md) | Sidecar endpoints and backend behavior; the functional default and alternate backend evidence remain separate. |
| CLI traces and repository setup | [`../../cli/`](../../cli/) and [`../DEPLOY.md`](../DEPLOY.md) | CLI capabilities and local trace retrieval where the owning docs support them. |
| Hosted operations | [`../DEPLOY.md`](../DEPLOY.md) | Deployed infrastructure only after the documented manual gates and environment are observed. |

## Operating Rules

Label every result as **offline/mock**, **local-process**, **Compose**,
**real-provider/LiveKit**, or **hosted**. Do not promote a liveness endpoint,
Compose syntax check, image build, or offline test into provider, LiveKit,
dependency-readiness, or hosted proof.

The index does not invent credentials, retention, cleanup, or deployment
obligations. Identify the resources owned by a run and follow cleanup only when
the owning DeepInterview source authorizes it. Record missing `uv`, Docker, provider,
LiveKit, device, or hosted prerequisites as unavailable evidence.

Use [`../templates/application-runbook.md`](../templates/application-runbook.md)
to structure a proposed runbook when no maintained source exists; it supplies
headings, not commands or policy.
