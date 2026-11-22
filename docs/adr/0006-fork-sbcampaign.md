# ADR-0006: Build the core on a fork of sbcampaign

**Status:** Proposed, waiting for the agreement of the `sbcampaign` author · **Date:** 2026-11-22

## Context

`sbcampaign` already implements the LoC campaign: the decoded protocol, the campaign rules, the clock and the database, and it runs the live campaign on Insignia. Rewriting all of that would waste a lot of proven work and would likely introduce new bugs.

`sbcampaign` currently has no license. Without one, the code may be viewed but not reused, so a fork needs the author's explicit agreement.

## Decision

- Ask the author to add a license to `sbcampaign`. The author chooses which one. AGPL-3.0 or GPL-3.0 would match this project, and a permissive license works as well.
- Create a **real GitHub fork**. It keeps the full commit history and the visible "forked from" link, so the original work stays credited automatically.
- Keep the original code as intact as possible. New parts (identities, Core API, gateways) are added as separate modules next to it, which keeps upstream merges simple.
- Pull upstream changes regularly (`git fetch upstream`, `git merge upstream/main`). General fixes go back upstream as pull requests.
- The live Insignia campaign stays on the original server and is not affected by the fork.

## Consequences

- **+** Proven campaign logic from day one; the work goes into the new parts.
- **+** Credit stays visible in the history and on GitHub.
- **+** Upstream and fork can benefit from each other's fixes.
- **−** Two code bases need syncing. Keeping our changes additive limits the effort.
- **−** Nothing can start before the author agrees and adds a license.

## Alternatives considered

- **Clean rewrite:** independent of the license, but repeats work that already exists and runs.
- **Contribute directly to `sbcampaign`:** the friendliest option if the author prefers it. The new parts would then live in the original repository, and this repository would only keep the concept.
