# DeepInterview Application Runbook: Surface

Use this template only after DeepInterview evidence establishes the commands
and behavior. A heading with no verified content is a gap, not an operational
instruction. Keep offline/mock, local-process, Compose, real-provider/LiveKit,
and hosted evidence separate.

## Scope

Name the DeepInterview application surface, owning module, and jobs this
runbook supports.

## Prerequisites

List required runtimes, dependencies, services, credentials, and safe checks;
link each prerequisite to the DeepInterview owning authority.

## Start

Record the exact command, process or Compose project identity, ports, and
writable state. Distinguish fixed, defaulted, configurable, and observed values.

## Readiness

Name the observable condition that proves startup completed.

## Deterministic State

Explain how to create, select, or reset the scenario without touching unowned
state. Do not add a reset or cleanup obligation without authority.

## Interface

Describe how to exercise the relevant browser, API, CLI, worker, or service.

## Runtime Evidence

Give retrieval commands for logs, traces, errors, and correlation identifiers.
Distinguish guaranteed fields from optional ones.

## Ownership And Cleanup

Explain how to identify resources created by this run and stop only those
resources. Keep missing cleanup policy under Unknowns.

## Validation

Name focused checks and the real-interface journey that prove the outcome.
State what the evidence does not establish, such as provider, LiveKit,
dependency-readiness, or hosted behavior.

## Unknowns

List missing facts or decisions that an agent must not invent.
