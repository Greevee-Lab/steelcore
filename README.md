# steelcore

**One Line of Contact campaign for every client.**

steelcore is a proposed campaign service for *Steel Battalion: Line of Contact*. Its goal is that players on the original Xbox (via Insignia), on Steelbound, on a native PC port and on future clients all fight in **one shared campaign**: the same war, rounds and turns, leaderboards, awards, garage and shop.

It is **not** crossplay. Matches stay on each platform. Only campaign progress is shared.

![steelcore overview](docs/diagrams/overview.svg)

## Built on what already runs

The LoC campaign is already back. `sbcampaign` has decoded the campaign protocol, rebuilt the campaign rules, clock and database, and runs a live campaign on Insignia. steelcore does not replace that work. The proposal is to build on a **fork of `sbcampaign`** (only with its author's agreement), **move that proven campaign logic behind one API** and add what sharing needs: identities, account linking, per-provider trust and a read API.

**Steelbound connects first.** The Insignia campaign keeps running as it is; connecting it later is an option, not a requirement. The overview marks every part as *exists*, *in development*, *new* or *future option*.

## Status

**Concept / draft for discussion.** steelcore itself has no code yet. We want to agree on the architecture with the people who run LoC campaign servers and build LoC clients first.

## Documents

| Document | What's in it |
|---|---|
| [Concept](docs/concept.md) | Goal, architecture, domain model, account linking, Core API, trust, clock, migration path |
| [Decisions (ADRs)](docs/adr/README.md) | Proposed and accepted architecture decisions |
| [FAQ](docs/faq.md) | Short answers to questions that came up, for maintainers and players |
| [Open questions](docs/open-questions.md) | What we still need to decide together |

## The idea in five sentences

1. **steelcore** owns the campaign database and the campaign clock, and is the only component that touches campaign data.
2. Every provider runs a **gateway** that authenticates its own users and talks to steelcore through a versioned **Core API**. Steelbound comes first; Insignia, Brainbox and others can follow.
3. Every provider account is an **identity** that belongs to one campaign **player**. Pilot, garage and stats belong to the player.
4. Players can **link** accounts from different providers with a short-lived code, so the same pilot works on every client.
5. The core keeps the existing data model and keys, so campaigns can be joined later step by step.

## Contributing

Comments and ideas are welcome. Please open an issue or a discussion. For bigger changes, propose an ADR.

Please **never** put real player data (XUIDs, account names, pilot data, IP addresses) into issues, examples or tests. Use made-up or cleaned data only.

## License

[AGPL-3.0](LICENSE). Gateways connect over the network API and can use their own license.

---

*A community project for game preservation. Not affiliated with Microsoft, Capcom or the Insignia project. Line of Contact and Steel Battalion are trademarks of their respective owners.*
