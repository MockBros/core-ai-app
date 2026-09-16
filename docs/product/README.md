# DeepInterview Product Docs

This directory is reserved for current DeepInterview product behavior derived
from accepted intent. The harness ships no fabricated product domains or
defaults. Product authority remains with the maintained root READMEs,
architecture and deployment docs, accepted decisions, implementation, tests,
and observed behavior in its named environment.

## Current Product Contract

No product-specific contract is pre-populated here. Start with
[`../../README.md`](../../README.md), [`../ARCHITECTURE.md`](../ARCHITECTURE.md),
[`../DEPLOY.md`](../DEPLOY.md), [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md),
and [`../../SECURITY.md`](../../SECURITY.md), then add a focused living product
document only when an owner accepts the behavior. Do not treat this empty index
as permission to choose product policy.

## Update Rule

When DeepInterview behavior changes:

1. Update the affected product document when expected behavior changes.
2. Update the active execution plan when complex work uses one.
3. Add a lasting decision only when future work must inherit a consequential
   product, architecture, data, security, compatibility, or validation choice.
4. Add or update executable proof that exercises the behavior.

Keep offline/mock, local-process, Compose, real-provider/LiveKit, and hosted
evidence distinct. A current implementation detail or passing test is not, by
itself, a new product contract.
