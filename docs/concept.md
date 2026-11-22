# steelcore: one campaign, many clients

**Status:** Draft concept for discussion · **Scope:** Line of Contact (LoC) online campaign
**Audience:** maintainers of LoC campaign servers, game clients and community services

> This is a proposal, not a finished design. Every decision below is open for discussion. Decisions that are already proposed are recorded as [ADRs](adr/). Short answers to common questions are in the [FAQ](faq.md).

---

## 1. Goal

There will soon be several ways to play Line of Contact online:

| Client | How it runs | Online today |
|---|---|---|
| Original Xbox (hardware or emulator) | Original game, online via **Insignia** | **Live campaign**, run by `sbcampaign` |
| **Steelbound** | Original game in a compatibility layer on PC | Free play via steelnet (lobbies, relays, accounts); no campaign yet |
| **Project Brainbox** | Native PC port: new engine plus tools that convert the game's assets | In development |
| Future clients and services | Web stats, Discord bot, tools | — |

**steelcore makes all of them take part in one shared campaign.** A player on Steelbound and a player on Insignia fight for their factions in the same war, on the same leaderboards, in the same rounds and turns.

**Step by step:** the core is built on a fork of the existing campaign server, and **Steelbound connects first**. The Insignia campaign keeps running as it is. Connecting it, and a native port like Brainbox, are **possible future options**, only if the people behind them want that.

**Not a goal:** crossplay. Matches still happen inside each platform's own networking. Only **campaign state** is shared: points, war tide, awards, garage, shop and pilots.

### Why one campaign

- LoC's campaign needs a lot of players to feel alive. Splitting the community into one campaign per client starves all of them.
- Players move between clients (Xbox today, PC tomorrow). Their pilot and garage should move with them.
- One set of campaign rules, one clock and one moderation team instead of several drifting copies.

### What already exists

steelcore does not start from zero. The hardest parts of an LoC campaign revival have already been built, and the campaign is running:

| Piece | Status | Where | Role in steelcore |
|---|---|---|---|
| **LoC campaign protocol**, decoded: 36 commands across war status, missions, pilots, garage, shop, leaderboards, awards, trading and messages | ✅ running | `sbcampaign` | Taken over via the fork; spoken by the Steelbound gateway, and by an Insignia gateway if one is added later |
| **Campaign rules:** points per turn and round, award VTs per faction, award rankings in four categories, shop stock with random drops, faction resets | ✅ running | `sbcampaign` | Taken over via the fork as the core's domain logic |
| **Campaign clock:** weekly turns, rounds, restocking, awards | ✅ running | `sbcampaign` | Taken over as the core's single clock |
| **Data model** in PostgreSQL: accounts, pilots, garage, awards, leaderboards, shop, campaign periods | ✅ running | `sbcampaign` | Taken over, extended by players and identities |
| **Import of earlier campaign data** | ✅ exists | `sbcampaign` | Makes it possible to bring campaign data over if campaigns are joined later |
| **Live campaign on Insignia**, with English and Japanese players | ✅ running | Insignia + `sbcampaign` | Keeps running separately; a possible future provider |
| **Native PC port and asset tools** | 🚧 in development | Project Brainbox | A future provider |
| **PC client with online play, accounts and relays** | ✅ running | Steelbound + steelnet | A future provider |

**New in steelcore** are only the parts that sharing requires: the identity and linking layer, the Core API in front of the existing logic, per-provider trust and auditing, and a read API with events. In other words, steelcore mostly **moves proven campaign logic behind an API** and adds shared identities. The plan is to do that on a **fork of `sbcampaign`**, with its author's agreement (see [migration path](#11-migration-path) and [ADR-0006](adr/0006-fork-sbcampaign.md)). The overview below marks every part accordingly.

---

## 2. Architecture at a glance

![steelcore overview](diagrams/overview.svg)

Green borders and labels mark what exists today, amber what is being built, grey what steelcore adds, and dashed boxes possible future options.

Four layers, from the bottom up:

1. **steelcore (Campaign Core):** the only component that holds campaign state and enforces rules. It owns the database and the campaign clock and offers a versioned **Core API**. Its campaign logic, clock and schema are the ones `sbcampaign` already runs.
2. **Identity & accounts (part of the core):** maps every provider account to one **campaign player**.
3. **Provider gateways:** one per provider. Steelbound comes first; Insignia and Brainbox are possible later. A gateway authenticates its own users, speaks whatever protocol its client needs and calls the Core API. The provider runs it.
4. **Games and services:** the clients players actually use, plus read-only consumers such as a stats website.

**The core rule:** gateways never touch the database. Everything goes through the Core API. That is what keeps rules, anti-cheat, auditing and the campaign clock in one place, and lets the schema evolve without breaking every provider at once ([ADR-0001](adr/0001-core-api-only.md)).

---

## 3. Domain model

The core keeps the data model that `sbcampaign` already runs in production: pilots, garage, awards, leaderboards, shop and campaign periods. The one new idea is that the **player**, not the provider account, becomes the owner of everything.

**New in this diagram:** `PROVIDER`, `PLAYER`, `IDENTITY` and the `identity_id` column on leaderboard entries. Everything else exists in `sbcampaign` today, with the XUID as its key.

```mermaid
erDiagram
    PROVIDER ||--o{ IDENTITY : issues
    PLAYER ||--|{ IDENTITY : "is known as"
    PLAYER ||--o| PILOT : has
    PLAYER ||--o{ GARAGE_VT : owns
    PLAYER ||--o{ LEADERBOARD_ENTRY : earns
    PLAYER ||--o{ AWARD : receives
    IDENTITY ||--o{ LEADERBOARD_ENTRY : "reported via"
    CAMPAIGN ||--|{ TURN : "runs in"
    TURN ||--o{ LEADERBOARD_ENTRY : "scored in"
    CAMPAIGN ||--o{ SHOP_ITEM : stocks

    PROVIDER {
        text id PK "insignia | steelbound | brainbox"
        text display_name
        int trust_level
        text scopes "list of API scopes"
    }
    PLAYER {
        uuid player_id PK
        faction current_faction
        lang language
        bool banned
        timestamptz created_at
    }
    IDENTITY {
        uuid identity_id PK
        text provider_id FK
        text external_id "XUID, account id, ..."
        uuid player_id FK
        text display_name
        text verified_by "first_login | link_code | admin"
        timestamptz linked_at
    }
    PILOT {
        uuid player_id PK
        text pilot_name "unique campaign-wide"
        bytea pilot_data "opaque game blob"
        int format_version
    }
    GARAGE_VT {
        smallint vt_type PK
        bigint serial PK
        uuid player_id FK
        faction faction
        bool sortied
    }
    LEADERBOARD_ENTRY {
        uuid player_id FK
        uuid identity_id FK "audit: which client reported"
        smallint round
        smallint turn
        smallint map
        jsonb stats "stat1..stat10"
    }
```

### Players and identities

- A **player** (`player_id`) is the campaign's own idea of a person. Pilot, garage, stats and awards belong to the player.
- An **identity** is one account at one provider: `(insignia, <XUID>)`, `(steelbound, <account id>)`, `(brainbox, <account id>)`. The pair `(provider, external_id)` is unique.
- A player has one or more identities. On first contact a gateway calls `ResolveIdentity`. An unknown identity automatically gets a new player.
- **Existing data keeps its keys.** `sbcampaign` already stores the XUID as a UUID. That exact UUID becomes the `player_id`, and each existing account gets one `insignia` identity. No campaign row has to move ([ADR-0002](adr/0002-player-id-from-existing-uuid.md)).

### Things that must be unique campaign-wide

Several LoC features were designed for one network and become cross-client the moment they share a campaign:

| Feature | Why it matters | Rule |
|---|---|---|
| **Pilot names** | Trading and VT capture look players up by pilot name | The core enforces uniqueness when a pilot is created |
| **VT serials** | Garage entries are `(type, serial)` | Serials come only from the core |
| **Trades** | Two players may be on different clients | Trade tokens are issued and redeemed by the core |
| **Faction resets** | Happen on turn 3, turn 5 and round end | Only the core's clock does this |

### Pilot data

The pilot record is an opaque binary blob produced by the game. Steelbound runs the original game, so it produces the original format automatically. A native port has to read and write **the exact same format**. The core stores the blob as-is with a `format_version` and can validate it with a shared library later. It never needs to understand it in order to run the campaign.

---

## 4. Account linking

Linking matters as soon as more than one provider is connected. The examples use Insignia, because that is the most likely second provider if it joins later. A player who already has an Insignia pilot and now starts Steelbound should be able to keep playing as the same pilot. Three ways, in order of preference ([ADR-0003](adr/0003-account-linking.md)):

### 4.1 Link code (default)

The player proves they control **both** accounts. A short-lived code is shown on one side and entered on the other.

```mermaid
sequenceDiagram
    autonumber
    actor P as Player
    participant X as Original Xbox (LoC)
    participant IG as Insignia gateway (today sbcampaign)
    participant C as steelcore
    participant SG as Steelbound gateway
    participant L as Steelbound launcher

    P->>X: Open campaign menu
    X->>IG: FreeMessage (per session, XUID known)
    IG->>C: CreateLinkCode(identity = insignia:XUID)
    C-->>IG: code "K7Q-3XF", valid 15 min
    IG-->>X: Message of the day incl. "Link code: K7Q-3XF"
    P->>L: Enter K7Q-3XF ("Link existing pilot")
    L->>SG: RedeemLinkCode(code), signed in as Steelbound account
    SG->>C: RedeemLinkCode(code, identity = steelbound:ACCOUNT)
    C->>C: attach identity to the code owner's player
    C-->>SG: linked to player, pilot "EXAMPLE-PILOT"
    SG-->>L: Done, same pilot on both clients
```

**Why the message of the day:** the original game has no field for typing a code, but it asks the server for a free-form message (`FreeMessage`) on the same connection, after the XUID handshake. So the gateway already knows which XUID is asking and can return a personal code instead of the shared text. The message is UTF-16 with a 16-bit length field, and multi-line text already works. *(To verify on real hardware: how much text is visible, and whether it is fetched every time the campaign menu opens.)*

**How strong is this proof?** Exactly as strong as the XUID itself. In the current campaign protocol, **the game reports its own XUID** and the server accepts it. Insignia authenticates the console's connection, but it is not yet clear whether the campaign server can confirm *which* user is connected. If it cannot, a modified console could claim another player's XUID and see their link code. That is not a new risk: the same spoof would already let someone play another player's pilot today. Linking is therefore as safe as the existing campaign, and every link can be reverted by an admin. If Insignia can pass the authenticated identity to the gateway, both problems go away ([open questions](open-questions.md#identity-and-linking)).

The reverse direction works too. Any client with its own UI (Steelbound launcher, Brainbox, a web portal) can **show** a code that is then redeemed from another client that has a text field.

### 4.2 Admin merge (fallback)

For accounts that cannot prove ownership the normal way, for example a forgotten Insignia login. A campaign admin merges two players after reviewing the evidence. Every merge is written to the audit log and can be reverted.

### 4.3 Unlinked (always allowed)

Linking is optional. An unlinked Steelbound account is simply a new player in the same campaign.

### Merge rules

Linking an identity to a player that already has progress needs clear rules, otherwise two accounts could be used to farm VTs:

1. **At most one pilot survives.** If both sides have a pilot, the player chooses which one is kept. The other pilot and its garage are archived, not merged.
2. **History is kept, not summed twice.** Old leaderboard rows keep their `identity_id`, so audits and voiding by provider stay possible.
3. **No linking in the last 24 h of a turn** (configurable), so awards cannot be gamed right before the turn ends.
4. **Unlinking** is an admin action. It never duplicates a garage.

---

## 5. Core API

A versioned API (`steelcore.v1`) that mirrors the command groups of the original campaign protocol, as `sbcampaign` has already decoded and implemented them. Each call below has a working counterpart there today. Gateways translate one-to-one. Proposed transport: **gRPC** (typed contracts, server-to-server streaming for events), plus an optional read-only HTTP/JSON API for websites and bots.

| Group | Calls (sketch) | Used by |
|---|---|---|
| Identity | `ResolveIdentity`, `CreateLinkCode`, `RedeemLinkCode`, `ListIdentities` | all gateways |
| War | `GetCampaignState`, `GetWarTide`, `GetWarInfluence`, `GetRoundPoints` | all gateways, read API |
| Missions | `ReportUserPoints`, `ReportMissionPoints`, `AnalyzeMatch` | game gateways |
| Pilot | `GetPilot`, `CreatePilot`, `UpdatePilot`, `DeletePilot`, `SetFaction` | game gateways |
| Garage | `ListVTs`, `AddVTs`, `RemoveVTs`, `CaptureVTs`, `SortieVTs`, `ReturnVTs` | game gateways |
| Shop | `ListShop`, `GetPotentialCost`, `BuyVT` | game gateways |
| Leaderboard | `GetRanks`, `CountRanks` | all, read API |
| Awards | `ListAvailableAwards`, `GetAwardRanks`, `ClaimAward` | game gateways |
| Trading | `CreateTradeToken`, `GetTradePartner`, `ExecuteTrade` | game gateways |
| Messages | `GetMessageOfTheDay(language, provider, identity)` | game gateways |
| Events | `Subscribe(turn_started, round_ended, awards_granted, …)` | gateways, bots |

**Every call carries:** the gateway's credentials (mTLS or signed tokens), the `identity_id` it acts for, and an idempotency key for writes. Gateways get **scopes** (`identity:resolve`, `identity:link`, `campaign:report`, `garage:write`, `read:public`, …), so a stats website can never write.

---

## 6. Trust and anti-cheat

In LoC the **client reports its own results** (`AddUserPoint`, `AddMissionPoint`). With several clients, the core has to decide how much to believe each one.

- **Per-provider trust level.** New providers start low (lower rate limits, results held for review), established ones are trusted more.
- **Plausibility checks in the core:** maximum points per mission and per time window, impossible stat combinations, VT counts that don't add up.
- **Audit log for every write:** gateway, provider, identity, request id. Results can be **voided per provider, per identity or per time range** without touching anyone else.
- **Optional later:** match results signed by the session host or relay, if a provider's networking supports it.
- **Bans** apply to the player, so all linked identities are affected.

---

## 7. Campaign clock

There is exactly **one** campaign clock, in the core ([ADR-0004](adr/0004-single-campaign-clock.md)). It is not new: `sbcampaign`'s service task already runs this cycle every week, and steelcore takes it over as it is:

```mermaid
stateDiagram-v2
    direction LR
    [*] --> TurnRunning
    TurnRunning --> TurnRunning: shop drop (n times per turn)
    TurnRunning --> TurnEnd: period expired
    TurnEnd --> TurnRunning: restock shop, turn awards, turn+1<br/>(faction reset on turn 3 and 5)
    TurnEnd --> RoundEnd: after last turn
    RoundEnd --> TurnRunning: round awards, faction reset,<br/>round+1, turn 1
```

New in steelcore is only that every transition is published as an **event**, so gateways can refresh caches and a Discord bot can announce "Round 4, Turn 1 has started". The campaign rules (points per turn and round, award VTs per faction, shop drops) already live in one configuration file in `sbcampaign`. steelcore keeps that file and adds versioning, so rule changes take effect at a turn boundary.

---

## 8. Provider gateways

| Gateway | Status | Client protocol | Authentication | Operated by |
|---|---|---|---|---|
| **Steelbound** | new, the first gateway, part of steelnet | Original LoC campaign protocol, redirected to steelnet (Steelbound's online service) | steelnet account, verified by challenge-response (see [8.1](#81-example-the-steelbound-gateway-inside-steelnet)) | Steelbound |
| **Insignia** | possible future option, if the Insignia side agrees; for example the existing `sbcampaign` server could act as the gateway | Original LoC campaign protocol (TCP) | Insignia authenticates the connection; the game reports its XUID (see [4.1](#41-link-code-default)) | Insignia campaign maintainer |
| **Brainbox** | possible future option, with the port | Its choice: original protocol or a modern API | Brainbox account | Brainbox |
| **Read API** | new | HTTP/JSON, read-only | none or API key | core operator |

Notes:

- The Steelbound gateway and a possible Insignia gateway speak the **same legacy protocol**, which `sbcampaign` has already decoded completely. Through the fork, the Steelbound gateway reuses that protocol code directly. Whether and how that's possible depends on licensing, see [open questions](open-questions.md).
- The original game expects an **XUID** in places, even when it runs outside Xbox Live. Non-Insignia gateways hand the game a **stable, provider-scoped pseudo-XUID** from a reserved range that cannot collide with real XUIDs. The core never relies on it. Its key is always the `identity_id`.

### 8.1 Example: the Steelbound gateway inside steelnet

A gateway is not a separate platform. It is the piece of a provider's existing online service that speaks the campaign. Steelbound shows how that fits together:

| | Original Xbox | Steelbound |
|---|---|---|
| Network, accounts, sign-in | **Insignia** | **steelnet** (exists today) |
| Speaks the campaign protocol with the game | `sbcampaign` (exists, live); could act as the Insignia gateway later | **Steelbound gateway**, a new part of steelnet, built on the forked protocol code |
| Shared campaign state | steelcore | steelcore |

**What steelnet already provides:** lobbies, NAT traversal help and relays for Steelbound's peer-to-peer matches, plus **pilot accounts**. Each account has an id and a unique pilot name and can be secured with Discord or a login. The game itself only receives a short-lived game key, never the account key, and signs in by challenge-response. So steelnet already is Steelbound's **identity provider**. In steelcore a Steelbound player is simply the identity `(steelbound, <steelnet account id>)`.

**What the gateway adds:**

```mermaid
sequenceDiagram
    autonumber
    participant G as LoC in Steelbound
    participant SG as Steelbound gateway (steelnet)
    participant C as steelcore

    G->>SG: campaign connection (redirected by Steelbound, encrypted)
    SG->>G: challenge
    G->>SG: proof with short-lived game key
    SG->>C: ResolveIdentity(steelbound, account id)
    C-->>SG: player, pilot, faction
    SG-->>G: Accept (game gets a pseudo-XUID for this account)
    loop every campaign command
        G->>SG: legacy command, e.g. AddUserPoint
        SG->>C: matching Core API call, e.g. ReportUserPoints
        C-->>SG: result
        SG-->>G: legacy response
    end
```

1. Steelbound redirects the game's campaign connection to the gateway. The connection is encrypted and signed in with the game key the launcher already hands out.
2. The gateway speaks the **original LoC campaign protocol** with the game, the same protocol `sbcampaign` already decoded and speaks on Insignia.
3. For every command it calls the **Core API** with its own gateway credentials, acting for the signed-in account.
4. It **ignores the XUID the game reports.** The game gets a stable pseudo-XUID derived from the account.

**Why this matters for linking:** steelnet checks the sign-in cryptographically, so the gateway knows for certain which account is connected. That makes the Steelbound side the stronger half of a link (compare [4.1](#41-link-code-default)). The Steelbound launcher is also the natural place to redeem a link code shown on the Xbox, and steelnet already uses redeemable codes for account recovery.

**Still to work out:**

- **Pilot names.** steelnet names are unique within steelnet only. Once steelcore requires campaign-wide unique names, a steelnet name can collide with an existing Insignia pilot. steelcore needs one rule for that, for example reserving names in the core and letting the player pick a different campaign name on conflict.
- **Redirect.** How the game finds its campaign server, and the cleanest way for Steelbound to point it at the gateway.
- **Placement.** The gateway is lightweight and runs next to the other steelnet services. The core itself is meant to run separately (see [operations](#10-operations-open)).

Other providers can follow the same pattern: keep your own accounts and sign-in, add a gateway that translates your client's protocol to the Core API.

---

## 9. Data protection

- The core stores **only what the campaign needs:** provider ids, display and pilot names, pilot blobs, stats, garage. **No passwords, no e-mail addresses.** Authentication stays with each provider.
- No logging of player input. Logs contain request metadata only.
- A deletion request removes all of a player's identities and anonymises their history (leaderboard totals stay correct, the name goes away).
- Backups are encrypted, and access to production data is limited to named admins.

---

## 10. Operations (open)

**Who runs the core is deliberately left open** and will be agreed between the maintainers. The concept only defines the roles:

| Role | Responsibility |
|---|---|
| **Core operator** | Runs core and database: backups with point-in-time recovery, monitoring, upgrades |
| **Gateway operator** | Runs one gateway, holds its credentials, handles that provider's users |
| **Campaign admins** | Moderation, merges, voiding results, campaign configuration; drawn from all providers |
| **Maintainers** | Review changes to the core and API in this repository (ADRs for bigger decisions) |

**Proposal:** a small dedicated server that runs only the core and its database, with nothing else on it. The maintainers involved get equal admin access, and new versions are deployed automatically from the repository, so nobody has to work on the server by hand. Other options, such as shared neutral infrastructure, are possible too. Requirements are the same either way: one Postgres primary, encrypted backups, a status page and documented restore drills.

---

## 11. Migration path

```mermaid
flowchart LR
    P0["<b>Phase 0 – done ✅</b><br/>sbcampaign runs the live campaign:<br/>protocol decoded, rules, clock,<br/>database, data import"]
    P1["<b>Phase 1 – fork</b><br/>fork sbcampaign with its<br/>author's OK and a license,<br/>keep in sync with upstream"]
    P2["<b>Phase 2 – core</b><br/>add players + identities,<br/>Core API in front of the<br/>existing rules and clock"]
    P3["<b>Phase 3 – Steelbound</b><br/>Steelbound gateway in steelnet,<br/>campaign live for<br/>Steelbound players"]
    P4["<b>Phase 4 – options</b><br/>Insignia gateway (if agreed),<br/>Brainbox gateway, link codes,<br/>read API + events"]
    P0 --> P1 --> P2 --> P3 --> P4
    classDef done fill:#dcf3e6,stroke:#2f8f5b,color:#1b2230
    classDef option fill:#eef0fb,stroke:#7b83c9,stroke-dasharray:6 4,color:#1b2230
    class P0 done
    class P4 option
```

- **Phase 0 is already done**, and it was the largest step: decoding the campaign protocol, rebuilding the campaign rules and running a live campaign. Everything after it builds on that.
- **Phase 1** forks `sbcampaign` instead of rewriting it. The fork keeps the full history and stays visibly linked to the original. General fixes go back upstream as pull requests ([ADR-0006](adr/0006-fork-sbcampaign.md)).
- **Phase 2** is mostly restructuring, not new logic. The existing domain logic is separated from the protocol server and put behind the Core API, and both are tested against the same campaign replays.
- **Phase 3** brings the campaign to Steelbound. The live Insignia campaign is not touched at any point.
- **Phase 4** contains only options. Each is done only if the people behind it want it.
- Each phase can be released and rolled back on its own.

---

## 12. Multiple games and campaigns

The design starts with **one LoC campaign**, but no table assumes that:

- `campaign_id` on campaign-scoped data allows parallel or seasonal campaigns (for example a test campaign, or a reset season).
- `provider` and `title` are separate concepts. A future title could use the same identity and account layer with its own domain module.
- Game regions (US, EU, JP) already share one campaign today (English and Japanese messages exist). The pilot-blob format must stay compatible across regions and clients.

---

## 13. Next steps

1. Discuss this draft with the author of `sbcampaign`, whose campaign server it builds on: ask for agreement to the fork and a license, and agree on the [open questions](open-questions.md).
2. Set up the fork and a small dedicated server for the core.
3. Agree on the identity schema and the `steelcore.v1` API contract (Phase 2).
4. Build a prototype core against a copy of the campaign data. Only cleaned or synthetic test data, never real player data in the repository.

---

*steelcore is a community project for game preservation. It is not affiliated with Microsoft, Capcom or the Insignia project. Line of Contact and Steel Battalion are trademarks of their respective owners. This concept builds directly on the work behind `sbcampaign`: decoding the LoC campaign protocol, rebuilding the campaign rules and running the revived campaign on Insignia. Without that work there would be nothing to share. This repository contains no code from it yet. Code is only taken over with the author's permission.*
