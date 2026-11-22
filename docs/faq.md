# FAQ

Short answers to questions that came up. Unanswered ones are in [open questions](open-questions.md).

## The project

### Why fork sbcampaign instead of writing a new server?

The hard part already exists and runs: the decoded protocol, the rules, the clock and the database. A fork keeps all of that, keeps the history and the "forked from" link, and lets fixes flow both ways. See [ADR-0006](adr/0006-fork-sbcampaign.md).

### How would the fork work?

1. The `sbcampaign` author agrees and adds a license of their choice. The code has none today, so it cannot be reused without one.
2. A real GitHub fork is made, with full history and the visible link to the original.
3. New parts go into separate modules next to the original code, which stays as intact as possible.
4. Upstream changes are merged regularly, and general fixes go back as pull requests.

If the author prefers, the new parts can go straight into `sbcampaign` instead. Details: [concept 4.1](concept.md#41-how-the-fork-works).

### Where would it run, and who runs it?

The proposal is a small dedicated server just for the core, with equal admin access for the maintainers involved and automatic deployments. Nothing is decided yet. See [concept 4.2](concept.md#42-where-it-runs).

### Is "steelcore" the final name?

No, it is a working title. Name and license are agreed with the `sbcampaign` author.

## Architecture

### Does Insignia have to take part?

No. Steelbound connects first, and the Insignia campaign keeps running as it is. Connecting it later is technically possible: `sbcampaign` could act as the Insignia gateway and call the Core API instead of its own database. Two things are open: whether the server can confirm which user is connected (the game reports its own XUID), and whether the Insignia project agrees. See [concept 6.1](concept.md#61-link-code-default).

### How do the Steelbound gateway and steelnet relate?

steelnet is to Steelbound what Insignia is to the original Xbox: network, accounts and sign-in. The gateway is a new part of steelnet that speaks the campaign protocol with the game and calls the Core API. See [concept 8.1](concept.md#81-the-steelbound-gateway-inside-steelnet).

### Why not just share one database between all servers?

Every server would carry its own copy of the rules, and every schema change would break all of them at once. With one Core API, rules, clock, anti-cheat and audit stay in one place. See [ADR-0001](adr/0001-core-api-only.md).

## For players

### Is this crossplay?

No. Insignia players play with Insignia players, Steelbound players with Steelbound players. Only the campaign is shared.

### What happens to my Insignia progress?

Nothing. The Insignia campaign keeps running. If it is connected later, the existing keys are reused, so no data has to be rewritten ([ADR-0002](adr/0002-player-id-from-existing-uuid.md)).

### Do I have to link my accounts?

No. An unlinked account is simply its own player. Linking only helps if you want the same pilot on several clients.

### What if I lost access to an old account?

An admin can merge accounts after review. Every merge is logged and can be reverted. See [concept 6.2](concept.md#62-admin-merge-and-unlinked-play).

### Can I farm VTs on two accounts and merge them?

No. Only one pilot survives a merge, and the other garage is archived, not added. Linking is also blocked shortly before a turn ends. See [merge rules](concept.md#63-merge-rules).

### What data is stored about me?

Only what the campaign needs: provider ids, pilot name and data, stats and garage. No passwords and no e-mail addresses. See [concept 9](concept.md#9-rules-that-stay-in-the-core).
