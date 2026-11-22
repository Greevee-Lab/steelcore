# FAQ

Questions that came up while discussing the concept, with short answers. Questions that are **not answered yet** are collected in [open questions](open-questions.md).

## Architecture

### Does the Insignia part work at all?

**Technically yes, and most of it already exists.**

- The Insignia gateway is essentially today's `sbcampaign`. Insignia already routes the LoC campaign traffic to it. Becoming a gateway is an internal change: instead of writing to its own database, it calls the Core API. Nothing changes for Insignia.
- A personal link code in the message of the day is a small change. The game requests that message after the XUID handshake on the same connection, so the server already knows who is asking. The message is UTF-16 and multi-line text already works.

Two things are still open:

- **Is the XUID genuine?** The game reports its own XUID, and Insignia authenticates the console's connection. It is not yet clear whether the campaign server can confirm *which* user is connected. If not, a modified console could claim someone else's XUID. That risk already exists in the current campaign, and links can be reverted by an admin. Details are in [concept 4.1](concept.md#41-link-code-default).
- **Does the Insignia project agree?** Linking XUIDs to accounts at other services, and an Insignia campaign shared with PC clients, are decisions for the Insignia project.

### How do the Steelbound gateway and steelnet relate?

**steelnet is the platform, and the gateway is a new part of it.** steelnet plays the role for Steelbound that Insignia plays for the original Xbox:

| | Original Xbox | Steelbound |
|---|---|---|
| Network, accounts, sign-in | Insignia | steelnet |
| Speaks the campaign protocol with the game | `sbcampaign` (Insignia gateway) | Steelbound gateway |
| Shared campaign state | steelcore | steelcore |

steelnet already has lobbies, relays and pilot accounts with a cryptographic sign-in, so it already is Steelbound's identity provider. The gateway adds the campaign protocol and translates it to the Core API. Details are in [concept 8.1](concept.md#81-example-the-steelbound-gateway-inside-steelnet).

### Why not just share one database between all servers?

It would be the fastest start, but every server would then carry its own copy of the campaign rules, schema changes would break everyone at once, and permissions could only be set per table. With one Core API, rules, the campaign clock, anti-cheat checks and auditing stay in one place. See [ADR-0001](adr/0001-core-api-only.md).

### Who runs steelcore?

Not decided yet. The concept defines the roles (core operator, gateway operators, campaign admins, maintainers) and leaves the choice to the people involved. See [concept section 10](concept.md#10-operations-open).

## For players

### Is this crossplay?

No. Matches stay on each platform: Insignia players play with Insignia players, Steelbound players with Steelbound players. What is shared is the **campaign**: the war, rounds and turns, leaderboards, awards, garage and shop.

### What happens to my existing Insignia progress?

It stays where it is. The existing account keys are reused as campaign player ids, so no campaign data has to move ([ADR-0002](adr/0002-player-id-from-existing-uuid.md)). Whether the shared campaign continues the current round or starts a new season is still [open](open-questions.md).

### Do I have to link my accounts?

No. An unlinked account is simply its own player in the shared campaign. Linking is only useful if you want to play the same pilot on more than one client.

### What if I can't sign in to my old Insignia account any more?

A campaign admin can merge accounts after reviewing the case. Every merge is logged and can be reverted. See [concept 4.2](concept.md#42-admin-merge-fallback).

### Can I farm VTs on two accounts and merge them?

No. When two accounts with pilots are linked, only one pilot survives (you choose which). The other pilot's garage is archived, not added. Linking is also blocked shortly before a turn ends. See [concept, merge rules](concept.md#merge-rules).

### What data does steelcore store about me?

Only what the campaign needs: your provider ids, pilot name, pilot data, stats and garage. No passwords and no e-mail addresses, because sign-in stays with each provider. See [concept section 9](concept.md#9-data-protection).
