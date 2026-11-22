# ADR-0004: Exactly one campaign clock, inside the core

**Status:** Proposed · **Date:** 2026-11-22

## Context

The LoC campaign advances on a schedule: shop drops during a turn, then at turn end restocking, turn awards, the next turn and faction resets (turn 3 and 5), and at round end round awards and a new round. If more than one service did this, awards would be granted twice and turns would drift apart.

## Decision

- The campaign clock runs only in steelcore, as a single scheduler with a database lock (leader election), so a second core instance can never tick in parallel.
- Every transition is idempotent (keyed by round and turn) and published as an event: `turn_started`, `turn_ended`, `round_ended`, `awards_granted`, `shop_restocked`.
- Campaign rules (points, award VTs per faction, shop drops, turn length) are one versioned configuration in the core. Changes take effect at a turn boundary.

## Consequences

- **+** One source of truth for "which round and turn is it".
- **+** Gateways and bots react to events instead of polling.
- **−** Gateways have no clock of their own; if the core is down, the campaign pauses (by design).
