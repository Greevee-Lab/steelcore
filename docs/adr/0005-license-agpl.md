# ADR-0005: License steelcore under AGPL-3.0

**Status:** Accepted · **Date:** 2026-11-22

## Context

steelcore is meant to be run by different people and connected to by several independent projects. Anyone should be able to host it, but a hosted, modified core should not turn into a closed fork the community cannot inspect.

## Decision

steelcore is licensed under the **GNU Affero General Public License v3.0**.

## Consequences

- **+** Anyone may run, study and modify it. Changes to a publicly hosted core must be published.
- **+** Compatible with GPL-3.0 projects in the LoC community.
- **+** Gateways talk to the core over a network API and can be licensed independently. Only code that is linked into the core falls under the AGPL.
- **−** Some contributors avoid AGPL code. Shared libraries (for example an API client) can be published under a more permissive license if needed.
