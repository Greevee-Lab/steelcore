# ADR-0002: The existing account UUID becomes the player_id

**Status:** Proposed · **Date:** 2026-11-22

## Context

The current LoC campaign database keys accounts, garage, awards and leaderboard on the XUID, stored as a UUID. To support several providers, ownership has to move from "provider account" to "campaign player".

## Decision

- Add a `players` table and an `identities` table (`provider`, `external_id` → `player_id`).
- **Every existing account UUID is reused as its `player_id`.** Each existing account gets one identity `(insignia, <XUID>)`.
- New players of a provider with XUID-like ids get the same derivation: Steelbound maps its account id to the pseudo-XUID `0x53424C01_<account id>` and then to the UUID (see the [FAQ](../faq.md#which-xuid-range-do-non-xbox-clients-use)). Providers without such an id get a random UUID v4 (or v7) that cannot collide with the XUID-derived values.

## Consequences

- **+** No campaign rows change. Garage, awards and leaderboard keep their keys.
- **+** Phase 1 of the migration is a pure schema addition plus a backfill, and can be rolled back.
- **−** For legacy players, `player_id` and XUID are numerically related. That is acceptable because nothing outside the core sees the `player_id`, but it should never be used to infer an XUID.

## Alternatives considered

- **New random player_id for everyone:** cleaner, but every foreign key has to be rewritten in one risky migration.

## Implementation (2026-11-25)

In the [fork](https://github.com/Greevee-Lab/sbcampaign): `sql/fork/identity.sql` adds `provider`, `player`, `identity` and `audit_log` without altering upstream tables and backfills existing accounts; `resolve_identity` in `src/campaign_core/identity.rs` creates player and identity on first contact. The Insignia provider is prepared and disabled.
