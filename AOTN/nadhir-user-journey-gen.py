import sys

W, H = 1600, 1440
LX = [20, 410, 800, 1190]  # lane left edges, width 390
LW = 390
CX = [x + LW // 2 for x in LX]
INK = "#1F3A4A"
LINE = "#4A5F6D"

STY = {
    "n": ("#F4F7F9", "#5C7180"),
    "watch": ("#FCF0B4", "#C9A227"),
    "now": ("#F6C29A", "#C9783A"),
    "safe": ("#F9DCC0", "#D08A3C"),
    "ok": ("#DCE8D5", "#6E9A57"),
    "grey": ("#ECEFF1", "#8A99A3"),
    "dia": ("#FFF6D9", "#B8962E"),
}

out = []
add = out.append


def text(cx, cy, lines, size=15, lh=19, anchor="middle", color=INK):
    y0 = cy - (len(lines) - 1) * lh / 2 + size * 0.35
    for i, ln in enumerate(lines):
        parts = ln.split("*")
        spans = "".join(
            f'<tspan font-weight="700">{p}</tspan>' if k % 2 else p
            for k, p in enumerate(parts) if p
        )
        add(f'<text x="{cx}" y="{y0 + i*lh:.1f}" font-size="{size}" '
            f'text-anchor="{anchor}" fill="{color}">{spans}</text>')


def box(cx, cy, w, h, lines, s="n", size=15):
    f, st = STY[s]
    add(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="10" '
        f'fill="{f}" stroke="{st}" stroke-width="1.6"/>')
    text(cx, cy, lines, size)
    return dict(cx=cx, cy=cy, w=w, h=h)


def dia(cx, cy, w, h, lines):
    f, st = STY["dia"]
    add(f'<polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" '
        f'fill="{f}" stroke="{st}" stroke-width="1.6"/>')
    text(cx, cy, lines, 14, 17, color="#6B5410")


def arrow(pts, label=None, lpos=None, dashed=False):
    d = " ".join(f"{x},{y}" for x, y in pts)
    dash = ' stroke-dasharray="6 5"' if dashed else ""
    add(f'<polyline points="{d}" fill="none" stroke="{LINE}" stroke-width="1.6"'
        f'{dash} marker-end="url(#ah)"/>')
    if label:
        x, y, anc = lpos
        text(x, y, label if isinstance(label, list) else [label], 13, 16,
             anchor=anc, color="#3E5361")


def dot(cx, cy, end=False):
    if end:
        add(f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{INK}" stroke-width="2"/>')
        add(f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="{INK}"/>')
    else:
        add(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{INK}"/>')


# ---------- lanes ----------
titles = [
    ("Night / weekend guard", "on site, not allowed in the room"),
    ("Nadhir", "automatic, day and night"),
    ("On-call electrician (habilité)", "MAIN USER"),
    ("Maintenance &amp; plant manager", "escalation and review"),
]
for i, x in enumerate(LX):
    add(f'<rect x="{x}" y="20" width="{LW}" height="{H-110}" '
        f'fill="{"#EDF2F4" if i % 2 == 0 else "#E2ECEF"}" stroke="#B7C7CE" stroke-width="1.2"/>')
    add(f'<rect x="{x}" y="20" width="{LW}" height="64" fill="#D3E0E5" stroke="#B7C7CE" stroke-width="1.2"/>')
    t, sub = titles[i]
    text(CX[i], 44, [f"*{t}*"], 17)
    text(CX[i], 67, [sub], 13, color="#2F6B8A" if i == 2 else "#4F6573")

G, R, E, M = CX

# ---------- flow ----------
dot(R, 112)
b1 = box(R, 185, 330, 80, ["*1* Watches the existing dials,", "alarm lamps and siren",
                           "(camera + microphone, nothing wired)"])
arrow([(R, 122), (R, 145)])

dia(R, 300, 220, 76, ["What does", "it see?"])
arrow([(R, 225), (R, 262)])

# WATCH branch
bw = box(E, 300, 340, 96, ["*WATCH* · SMS to the electrician only",
                           "Checks the trend and time to limit,",
                           "plans a daytime visit (logged).",
                           "Nobody is woken up at night."], "watch", 14)
arrow([(R + 110, 300), (E - 170, 300)], ["slow drift,", "limit not reached"], (R + 165, 278, "middle"))

# INTERVENE NOW
bn = box(R, 435, 330, 92, ["*2 INTERVENE NOW*",
                           "limit reached, or 2 signals agree",
                           "(dial + lamp / siren). Alert sent to",
                           "guard and electrician at once"], "now", 14)
arrow([(R, 338), (R, 389)], ["limit or alarm"], (R + 10, 368, "start"))

# fork to guard and electrician
g3 = box(G, 575, 330, 92, ["*3* Gets an SMS:",
                           "“Alarm at the substation.",
                           "Do NOT enter the room.",
                           "Check from the outside.”"])
e3 = box(E, 575, 330, 92, ["*3* Gets SMS + push: the value,",
                           "trend and time to limit.",
                           "Replies “1” to acknowledge"])
arrow([(R - 165, 435), (G, 435), (G, 529)])
arrow([(R + 165, 435), (E, 435), (E, 529)])

# guard check
dia(G, 715, 230, 84, ["Smoke, smell", "or noise?"])
arrow([(G, 621), (G, 673)])
gy = box(G - 112, 855, 156, 104, ["*4* Replies “2”,", "clears the area,", "calls Civil", "Protection (198)"], "safe", 14)
gn = box(G + 112, 855, 156, 104, ["*4* Replies “1”:", "nothing visible", "from outside"], "grey", 14)
arrow([(G - 115, 715), (G - 115, 803)], "yes", (G - 125, 705, "end"))
arrow([(G + 115, 715), (G + 115, 803)], "no", (G + 125, 705, "start"))

# electrician ack
dia(E, 715, 240, 84, ["Acknowledged", "within 5 min?"])
arrow([(E, 621), (E, 673)])
esc = box(M, 715, 330, 112, ["*Safety net*: Nadhir calls the",
                             "electrician (voice call, 2G backup);",
                             "still no reply → calls the maintenance",
                             "manager, then the plant manager"], "safe", 14)
arrow([(E + 120, 715), (M - 165, 715)], "no", (E + 140, 703, "start"))

# guard reply shared via Nadhir
share = box(R, 990, 300, 72, ["Guard's reply is added", "to the alert, visible to all"])
arrow([(G - 112, 907), (G - 112, 990), (R - 150, 990)])
add(f'<polyline points="{G+112},907 {G+112},990" fill="none" stroke="{LINE}" stroke-width="1.6"/>')

# electrician assesses
e4 = box(E, 990, 330, 92, ["*4* Sees live dials, the trend", "and the guard's reply on the",
                           "phone, without entering the room"])
arrow([(E, 757), (E, 944)], "yes", (E + 10, 790, "start"))
arrow([(R + 150, 990), (E - 165, 990)])
arrow([(M, 771), (M, 990), (E + 165, 990)], ["first person", "to answer"], (M + 10, 900, "start"))

e5 = box(E, 1140, 330, 112, ["*5* Decides and replies:",
                             "*COMING*: on site, consignation + PPE",
                             "*WATCH*: keeps watching remotely",
                             "*FALSE ALARM*: helps recalibrate"], "ok")
arrow([(E, 1036), (E, 1083)])

log = box(R, 1140, 300, 92, ["*6* Decision log: who was alerted,",
                             "when they acknowledged,",
                             "the decision and the outcome"])
arrow([(E - 165, 1140), (R + 150, 1140)])

rev = box(M, 1250, 330, 76, ["*7* Next morning: reviews alerts,",
                             "response times and false alarms",
                             "on the dashboard"])
arrow([(R, 1186), (R, 1250), (M - 165, 1250)])
dot(M, 1312, end=True)
arrow([(M, 1288), (M, 1299)])

# ---------- legend ----------
ly = H - 62
items = [("watch", "WATCH: slow drift, no urgency"),
         ("now", "INTERVENE NOW"),
         ("safe", "Safety nets: guard check, voice call, escalation")]
x = 24
for s, t in items:
    f, st = STY[s]
    add(f'<rect x="{x}" y="{ly-9}" width="22" height="16" rx="3" fill="{f}" stroke="{st}"/>')
    text(x + 30, ly, [t], 14, anchor="start", color="#3E5361")
    x += 30 + len(t) * 7.6 + 34
text(24, ly + 30, ["Not shown: an unreadable dial gives a “check needed” message, never a false value. "
                   "If Nadhir itself goes silent, the cloud watchdog sends SYSTEM OFFLINE to the electrician."],
     13, anchor="start", color="#3E5361")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="Noto Sans, DejaVu Sans, Arial, sans-serif">'
       '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
       f'orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" fill="{LINE}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>' + "".join(out) + "</svg>")
open(sys.argv[1], "w").write(svg)
