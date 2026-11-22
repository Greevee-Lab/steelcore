"""Generates overview.svg for steelcore. Usage: python overview.py overview.svg"""
import sys
from xml.sax.saxutils import escape as e

OUT = sys.argv[1]
W, H = 1200, 910
o = []
add = o.append

# status kinds: ok = exists today, dev = in development, new = to build, fut = possible future option
CARD = {"ok": "card card-ok", "dev": "card", "new": "card", "fut": "card card-fut"}
MOD = {"ok": "mod mod-ok", "new": "mod", "fut": "mod card-fut"}


def pill(x, y, kind, text):
    w = round(7.0 * len(text) + 18)
    add(f'<rect class="p-{kind}" x="{x}" y="{y}" width="{w}" height="18" rx="9"/>')
    add(f'<text class="pt-{kind}" x="{x + w / 2}" y="{y + 12.5}" text-anchor="middle">{e(text)}</text>')
    return w


def card(x, y, w, h, accent, title, subs, status):
    kind, label = status
    add(f'<rect class="{CARD[kind]}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
    if accent:
        add(f'<rect class="{accent}{" acc-fut" if kind == "fut" else ""}" x="{x}" y="{y}" width="6" height="{h}" rx="3"/>')
    tx = x + 20
    add(f'<text class="t" x="{tx}" y="{y + 30}">{e(title)}</text>')
    for i, s in enumerate(subs):
        add(f'<text class="s" x="{tx}" y="{y + 52 + i * 18}">{e(s)}</text>')
    pill(tx, y + h - 28, kind, label)


def arrow(x, y1, y2, fut=False):
    cls = "arrow arrow-fut" if fut else "arrow"
    add(f'<path class="{cls}" d="M{x} {y1} V{y2}" marker-end="url(#a)"/>')


FONT = 'system-ui,-apple-system,"Segoe UI",sans-serif'
style = f"""
.bg{{fill:#f6f7f9}}.card{{fill:#fff;stroke:#d3d8e0;stroke-width:1.2}}.band{{fill:#eceff3}}
.core{{fill:#e9f4f2;stroke:#0f766e;stroke-width:2}}.api{{fill:#0f766e}}
.mod{{fill:#fff;stroke:#9cc9c2;stroke-width:1.2}}.db{{fill:#dcefeb;stroke:#0f766e;stroke-width:1.5}}
.card-ok{{stroke:#2f8f5b;stroke-width:2}}.mod-ok{{stroke:#2f8f5b;stroke-width:2}}
.card-fut{{fill:none;stroke:#7b83c9;stroke-width:1.6;stroke-dasharray:7 5}}.acc-fut{{opacity:.35}}
.h{{font:700 26px {FONT};fill:#1b2230}}
.sub{{font:400 15px {FONT};fill:#5a6474}}
.lbl{{font:700 12px {FONT};fill:#5a6474;letter-spacing:.08em}}
.t{{font:600 17px {FONT};fill:#1b2230}}
.s{{font:400 13px {FONT};fill:#5a6474}}
.apit{{font:700 17px {FONT};fill:#fff}}
.apis{{font:400 13px {FONT};fill:#d5efeb}}
.coret{{font:700 18px {FONT};fill:#0f766e}}
.arrow{{stroke:#7b8494;stroke-width:1.8;fill:none}}.arrow-fut{{stroke-dasharray:5 5;opacity:.7}}
.ev{{stroke:#0f766e;stroke-width:1.6;fill:none;stroke-dasharray:6 5}}
.ah{{fill:#7b8494}}.aht{{fill:#0f766e}}
.ins{{fill:#2f8f5b}}.stb{{fill:#d9822b}}.brx{{fill:#3b6fd8}}.svc{{fill:#7a5fc0}}
.p-ok{{fill:#dcf3e6;stroke:#2f8f5b}}.pt-ok{{font:700 10px {FONT};fill:#1f6b43;letter-spacing:.06em}}
.p-dev{{fill:#fdf0dc;stroke:#d9822b}}.pt-dev{{font:700 10px {FONT};fill:#9a5410;letter-spacing:.06em}}
.p-new{{fill:#eef0f4;stroke:#9aa3b2}}.pt-new{{font:700 10px {FONT};fill:#4f5867;letter-spacing:.06em}}
.p-fut{{fill:#eef0fb;stroke:#7b83c9;stroke-dasharray:4 3}}.pt-fut{{font:700 10px {FONT};fill:#3f4796;letter-spacing:.06em}}
@media (prefers-color-scheme: dark){{
.bg{{fill:#0f1218}}.card{{fill:#171b23;stroke:#2d3442}}.band{{fill:#141820}}
.core{{fill:#0f2420;stroke:#2bb3a3}}.api{{fill:#167d72}}.mod{{fill:#152a26;stroke:#2b5e57}}.db{{fill:#12302b;stroke:#2bb3a3}}
.card-ok,.mod-ok{{stroke:#3fae73}}.card-fut{{fill:none;stroke:#8189d6}}
.h,.t{{fill:#e7eaf0}}.sub,.s,.lbl{{fill:#9aa3b2}}.coret{{fill:#4fd1c0}}
.arrow{{stroke:#7d8798}}.ah{{fill:#7d8798}}.ev{{stroke:#4fd1c0}}.aht{{fill:#4fd1c0}}
.p-ok{{fill:#12301f;stroke:#2f8f5b}}.pt-ok{{fill:#7ad9a3}}
.p-dev{{fill:#33240f;stroke:#d9822b}}.pt-dev{{fill:#f0b067}}
.p-new{{fill:#1d222c;stroke:#4a5263}}.pt-new{{fill:#aab3c2}}
.p-fut{{fill:#1c1e36;stroke:#8189d6}}.pt-fut{{fill:#b3b9f2}}
}}"""

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">')
add('<title id="t">steelcore architecture overview</title>')
add('<desc id="d">steelcore is built on a fork of the existing LoC campaign server sbcampaign. '
    'Green marks what exists today: Steelbound with steelnet, the original Xbox campaign on Insignia (running separately), '
    'and inside the core the campaign domain, garage, shop and trades, pilots, the campaign clock and the database schema, taken over from sbcampaign. '
    'Project Brainbox is in development. New for steelcore: identity and accounts, the Core API, trust and audit, the Steelbound gateway and the read API. '
    'Possible future options: an Insignia gateway and a Brainbox gateway.</desc>')
add(f'<style>{style}</style>')
add('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
    '<marker id="e" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="aht"/></marker></defs>')
add(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="16"/>')
add('<text class="h" x="40" y="48">steelcore: one campaign, many clients</text>')
add('<text class="sub" x="40" y="72">Built on a fork of the existing campaign server. A Steelbound connection is being evaluated, other clients can join later.</text>')

cols = [40, 326, 612, 898]
cw = [260, 260, 260, 262]

# band 1: games & services
add('<rect class="band" x="24" y="92" width="1152" height="142" rx="12"/>')
add('<text class="lbl" x="40" y="114">GAMES &amp; SERVICES</text>')
b1 = [("stb", "Steelbound", ["original LoC on PC, steelnet online"], ("ok", "EXISTS")),
      ("brx", "Project Brainbox", ["native PC port + asset tools"], ("dev", "IN DEVELOPMENT")),
      ("ins", "Original Xbox", ["campaign on Insignia, runs separately"], ("ok", "EXISTS")),
      ("svc", "Community services", ["stats website · Discord bot"], ("new", "NEW"))]
for (acc, t, s, st), x, w in zip(b1, cols, cw):
    card(x, 124, w, 96, acc, t, s, st)

# band 2: gateways
add('<rect class="band" x="24" y="246" width="1152" height="152" rx="12"/>')
add('<text class="lbl" x="40" y="268">PROVIDER GATEWAYS</text>')
b2 = [("stb", "Steelbound gateway", ["under evaluation, part of steelnet", "legacy LoC protocol · account"], ("new", "NEW")),
      ("brx", "Brainbox gateway", ["possible later, with the port", "protocol of its choice"], ("fut", "FUTURE OPTION")),
      ("ins", "Insignia gateway", ["possible later, if agreed", "e.g. via the sbcampaign server"], ("fut", "FUTURE OPTION")),
      ("svc", "Read API", ["HTTP/JSON, read-only", "scope: read:public"], ("new", "NEW"))]
for (acc, t, s, st), x, w in zip(b2, cols, cw):
    card(x, 278, w, 106, acc, t, s, st)

# core
add('<rect class="core" x="24" y="412" width="1152" height="410" rx="14"/>')
add('<text class="coret" x="40" y="438">steelcore · Campaign Core</text>')
add('<text class="s" x="1160" y="438" text-anchor="end">green = taken over from sbcampaign (fork), placed behind the API</text>')
add('<rect class="api" x="40" y="452" width="1120" height="52" rx="10"/>')
add('<text class="apit" x="60" y="484">Core API  steelcore.v1</text>')
pill(262, 469, "new", "NEW")
add('<text class="apis" x="1140" y="484" text-anchor="end">mirrors the decoded campaign commands · gRPC · mTLS · scopes · audited</text>')

mods = [(40, 268, "Identity &amp; accounts", ["players · identities", "link codes · admin merges"], ("new", "NEW")),
        (324, 268, "Campaign domain", ["war tide · influence · points", "leaderboards · award rankings"], ("ok", "FROM SBCAMPAIGN")),
        (608, 268, "Garage, shop &amp; trades", ["VT serials · stock &amp; drops", "capture · sortie · trades"], ("ok", "FROM SBCAMPAIGN")),
        (892, 268, "Pilots", ["pilot data · factions", "+ unique names (new)"], ("ok", "FROM SBCAMPAIGN"))]
for x, w, t, s, st in mods:
    add(f'<rect class="{MOD[st[0]]}" x="{x}" y="520" width="{w}" height="104" rx="10"/>')
    add(f'<text class="t" x="{x + 18}" y="550">{t}</text>')
    for i, line in enumerate(s):
        add(f'<text class="s" x="{x + 18}" y="{572 + i * 18}">{line}</text>')
    pill(x + 18, 596, *st)

row2 = [(40, 552, "Campaign clock (exactly one)", "weekly turns · rounds · shop drops · awards · faction resets", ("ok", "FROM SBCAMPAIGN")),
        (608, 552, "Trust &amp; audit", "per-provider trust · plausibility checks · voiding · bans per player", ("new", "NEW"))]
for x, w, t, s, st in row2:
    add(f'<rect class="{MOD[st[0]]}" x="{x}" y="638" width="{w}" height="86" rx="10"/>')
    add(f'<text class="t" x="{x + 18}" y="668">{t}</text>')
    add(f'<text class="s" x="{x + 18}" y="690">{s}</text>')
    pill(x + 18, 698, *st)

# database
add('<path class="db" d="M40 752 a560 14 0 0 0 1120 0 v44 a560 14 0 0 1 -1120 0 z"/>')
add('<ellipse class="db" cx="600" cy="752" rx="560" ry="14"/>')
add('<text class="t" x="430" y="790" text-anchor="middle">PostgreSQL · single source of truth</text>')
pill(620, 777, "ok", "SCHEMA FROM SBCAMPAIGN")
pill(820, 777, "new", "+ PLAYERS & IDENTITIES")

# arrows (drawn last so heads stay visible); dashed into future options
for x, fut in [(250, False), (536, True), (822, True), (1108, False)]:
    arrow(x, 220, 276, fut)
    arrow(x, 384, 410, fut)
add('<path class="ev" d="M1176 681 H1188 V331 H1172" marker-end="url(#e)"/>')

# legend
add('<path class="arrow" d="M40 846 H84" marker-end="url(#a)"/><text class="s" x="94" y="850">API call</text>')
add('<path class="ev" d="M170 846 H214" marker-end="url(#e)"/><text class="s" x="224" y="850">events (turn started, round ended, awards granted)</text>')
x = 40
for kind, label, text, gap in [("ok", "EXISTS", "exists today (green border)", 210),
                               ("dev", "IN DEVELOPMENT", "being built", 110),
                               ("new", "NEW", "to build for steelcore", 160),
                               ("fut", "FUTURE OPTION", "possible later (dashed)", 0)]:
    w = pill(x, 864, kind, label)
    add(f'<text class="s" x="{x + w + 8}" y="877">{text}</text>')
    x += w + gap
add('<text class="s" x="1160" y="877" text-anchor="end">Draft · for discussion</text>')
add('</svg>')

open(OUT, "w", encoding="utf-8").write("\n".join(o) + "\n")
print("written", OUT)
