"""Generates overview.svg for steelcore. Usage: python overview.py overview.svg"""
import sys
from xml.sax.saxutils import escape as e

OUT = sys.argv[1]
W, H = 1200, 890
o = []
add = o.append

def pill(x, y, kind, text):
    w = round(7.0 * len(text) + 18)
    add(f'<rect class="p-{kind}" x="{x}" y="{y}" width="{w}" height="18" rx="9"/>')
    add(f'<text class="pt-{kind}" x="{x + w / 2}" y="{y + 12.5}" text-anchor="middle">{e(text)}</text>')
    return w

def card(x, y, w, h, accent, title, subs, status, cls="card"):
    add(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
    if accent:
        add(f'<rect class="{accent}" x="{x}" y="{y}" width="6" height="{h}" rx="3"/>')
    tx = x + 20
    add(f'<text class="t" x="{tx}" y="{y + 30}">{e(title)}</text>')
    for i, s in enumerate(subs):
        add(f'<text class="s" x="{tx}" y="{y + 52 + i * 18}">{e(s)}</text>')
    kind, label = status
    pill(tx, y + h - 28, kind, label)

def arrow(x, y1, y2):
    add(f'<path class="arrow" d="M{x} {y1} V{y2}" marker-end="url(#a)"/>')

style = """
.bg{fill:#f6f7f9}.card{fill:#fff;stroke:#d3d8e0;stroke-width:1.2}.band{fill:#eceff3}
.core{fill:#e9f4f2;stroke:#0f766e;stroke-width:2}.api{fill:#0f766e}
.mod{fill:#fff;stroke:#9cc9c2;stroke-width:1.2}.db{fill:#dcefeb;stroke:#0f766e;stroke-width:1.5}
.h{font:700 26px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#1b2230}
.sub{font:400 15px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#5a6474}
.lbl{font:700 12px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#5a6474;letter-spacing:.08em}
.t{font:600 17px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#1b2230}
.s{font:400 13px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#5a6474}
.apit{font:700 17px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#fff}
.apis{font:400 13px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#d5efeb}
.coret{font:700 18px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#0f766e}
.arrow{stroke:#7b8494;stroke-width:1.8;fill:none}.ev{stroke:#0f766e;stroke-width:1.6;fill:none;stroke-dasharray:6 5}
.ah{fill:#7b8494}.aht{fill:#0f766e}
.ins{fill:#2f8f5b}.stb{fill:#d9822b}.brx{fill:#3b6fd8}.svc{fill:#7a5fc0}
.p-ok{fill:#dcf3e6;stroke:#2f8f5b}.pt-ok{font:700 10px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#1f6b43;letter-spacing:.06em}
.p-dev{fill:#fdf0dc;stroke:#d9822b}.pt-dev{font:700 10px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#9a5410;letter-spacing:.06em}
.p-new{fill:#eef0f4;stroke:#9aa3b2}.pt-new{font:700 10px system-ui,-apple-system,"Segoe UI",sans-serif;fill:#4f5867;letter-spacing:.06em}
@media (prefers-color-scheme: dark){
.bg{fill:#0f1218}.card{fill:#171b23;stroke:#2d3442}.band{fill:#141820}
.core{fill:#0f2420;stroke:#2bb3a3}.api{fill:#167d72}.mod{fill:#152a26;stroke:#2b5e57}.db{fill:#12302b;stroke:#2bb3a3}
.h,.t{fill:#e7eaf0}.sub,.s,.lbl{fill:#9aa3b2}.coret{fill:#4fd1c0}
.arrow{stroke:#7d8798}.ah{fill:#7d8798}.ev{stroke:#4fd1c0}.aht{fill:#4fd1c0}
.p-ok{fill:#12301f;stroke:#2f8f5b}.pt-ok{fill:#7ad9a3}
.p-dev{fill:#33240f;stroke:#d9822b}.pt-dev{fill:#f0b067}
.p-new{fill:#1d222c;stroke:#4a5263}.pt-new{fill:#aab3c2}
}"""

add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">')
add('<title id="t">steelcore architecture overview</title>')
add('<desc id="d">Games and services connect through provider gateways to the steelcore Core API. '
    'Green marks what already runs today: the original Xbox campaign on Insignia, Steelbound with steelnet, the Insignia gateway (today sbcampaign) '
    'and, inside the core, the campaign domain, garage, shop and trades, pilots, the campaign clock and the database schema, all implemented in sbcampaign. '
    'Project Brainbox is in development. New for steelcore: identity and accounts, the Core API, trust and audit, the Steelbound and Brainbox gateways and the read API.</desc>')
add(f'<style>{style}</style>')
add('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
    '<marker id="e" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="aht"/></marker></defs>')
add(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="16"/>')
add('<text class="h" x="40" y="48">steelcore: one campaign, many clients</text>')
add('<text class="sub" x="40" y="72">Most of the campaign already runs today. steelcore puts it behind one API and adds shared identities.</text>')

cols = [40, 326, 612, 898]
cw = [260, 260, 260, 262]

# band 1
add('<rect class="band" x="24" y="92" width="1152" height="142" rx="12"/>')
add('<text class="lbl" x="40" y="114">GAMES &amp; SERVICES</text>')
b1 = [("ins", "Original Xbox", ["live campaign via Insignia"], ("ok", "EXISTS")),
      ("stb", "Steelbound", ["original LoC on PC, steelnet online"], ("ok", "EXISTS")),
      ("brx", "Project Brainbox", ["native PC port + asset tools"], ("dev", "IN DEVELOPMENT")),
      ("svc", "Community services", ["stats website · Discord bot"], ("new", "NEW"))]
for (acc, t, s, st), x, w in zip(b1, cols, cw):
    card(x, 124, w, 96, acc, t, s, st)

# band 2
add('<rect class="band" x="24" y="246" width="1152" height="152" rx="12"/>')
add('<text class="lbl" x="40" y="268">PROVIDER GATEWAYS</text>')
b2 = [("ins", "Insignia gateway", ["today: sbcampaign (live)", "legacy LoC protocol · XUID"], ("ok", "EXISTS")),
      ("stb", "Steelbound gateway", ["new part of steelnet", "legacy LoC protocol · account"], ("new", "NEW")),
      ("brx", "Brainbox gateway", ["protocol of its choice", "identity: Brainbox account"], ("new", "NEW")),
      ("svc", "Read API", ["HTTP/JSON, read-only", "scope: read:public"], ("new", "NEW"))]
for (acc, t, s, st), x, w in zip(b2, cols, cw):
    card(x, 278, w, 106, acc, t, s, st)

# core
add('<rect class="core" x="24" y="412" width="1152" height="410" rx="14"/>')
add('<text class="coret" x="40" y="438">steelcore · Campaign Core</text>')
add('<text class="s" x="1160" y="438" text-anchor="end">green = already implemented in sbcampaign, moved behind the API</text>')
add('<rect class="api" x="40" y="452" width="1120" height="52" rx="10"/>')
add('<text class="apit" x="60" y="484">Core API  steelcore.v1</text>')
pill(262, 469, "new", "NEW")
add('<text class="apis" x="1140" y="484" text-anchor="end">mirrors the decoded campaign commands · gRPC · mTLS · scopes · audited</text>')

mods = [(40, 268, "Identity &amp; accounts", ["players · identities", "link codes · admin merges"], ("new", "NEW")),
        (324, 268, "Campaign domain", ["war tide · influence · points", "leaderboards · award rankings"], ("ok", "IN SBCAMPAIGN")),
        (608, 268, "Garage, shop &amp; trades", ["VT serials · stock &amp; drops", "capture · sortie · trades"], ("ok", "IN SBCAMPAIGN")),
        (892, 268, "Pilots", ["pilot data · factions", "+ unique names (new)"], ("ok", "IN SBCAMPAIGN"))]
for x, w, t, s, st in mods:
    # titles/subs already escaped
    add(f'<rect class="mod" x="{x}" y="520" width="{w}" height="104" rx="10"/>')
    add(f'<text class="t" x="{x + 18}" y="550">{t}</text>')
    for i, line in enumerate(s):
        add(f'<text class="s" x="{x + 18}" y="{572 + i * 18}">{line}</text>')
    pill(x + 18, 596, *st)

row2 = [(40, 552, "Campaign clock (exactly one)", "weekly turns · rounds · shop drops · awards · faction resets", ("ok", "IN SBCAMPAIGN")),
        (608, 552, "Trust &amp; audit", "per-provider trust · plausibility checks · voiding · bans per player", ("new", "NEW"))]
for x, w, t, s, st in row2:
    add(f'<rect class="mod" x="{x}" y="638" width="{w}" height="86" rx="10"/>')
    add(f'<text class="t" x="{x + 18}" y="668">{t}</text>')
    add(f'<text class="s" x="{x + 18}" y="690">{s}</text>')
    pill(x + 18, 698, *st)

# database
add('<path class="db" d="M40 752 a560 14 0 0 0 1120 0 v44 a560 14 0 0 1 -1120 0 z"/>')
add('<ellipse class="db" cx="600" cy="752" rx="560" ry="14"/>')
add('<text class="t" x="430" y="790" text-anchor="middle">PostgreSQL · single source of truth</text>')
pill(620, 777, "ok", "SCHEMA IN SBCAMPAIGN")
pill(806, 777, "new", "+ PLAYERS & IDENTITIES")

# arrows (drawn last so heads stay visible)
for x in [250, 536, 822, 1108]:
    arrow(x, 220, 276)
    arrow(x, 384, 410)
add('<path class="ev" d="M1176 681 H1188 V331 H1172" marker-end="url(#e)"/>')

# legend
add('<path class="arrow" d="M40 846 H84" marker-end="url(#a)"/><text class="s" x="94" y="850">API call</text>')
add('<path class="ev" d="M170 846 H214" marker-end="url(#e)"/><text class="s" x="224" y="850">events (turn started, round ended, awards granted)</text>')
x = 560
w = pill(x, 837, "ok", "EXISTS"); add(f'<text class="s" x="{x + w + 8}" y="850">running today</text>'); x += w + 110
w = pill(x, 837, "dev", "IN DEVELOPMENT"); add(f'<text class="s" x="{x + w + 8}" y="850">being built</text>'); x += w + 92
w = pill(x, 837, "new", "NEW"); add(f'<text class="s" x="{x + w + 8}" y="850">to build for steelcore</text>')
add('<text class="s" x="1160" y="874" text-anchor="end">Draft · for discussion</text>')
add('</svg>')

open(OUT, "w", encoding="utf-8").write("\n".join(o) + "\n")
print("written", OUT)
