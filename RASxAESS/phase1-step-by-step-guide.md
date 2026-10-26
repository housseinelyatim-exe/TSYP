# The Living Map: Phase 1 Step-by-Step Guide

**Challenge:** TSYP14 IEEE RAS × IEEE AESS, *"The Living Map: Spatial Memory for Emergency Robots"*
**Phase 1 deadline:** **05/10/2026**
> **Status (02/10/2026):** all tasks below are implemented in [`living-map/`](living-map/README.md). Where the final values differ from this plan (aging constants, drift correction), the code and `living-map/docs/` are the reference.

**Team:** 3 people. Person 1 is the lead and has the heavy task. Persons 2 and 3 have simple tasks of about 2 days each.

---

## 0. What Phase 1 Asks For (and Where the Points Are)

| Deliverable | Points | Owner |
|---|---|---|
| Simulation Demo | **8** | Person 1 |
| GitHub Repository | 4 | Person 1 (Person 3 writes the README) |
| Innovation, Originality & Creativity | 5 | Everyone |
| Implementation Plan | 3 | Person 3 |
| Failure Cases | 3 | Person 3 |
| Short Technical Report (max **6 pages**) | 2 | Person 1 assembles it |
| Writer Robot autonomy | 5 | Person 1 (code) + Person 2 (text) |
| Event detection & beacon deposition | 5 | Person 1 (code) + Person 3 (text) |
| Beacon message & signal design | 5 | Person 3 |
| Frame translation | 5 | Person 2 (math) + Person 1 (code) |
| Outside Network Area | 5 | Person 2 (text) + Person 1 (code) |
| Executor Robot | 5 | Person 1 |
| Technical solution diagrams | 5 | Person 2 |

**Rule to remember:** the simulation must show the **whole chain**. A simulation that only covers exploration loses most of the technical points.

---

## 1. The Architecture We Are Building

This section follows the organizers' diagram.

```
 ┌──────────── THE BUILDING ────────────┐ ┆            ┌──────── OUTSIDE NETWORK AREA (ONA) ────────┐
 │  no GPS · no network                 │ ┆            │                                            │      uplink      ┌──────────────┐
 │                                      │ ┆  Writer    │  ROLE 1 RECEIVE   ROLE 2 TRANSLATE         │ ───────────────► │  COMMAND     │
 │   (B1)        (B2)                   │ ┆  returns   │  Writer's dump  → private frame → GPS      │  (LoRa / Sat)    │  POST        │
 │        beacons on the floor          │ ┆  with data │                                            │                  │  live map    │
 │                                      │ ┆ ─────────► │  ROLE 3 CARRY     ROLE 4 BRIEF             │                  │  commander   │
 │   [WRITER] explores, detects, drops  │ ┆            │  long-range link  mission plan → Executor  │                  │  decides     │
 └──────────────────────────────────────┘ ┆            └───────────────────────────┬────────────────┘                  └──────────────┘
                                 RADIO STOPS HERE                                   │ brief (short range)
                                                                                    ▼
                                                                              [EXECUTOR] enters and
                                                                              navigates using beacons
```

### Key design decisions (agree on these on day 0)

1. **No radio crosses the building wall.** The Writer is a **data mule**: it carries its log out and dumps it to the ONA when it exits.
2. **Beacons only talk to robots inside the building.** They use short-range RF (BLE / ESP32 / nRF24).
3. **The ONA briefs the Executor directly.** The command post gets only an **uplink** for the live map and the commander's decision. **Robots never talk to the command post.** This is a hard rule.
4. **The command post is far away and has no infrastructure.** The "Carry" role therefore uses a long-range link: **LoRa (or LoRaWAN-free point-to-point)**, with a satellite modem (Iridium SBD / Swarm-style) as backup. In the simulation this is a lossy, delayed channel.
5. **Every piece of data carries a timestamp.** Beacons **age**: their confidence drops over time.

### Pick these now (suggested defaults)

| Choice | Suggested default | Why |
|---|---|---|
| Environment | **Fire / Hazardous Building** | Matches the "building" diagram. Events are easy to simulate and to build physically later. |
| Event type 1 | **Fire / heat hotspot** (temperature sensor, threshold) | Cheap sensor (MLX90614 / DHT) for Phase 2 |
| Event type 2 | **Victim detected** (camera + person detection, or PIR) | High "mission" value |
| Event type 3 (bonus) | **Blocked passage / structural** (lidar shows a new obstacle) | Gives the Executor a reason to reroute |
| Robot platform (Phase 2) | 2× differential-drive robots (ESP32 / Raspberry Pi + encoders + IMU + lidar/ToF) | Cheap and realistic |
| Simulator | **Python 2D grid simulator (Pygame)** | Can be built in 3 days. ROS2/Gazebo is too risky for this deadline (mention it as the Phase 2 path). |

---

## 2. Team Split and Timeline

| Day | Person 1 (Lead: simulation + code) | Person 2 (Architecture + ONA write-up) | Person 3 (Beacons + plan + failures) |
|---|---|---|---|
| **Day 0 (02/10, 30 min together)** | Lock decisions from §1, create the GitHub repo | Same meeting | Same meeting, freeze the **beacon message format** (§4) |
| **Day 1 (03/10)** | Map, Writer exploration, beacon drop, data log | Architecture + data-flow diagrams | Beacon spec + implementation plan |
| **Day 2 (04/10)** | ONA (Receive/Translate/Carry/Brief), Executor, live map | ONA write-up + frame-translation math | Failure-case table + README skeleton. **Deliver by evening.** |
| **Day 3 (05/10)** | Record demo video, assemble the 6-page report, push, **submit** | Proofread the report | Proofread, check repo links |

---

## 3. Repository Structure (Person 1 creates it on day 0)

```
living-map/
├── README.md                  # Person 3
├── requirements.txt           # pygame, numpy, folium (or flask)
├── config.yaml                # map, anchor GPS, heading, sensor thresholds, link loss
├── sim/
│   ├── world.py               # grid map, walls, hidden events (fire, victims)
│   ├── beacon.py              # Beacon packet encode/decode + aging   (spec by Person 3)
│   ├── writer.py              # Writer robot: frontier exploration, sensing, beacon drop
│   ├── frame.py               # private frame → GPS                   (math by Person 2)
│   ├── ona.py                 # Outside Network Area: receive/translate/carry/brief
│   ├── link.py                # lossy long-range link (LoRa/sat model)
│   ├── command_post.py        # live map + commander decision
│   ├── executor.py            # Executor: brief → beacon-guided navigation → mission
│   └── main.py                # runs the full scenario, pygame window
├── tests/
│   ├── test_beacon.py
│   └── test_frame.py
├── docs/
│   ├── architecture.png       # Person 2
│   ├── dataflow.png           # Person 2
│   ├── beacon_spec.md         # Person 3
│   ├── implementation_plan.md # Person 3
│   ├── failure_cases.md       # Person 3
│   └── report.pdf             # final 6-page report
└── media/
    └── demo.mp4               # 2–3 min simulation video
```

---

## 4. Step 1: Freeze the Beacon Message (Person 3, day 0–1)

The challenge says a beacon must hold **what was found, where to go, and when it was written**.

### 4.1 Packet format: 16 bytes, binary, fits in one BLE advertisement

| Byte(s) | Field | Type | Meaning |
|---|---|---|---|
| 0 | `beacon_id` | uint8 | Unique ID of this beacon |
| 1 | `event_type` | uint8 | 0 = waypoint, 1 = fire, 2 = victim, 3 = blocked, 4 = exit |
| 2–3 | `x_cm` | int16 | Position in the Writer's **private frame** (cm) |
| 4–5 | `y_cm` | int16 | Position in the private frame (cm) |
| 6–9 | `t_written` | uint32 | Seconds since mission start (**when**) |
| 10 | `severity` | uint8 | 0–255 (temperature level, number of victims, …) (**what**) |
| 11 | `next_id` | uint8 | ID of the next beacon toward the target/exit (**where to go**) |
| 12 | `heading_next` | uint8 | Direction to `next_id`, 0–255 ↦ 0–360° |
| 13 | `ttl_min` | uint8 | Validity time in minutes (depends on event type) |
| 14–15 | `crc16` | uint16 | CRC-16/CCITT over bytes 0–13 |

### 4.2 Signal design
- **Inside the building:** beacons broadcast every **500 ms** (BLE advertising, or ESP-NOW / nRF24 in Phase 2). Robots read **RSSI** to estimate how close they are (proximity, not exact range).
- **Message aging:** confidence drops over time:

  `confidence(t) = severity_weight × exp(−age / τ_type)`

  | Event | τ (half-life feeling) | TTL |
  |---|---|---|
  | Fire | short (fire spreads): τ = 5 min | 15 min |
  | Victim | medium (they may move): τ = 15 min | 45 min |
  | Blocked | long: τ = 60 min | 180 min |
  | Waypoint/exit | almost permanent | 255 |

  When `age > ttl`, the beacon is **stale**. The Executor still uses it for navigation but treats its event as "unverified".
- **Beacon drop rule:** drop a beacon **(a)** at every detected event, **(b)** at every junction/turn, and **(c)** every N metres along a corridor (a "breadcrumb"). Together these form a **graph** that the Executor can follow.

### 4.3 Reference code: `sim/beacon.py`

```python
import struct, math, binascii
from dataclasses import dataclass

FMT = "<BBhhIBBBB"          # 14 bytes payload
EVENT = {0: "waypoint", 1: "fire", 2: "victim", 3: "blocked", 4: "exit"}
TAU_S = {0: 1e9, 1: 300, 2: 900, 3: 3600, 4: 1e9}

@dataclass
class Beacon:
    beacon_id: int
    event_type: int
    x_cm: int
    y_cm: int
    t_written: int
    severity: int = 0
    next_id: int = 255        # 255 = none
    heading_next: int = 0
    ttl_min: int = 255

    def encode(self) -> bytes:
        body = struct.pack(FMT, self.beacon_id, self.event_type, self.x_cm, self.y_cm,
                           self.t_written, self.severity, self.next_id,
                           self.heading_next, self.ttl_min)
        return body + struct.pack("<H", binascii.crc_hqx(body, 0xFFFF))

    @staticmethod
    def decode(pkt: bytes) -> "Beacon":
        if len(pkt) != 16:
            raise ValueError("bad length")
        body, (crc,) = pkt[:14], struct.unpack("<H", pkt[14:])
        if binascii.crc_hqx(body, 0xFFFF) != crc:
            raise ValueError("CRC mismatch")
        return Beacon(*struct.unpack(FMT, body))

    def confidence(self, now_s: int) -> float:
        age = now_s - self.t_written
        if age > self.ttl_min * 60:
            return 0.0
        return (self.severity / 255 if self.event_type else 1.0) * math.exp(-age / TAU_S[self.event_type])
```

---

## 5. Step 2: Frame Translation (Person 2 writes the math, Person 1 codes it)

The Writer only knows its own **private frame**. It starts at (0, 0), facing +x, at the building entrance, and estimates its position by odometry/SLAM. The ONA turns these coordinates into GPS.

### 5.1 Calibration (done once, outside, before entry)
- `lat0, lon0`: GPS of the **entrance point** where the Writer starts. The ONA has GPS because it is outside.
- `ψ`: **bearing of the robot's +x axis**, measured clockwise from true North. Get it from a compass or from 2 GPS points along the building wall.

### 5.2 Formula (flat-earth approximation, error < 1 cm over a building-size area)

Robot frame: **x forward, y to the left**.

```
North = x·cos ψ + y·sin ψ
East  = x·sin ψ − y·cos ψ

lat = lat0 + (North / R) · 180/π
lon = lon0 + (East / (R · cos lat0)) · 180/π          R = 6 378 137 m
```

### 5.3 Worked example (put this in the report)
Entrance at ENSI, Manouba: `lat0 = 36.8130°`, `lon0 = 10.0600°`, `ψ = 90°` (robot faces East). An event at `x = 10 m, y = 5 m`:
- North = 10·0 + 5·1 = **5 m**
- East = 10·1 − 5·0 = **10 m**
- lat = 36.8130 + 5/6378137·57.2958 = **36.813045°**
- lon = 10.0600 + 10/(6378137·cos 36.813°)·57.2958 = **10.060112°**

### 5.4 Error handling (mention it, it scores points)
- Odometry drift grows with distance. Each GPS point therefore carries an **uncertainty radius** `σ = σ0 + k·distance_travelled` (e.g. k = 2 %), drawn as a circle on the live map.
- **Loop closure:** when the Writer comes back to the entrance, it compares its estimated (x, y) with (0, 0). The difference spreads the correction across the path (linear drift correction).

### 5.5 Reference code: `sim/frame.py`

```python
import math
R = 6378137.0

def to_gps(x, y, lat0, lon0, psi_deg):
    psi = math.radians(psi_deg)
    north = x * math.cos(psi) + y * math.sin(psi)
    east = x * math.sin(psi) - y * math.cos(psi)
    lat = lat0 + math.degrees(north / R)
    lon = lon0 + math.degrees(east / (R * math.cos(math.radians(lat0))))
    return lat, lon
```

---

## 6. Step 3: Build the Simulation (Person 1, days 1–2)

**Target:** one command, `python -m sim.main`, plays the whole story in a Pygame window, in 5 scenes.

### Scene A: World (`world.py`), about 1 hour
- A 40×30 grid. Each cell is 0.5 m, so the building is 20 m × 15 m. It has walls, rooms, one entrance and a vertical "RADIO STOPS HERE" line to the right of the entrance.
- Hidden events placed from `config.yaml`: 2 fires, 2 victims and 1 blocked corridor.
- Drawing: unknown cells in dark grey, explored cells in light grey, beacons as blue circles, events as icons.

### Scene B: Writer (`writer.py`), about 4 hours. This is the *autonomy* score.
1. **Sensing:** a simulated lidar (raycast in 16 directions, range 3 m) reveals cells. A simulated temperature sensor detects fire within 1.5 m. A simulated "camera" detects a victim in line of sight within 2 m.
2. **Exploration:** **frontier-based exploration**. Find the closest known-free cell next to an unknown cell, plan a path with A*, go there, and repeat.
3. **Decision-making:**
   - **Battery model.** Each step costs energy. If `battery < cost_to_return × 1.3`, stop exploring and **return to the entrance** so that the data is not lost. This directly answers the challenge's "robot loses power" problem.
   - Avoid fire cells: give them a high A* cost.
4. **Beacon deposition** (rule from §4.2): on an event, at junctions, and every 3 m. It has a limited stock of beacons (e.g. 12), so it prioritises events over breadcrumbs when the stock is low.
5. **Odometry noise:** the Writer's believed position = true position + small accumulated drift. This makes frame translation meaningful.
6. **Log:** a list of all encoded beacon packets, plus the explored occupancy grid and the trajectory, all in the private frame.

### Scene C: ONA (`ona.py` + `link.py`), about 3 hours
When the Writer crosses the radio line:
1. **RECEIVE:** dump the log as a byte stream, decode each packet and **reject bad CRCs**.
2. **TRANSLATE:** call `to_gps()` on every beacon, event and trajectory point, and attach the uncertainty radius.
3. **CARRY:** send compact JSON (or the 16-byte packets + GPS) to the command post over `link.py`. The link model has **packet loss of 10 %, 2 s delay and 51-byte frames (LoRa SF9)**. Lost packets are retransmitted until ACKed (stop-and-wait or a small window). Show a counter: "sent / lost / retried".
4. **BRIEF:** after the commander's decision comes back, build the **mission packet** for the Executor:
   ```json
   { "mission_id": 1, "target": "victim@B7", "target_beacon": 7,
     "route": [0, 2, 3, 5, 7], "avoid": [4], "issued_at": 812,
     "beacon_table": [ ... all decoded beacons ... ] }
   ```

### Scene D: Command post (`command_post.py`), about 2 hours
- **Live map** updated as packets arrive. Use either:
  - **Option 1 (easy, looks great):** generate a `folium` HTML map with OpenStreetMap tiles. It shows a marker per event (red = fire, green = victim, grey = blocked), uncertainty circles and the Writer's path, and auto-refreshes.
  - **Option 2:** a side panel in the Pygame window.
- **Commander decision:** automatic, with a rule: rescue the victim with the highest confidence whose route avoids active fire. Show the choice on screen. Only this decision goes back to the ONA.

### Scene E: Executor (`executor.py`), about 4 hours. This is the *Executor* score.
1. Waits at the ONA, then receives the **brief**. It has **no map of its own**.
2. Enters and navigates **from beacon to beacon**: it moves toward the next beacon in `route`, using the RSSI-like distance to correct its own drift when it reaches each beacon ("beacon snap").
3. Its local lidar avoids obstacles. If a beacon says `blocked`, or it finds a new obstacle, it **re-plans** over the beacon graph without that edge.
4. It reads each beacon's age and shows "fire info is 9 min old → confidence 16 %" to demonstrate **message aging**.
5. Reaches the target, marks "mission complete", returns, and the ONA uplinks the result.

### Must-show moments in the demo (each one maps to a scoring line)
- [ ] The Writer explores autonomously and decides when to turn back (battery).
- [ ] 2+ event types detected, with a beacon dropped at each.
- [ ] A packet decoded on screen: what / where / when.
- [ ] "Radio stops here": nothing is transmitted until the Writer exits.
- [ ] Private → GPS translation shown (table or map).
- [ ] Long-range link with visible packet loss and retries.
- [ ] Live map at the command post.
- [ ] The Executor is briefed by the ONA, never by the command post.
- [ ] The Executor follows beacons, handles a blocked passage, reaches the victim.
- [ ] **Failure injection:** one run with a dead beacon and one with the Writer dying inside. Its last dropped beacons survive, which shows the "memory" idea.

### Tests (cheap points for the repo)
```python
# tests/test_beacon.py
from sim.beacon import Beacon
def test_roundtrip():
    b = Beacon(7, 2, 1000, -250, 812, 200, 9, 64, 45)
    assert Beacon.decode(b.encode()) == b

# tests/test_frame.py
from sim.frame import to_gps
def test_example():
    lat, lon = to_gps(10, 5, 36.8130, 10.0600, 90)
    assert abs(lat - 36.813045) < 1e-6 and abs(lon - 10.060112) < 1e-6
```

---

## 7. Step 4: Diagrams (Person 2, day 1)

Make them in **draw.io** and export PNG to `docs/`. Use the colours from the organizers' diagram: Writer orange, Executor green, ONA blue.

1. **System architecture:** the building (beacons, Writer), the red "radio stops here" line, the ONA box with its 4 roles, the Executor and the command post. Label every arrow with the **medium**: BLE inside, Wi-Fi dump at the exit, LoRa/sat uplink, short-range brief.
2. **Data-flow / sequence diagram** with 5 lanes (Writer · Beacon · ONA · Command Post · Executor):
   `explore → detect → drop beacon → return → dump log → decode+CRC → translate → uplink → live map → decision → brief → enter → read beacons → reach target → report`
3. **(Bonus) Beacon packet layout:** a 16-byte bar diagram.
4. **(Bonus) Writer decision state machine:** `EXPLORE → EVENT_FOUND → DROP → EXPLORE … → LOW_BATTERY → RETURN → DUMP`.

---

## 8. Step 5: ONA Write-Up (Person 2, day 2): about 1.5 pages

One short section per role, each with **what / how / technology / Phase 2 hardware**:

| Role | Sim implementation | Phase 2 hardware |
|---|---|---|
| Receive | Byte-stream dump + CRC check when the Writer crosses the line | Raspberry Pi gateway, Wi-Fi AP / BLE, Writer docks at the entrance |
| Translate | `to_gps()` + drift uncertainty | Pi + GPS module (NEO-6M) + compass for ψ |
| Carry | Lossy LoRa model, ACK + retry | SX1276 LoRa modules (several km line-of-sight); relay node if needed; satellite as option |
| Brief | JSON mission packet over short-range link | ESP-NOW / Wi-Fi from the gateway to the Executor before entry |

---

## 9. Step 6: Implementation Plan (Person 3, day 1): 1 page

**Phase 2 timeline (05/10 → 01/12):**

| Weeks | Milestone |
|---|---|
| W1–W2 (6–19 Oct) | Order hardware; assemble both robots; motor + encoder control |
| W3 (20–26 Oct) | Writer: odometry + lidar/ToF obstacle avoidance; beacons on ESP32 broadcasting the 16-byte packet |
| W4 (27 Oct–2 Nov) | Writer: frontier exploration + 2 sensors + beacon-drop mechanism (servo + magazine) |
| W5 (3–9 Nov) | ONA gateway: receive + translate + LoRa link to command post laptop |
| W6 (10–16 Nov) | Executor: brief reception + beacon-guided navigation |
| W7 (17–23 Nov) | Full integration test in a mock building (classroom + cardboard walls) |
| W8 (24–30 Nov) | Failure tests, user manual, pitch rehearsal, video |
| 01/12 | Final submission |

**Hardware list (rough prices, TND):** 2× robot chassis with encoders, 2× Raspberry Pi / ESP32, 2× ToF/lidar, IMU, MLX90614 temperature sensor, camera or PIR, 10–12× ESP32-C3 beacons + coin batteries, 2× SX1276 LoRa, NEO-6M GPS, servo for the drop mechanism. Fill in real prices from local shops.

**Roles:** who owns the Writer, the Executor and ONA/networking.

---

## 10. Step 7: Failure Cases (Person 3, day 2): 1 page table

| # | Failure | How we detect it | How the system handles it |
|---|---|---|---|
| 1 | Writer loses power inside | No return before timeout | Beacons already dropped keep the memory. The Executor is sent to the last known beacon. |
| 2 | Beacon battery dies | Executor does not hear it at the expected spot | Re-plan using neighbouring beacons + its own odometry |
| 3 | Beacon data is stale | `age > ttl` | Info marked "unverified"; confidence shown on the map |
| 4 | Corrupted packet | CRC mismatch | Packet rejected; the duplicate copy in the Writer log is used |
| 5 | Odometry drift → wrong GPS | Loop-closure error at the entrance | Drift correction + uncertainty circle |
| 6 | Wrong anchor / heading ψ | GPS points fall outside the building footprint | Re-calibrate ψ from 2 GPS points; sanity check |
| 7 | Long-range link drops | No ACK | Store-and-forward queue in the ONA; retry; satellite fallback |
| 8 | Commander decision never arrives | Timeout | The ONA applies a default rule (nearest victim, safe route) and briefs anyway |
| 9 | Passage became blocked after the Writer passed | Executor lidar | Local avoidance + re-plan over the beacon graph |
| 10 | Executor gets lost between beacons | No beacon RSSI for X seconds | Go back to the last beacon heard and retry |
| 11 | Beacon moved/kicked | Its RSSI doesn't match its stored (x, y) | Lower its trust and use the others |
| 12 | ONA power failure | Heartbeat lost | Robots keep their logs on board; resend on reconnect |

---

## 11. Step 8: README (Person 3, day 2)

```markdown
# The Living Map: Spatial Memory for Emergency Robots (TSYP14 RAS×AESS)
One-paragraph description + architecture.png
## Features   (Writer autonomy, beacons, ONA, frame translation, Executor, live map)
## Repo structure
## Install    pip install -r requirements.txt
## Run        python -m sim.main            (full scenario)
              python -m sim.main --fail beacon   (failure demo)
## Tests      pytest
## Demo video link
## Team
```

---

## 12. Step 9: The 6-Page Technical Report (Person 1 assembles it on day 3)

| Page | Content | Source |
|---|---|---|
| 1 | Title, team, abstract, chosen environment + events, **architecture diagram** | Person 2 |
| 2 | Writer robot: exploration, sensing, decision-making (battery return), beacon drop rule | Person 1 |
| 3 | Beacon message & signal design: packet table, RF, message aging | Person 3 |
| 4 | Frame translation (formula + example) + ONA 4 roles | Person 2 |
| 5 | Executor robot + simulation results (screenshots, numbers: coverage %, events found, packets lost/retried, time to victim) | Person 1 |
| 6 | Failure cases (short table), implementation plan summary, innovation points, links to the GitHub repo + video | Person 3 |

**Innovation points to highlight** (these earn the 5 creativity points):
- Battery-aware return, so the **knowledge survives the robot**.
- Beacons form a **navigation graph** (`next_id`), not just isolated markers.
- **Per-event aging** (fire ages fast, walls slowly), with a confidence display.
- An **uncertainty circle** on every GPS point.
- **Store-and-forward** long-range link with the ONA as the only bridge.

---

## 13. Final Submission Checklist (05/10)

- [ ] GitHub repo public, clean README, `python -m sim.main` works on a fresh clone
- [ ] `pytest` passes
- [ ] Demo video (2–3 min, with narration or captions) linked in the README
- [ ] `docs/architecture.png`, `docs/dataflow.png`
- [ ] Report PDF ≤ **6 pages**, in English
- [ ] Implementation plan + failure cases (in the report and in `docs/`)
- [ ] Every scoring line in §0 is visibly covered somewhere
- [ ] Rule check: **no direct robot ↔ command post link** anywhere in code or diagrams
- [ ] Submitted before the deadline. Questions go to aess@ieee.tn / ras@ieee.tn.
