# Open questions

To settle between the maintainers before building. Each answer becomes an ADR. Answered questions are in the [FAQ](faq.md).

## Fork and operations

1. **Fork and license:** is the `sbcampaign` author fine with a fork? Which license, and which name?
2. **Sync:** how do fork and upstream exchange fixes (pull requests, regular merges, a shared branch)?
3. **Server:** who holds backups and production access on the proposed dedicated server?
4. **Moderation:** who are the campaign admins, and how are merges, voiding and bans logged and reviewed?
5. **Releases:** how are API and rule changes agreed and rolled out?
6. **Continuity:** does the Steelbound campaign start as a new season? If Insignia connects later, are standings merged or does a joint season start?

## Identity and linking

7. **Link code in the message of the day:** how much text is visible, and is it fetched every time the campaign menu opens?
8. **Authenticated XUID:** can Insignia confirm to the campaign server which user is connected, so a modified console cannot claim someone else's XUID?
9. **Insignia's consent:** is the Insignia project fine with linking XUIDs to other services and with a campaign shared with PC clients?
10. **Pseudo-XUIDs:** which 64-bit range is safe for non-Xbox clients?
11. **Pilot names:** how are name clashes resolved, both existing duplicates and a steelnet name that is already taken?
12. **Redirect:** how does the game find its campaign server, and how do non-Xbox clients point it at their gateway?

## Game data

13. **Pilot blob:** is the format the same in US, EU and JP? Which fields must a native port produce?
14. **Stats:** what do `stat1`–`stat10` mean, and what are realistic limits per mission?
15. **Trust:** which reported values can a client inflate, and which can be cross-checked (for example both teams reporting one match)?

## Technology

16. **Transport:** gRPC (proposed) or HTTP/JSON with OpenAPI?
17. **Language:** stay with Rust like `sbcampaign` (easy reuse), or something else?
18. **Events:** gRPC streams, webhooks, or PostgreSQL `LISTEN/NOTIFY` behind the API?
