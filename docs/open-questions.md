# Open questions

Things to settle between the maintainers before building. Each answer will become an ADR.

## Operations and governance

1. **Who runs the core?** An existing campaign database becomes the core, or shared neutral infrastructure, or another option. Who holds backups and production access?
2. **Campaign admins:** who moderates (merges, voiding, bans), and how are decisions logged and reviewed?
3. **Release process:** how are API changes and rule changes agreed and rolled out?

## Existing campaign

4. **Continuity:** does the shared campaign continue the current round and turn count and the existing standings, or start a new season?
5. **Phase 1 timing:** when can the `players`/`identities` tables be added to the existing database?
6. **Protocol library:** can the legacy LoC campaign protocol (codec and command types) be shared between the Insignia and Steelbound gateways, for example as a separately licensed crate? Today it lives in an unlicensed repository, so this needs the author's decision.

## Identity and linking

7. **Message-of-the-day link codes:** is the free message fetched every session, and how many characters fit?
8. **Insignia:** does Insignia offer any account verification or OAuth that a gateway could use?
9. **Pseudo-XUIDs:** which 64-bit range is safe for non-Xbox clients so it can never collide with real XUIDs?
10. **Pilot names:** how are existing duplicate pilot names (if any) resolved when names become unique campaign-wide?

## Game data

11. **Pilot blob:** is the format identical across US, EU and JP versions? Which fields would a native port need to produce?
12. **Stats:** what do `stat1`–`stat10` mean exactly? Plausibility checks need real limits per mission.
13. **Trust:** which reported values can a malicious client inflate, and which can be cross-checked (for example both teams reporting the same match)?

## Technology

14. **API transport:** gRPC (proposed) or HTTP/JSON with OpenAPI for gateways?
15. **Language:** the core in Rust (matches the existing server and makes reuse easy), or another language?
16. **Events:** gRPC streams, webhooks, or PostgreSQL `LISTEN/NOTIFY` behind the API?
