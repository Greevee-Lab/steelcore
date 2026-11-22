# ADR-0001: Gateways use the Core API, never the database

**Status:** Proposed · **Date:** 2026-11-22

## Context

Several providers (Insignia, Steelbound, Brainbox, community services) need to read and write one shared campaign. One idea was a single PostgreSQL database with one endpoint per provider, each connecting directly with its own database user.

## Decision

Only steelcore talks to the database. Every provider gateway uses the versioned **Core API** (`steelcore.v1`). Each gateway has its own credentials and scopes.

## Consequences

- **+** Campaign rules, plausibility checks, the campaign clock and auditing live in one place, and no gateway can bypass them.
- **+** The schema can change without coordinating every provider. Only the API contract is stable.
- **+** Per-provider rate limits, trust levels and voiding become possible.
- **−** An extra network hop and one more service to run.
- **−** The existing campaign server has to be split into a protocol part (gateway) and a rules part (core). See the migration path in the [concept](../concept.md#4-the-plan-fork-then-evaluate-steelbound).

## Alternatives considered

- **Shared database, one DB user per provider:** fastest to start. But logic gets duplicated across services, schema changes break everyone, and permissions can only be enforced per table, not per campaign rule.
- **Phased:** shared DB first, API later. Still possible as a temporary step during migration, but not the target.
