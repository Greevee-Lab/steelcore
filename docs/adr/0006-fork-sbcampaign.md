# ADR-0006: Build the core on a fork of sbcampaign

**Status:** Proposed, waiting for the agreement of the `sbcampaign` author · **Date:** 2026-11-22

## Context

`sbcampaign` already implements the LoC campaign (protocol, rules, clock, database) and runs it live on Insignia. Rewriting that would waste proven work. It has no license, so its code may be read but not reused without the author's agreement.

## Decision

1. **License first.** The author adds a license of their choice. AGPL-3.0 or GPL-3.0 fit this project, and a permissive one works too.
2. **Real GitHub fork.** It keeps the full history and the "forked from" link, so credit stays visible.
3. **Additive changes.** The original code stays as intact as possible. Identities, Core API and gateway are added as separate modules.
4. **Stay in sync.** `git remote add upstream <sbcampaign>`, then regularly `git fetch upstream` and `git merge upstream/main`. General fixes go back upstream as pull requests.
5. **Insignia untouched.** The live campaign keeps running on the original server.
6. **Name and home** of the fork are agreed with the author.

## Consequences

- **+** Proven campaign logic from day one. The work goes into the new parts.
- **+** Credit stays visible, and fixes flow both ways.
- **−** Two code bases have to stay in sync. Keeping our changes additive limits the effort.
- **−** Nothing starts before the author agrees.

## Alternatives

- **Clean rewrite:** independent of any license, but it repeats work that already exists.
