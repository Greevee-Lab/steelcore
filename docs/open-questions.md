# Open questions

Things to settle between the maintainers before building. Each answer will become an ADR. Questions that already have an answer are in the [FAQ](faq.md).

## Operations and governance

1. **Who runs the core?** An existing campaign database becomes the core, or shared neutral infrastructure, or another option. Who holds backups and production access?
2. **Campaign admins:** who moderates (merges, voiding, bans), and how are decisions logged and reviewed?
3. **Release process:** how are API changes and rule changes agreed and rolled out?

## Existing campaign

4. **Continuity:** does the shared campaign continue the current round and turn count and the existing standings, or start a new season?
5. **Phase 1 timing:** when can the `players`/`identities` tables be added to the existing database?
6. **Protocol library:** can the legacy LoC campaign protocol (codec and command types) be shared between the Insignia and Steelbound gateways, for example as a separately licensed crate? Today it lives in an unlicensed repository, so this needs the author's decision.

## Identity and linking

7. **Message-of-the-day link codes:** how much of the free message is visible on screen, and is it fetched every time the campaign menu opens?
8. **Authenticated XUID:** the game reports its own XUID. Can Insignia confirm to the campaign server which user is actually connected (for example via connection metadata), so a modified console cannot claim someone else's XUID?
9. **Insignia's consent:** is the Insignia project fine with linking Insignia XUIDs to accounts at other services, and with an Insignia campaign that is shared with PC clients? Does Insignia offer account verification or OAuth that a gateway could use?
10. **Pseudo-XUIDs:** which 64-bit range is safe for non-Xbox clients so it can never collide with real XUIDs?
11. **Pilot names:** how are existing duplicate pilot names (if any) resolved when names become unique campaign-wide? And what happens when a provider's own account name (for example a steelnet pilot name) is already taken by a pilot from another provider?
12. **Campaign server redirect:** how does the game find its campaign server address, and how should non-Xbox clients point it at their gateway?

## Game data

13. **Pilot blob:** is the format identical across US, EU and JP versions? Which fields would a native port need to produce?
14. **Stats:** what do `stat1`–`stat10` mean exactly? Plausibility checks need real limits per mission.
15. **Trust:** which reported values can a malicious client inflate, and which can be cross-checked (for example both teams reporting the same match)?

## Technology

16. **API transport:** gRPC (proposed) or HTTP/JSON with OpenAPI for gateways?
17. **Language:** the core in Rust (matches the existing server and makes reuse easy), or another language?
18. **Events:** gRPC streams, webhooks, or PostgreSQL `LISTEN/NOTIFY` behind the API?
