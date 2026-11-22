# ADR-0003: Account linking by link code, admin merge as fallback

**Status:** Proposed · **Date:** 2026-11-22

## Context

Players will use more than one client and want to keep one pilot. The core must know that `insignia:<XUID>` and `steelbound:<account>` are the same person without trusting a bare claim.

## Decision

Three ways, in this order:

1. **Link code (default):** a short-lived code (for example 15 minutes, one use) is shown on a client where the player is already signed in and redeemed on the other. For the original game, the Insignia gateway shows the code in the per-session message of the day.
2. **Admin merge (fallback):** for players who cannot use a link code (for example a lost login). Reviewed by a campaign admin, audited and reversible.
3. **Unlinked:** always allowed. An unlinked account is simply its own player in the shared campaign.

**Merge rules:** at most one pilot survives (the player chooses), the other pilot's garage is archived rather than merged, history keeps the reporting identity, no linking in the final 24 h of a turn, and unlinking is admin-only.

## Consequences

- **+** Ownership of both accounts is proven, no passwords are shared, and providers keep their own authentication.
- **+** Works for the original game even though it has no text input.
- **−** Needs a small UI on providers that have one (launcher, port, web portal).
- **−** The message-of-the-day approach still has to be verified on the real client (visible length, fetched every session).
- **−** On the Insignia side the proof is only as strong as the XUID the game reports. Unless Insignia can confirm the connected user to the gateway, a modified console could claim another XUID. This is the same risk the existing campaign already has, and links can be reverted by an admin.

## Alternatives considered

- **Honor system** (the player states which XUID is theirs): easy, but allows taking over other people's progress.
- **Provider OAuth** (for example signing in with Insignia): the best experience, if a provider offers it. It can be added later as a fourth way.
