# City Brain Convergence — TSYP14 Technical Challenge
### IEEE ENSI Student Branch — Board Briefing

---

## Title
**City Brain Convergence**
TSYP14 Technical Challenge
Presented to: IEEE ENSI SB Board
Organizers: IEEE Tunisia Section / IEEE Region 8 / ANEEE AI LG / IEEE YP / IEEE CN / IEEE Computer Society Tunisia Chapter

---

## What Is This Challenge?
- Build a **connected three-layer smart city system**, split across three separate teams.
- Each team builds **one layer independently** — no team builds the whole thing.
- The three layers must be **merged and demonstrated live** as a single functioning smart city.
- Core theme: **engineering to an interface you don't control**, and proving your system stays reliable when connected to systems you didn't build — including when the data is being falsified.

---

## The Three Layers (Overview)
| Layer | Role |
|---|---|
| **Twin** | Simulates the city — sensors, actuators, the environment itself |
| **City Brain** | Reads sensor data, decides the right operational response, dispatches actuators |
| **Guardian** | Watches the same data stream, but asks "is this true?" — detects spoofing/attacks and can veto or contain |

Teams are grouped into **triplets** (1 team per layer). Triplets are matched **randomly** — you don't choose your partners.

---

## Layer Detail: Twin
Simulates the smart city environment.

**Sensors simulated:**
- Traffic cameras
- Water-level sensors
- Power-load meters
- Air-quality monitors
- Emergency-call feeds

**Actuators simulated:**
- Police / ambulance dispatch
- Traffic-signal control
- Water-valve control
- Power-grid switching
- Device isolation / quarantine

**Key requirement:** every sensor reading and actuator action must be exposed as a **callable MCP-style tool** so City Brain and Guardian can read and act on them.

---

## Layer Detail: City Brain
Monitors the Twin's live sensor stream for real-world incidents:
- Accidents
- Fires
- Traffic jams
- Flooding

**Must:**
- Decide the correct operational response
- Dispatch the matching actuator through the Twin's tools
- Respect Guardian's trust verdict before acting on a reading

---

## Layer Detail: Guardian
Watches the **same** sensor stream as City Brain, but asks a different question:
**"Is this sensor telling the truth?"**

**Detects:**
- Sensor malfunction
- Actuator failure
- Spoofed data
- Cyber-attacks

**Contains problems by:**
- Isolating a compromised sensor
- Quarantining a device
- Rolling back a falsified reading

**Key requirement:** provides City Brain with a **trust verdict** on a reading before City Brain is allowed to act on it.

---

## Why This Format Matters
- No team controls the full stack — success depends on **interoperability**, not just individual quality.
- Teams are **rematched twice** (Round 1 and Round 2) with different partners — your system must work with partners you've never met, built to a **shared technical contract**, not to each other's code.
- Security & trust are graded as **core requirements**, not an add-on.
- Adversarial testing is explicit: the system must survive **falsified/simulated attack scenarios** provided by organizers in Phase 2.

---

## Timeline
| Phase | Dates | Deliverable |
|---|---|---|
| **Phase 0 — Ideation** | 01 Sep → 17 Sep 2026 | 10-page proposal (all 3 layers, roadmap, tech choices, security) |
| Team–Layer Assignment | 22 Sep 2026 | Each team assigned Twin / City Brain / Guardian |
| **Phase 1 — Development** | 22 Sep → 14 Nov 2026 | Working prototype per team + triplet integration |
| Teams Matching (Round 1) | 31 Oct 2026 | Random triplet formed |
| Triplet Demo (Round 1) | 14 Nov 2026 @ CSTAM | Live demo of merged systems; some triplets advance |
| **Phase 2 — Improvement** | 14 Nov → 14 Dec 2026 | Final prototype + adversarial scenario testing |
| Teams Matching (Round 2) | 01 Dec 2026 | New random triplet |
| Final Submission | 11 Dec 2026 | Final report + GitHub repo |

---

## Key Dates at a Glance
- **09 Sep 2026** — Challenge Infosession
- **17 Sep 2026** — Phase 0 deadline
- **22 Sep 2026** — Layer assignment
- **31 Oct 2026** — Teams Matching Round 1
- **12 Nov 2026** — Phase 1 deadline
- **14 Nov 2026** — Phase 1 Pitching (CSTAM)
- **01 Dec 2026** — Teams Matching Round 2
- **11 Dec 2026** — Final Submission Deadline

---

## Team Requirements
- Max **4 members** per team
- Teams grouped into **triplets**: 1 Twin + 1 City Brain + 1 Guardian team
- Each team **owns and develops one layer only**
- Matching is **random**, twice — plan for a system that works with *any* partner, not a specific one

---

## Deliverables Summary
**Phase 0:** 10-page PDF report (proposal, roadmap, tech choices, security)

**Phase 1:** Working prototype + integrated triplet demo + 20-page report

**Phase 2:** Final prototype + integrated triplet demo + 20-page report + **GitHub repository** (well-documented, with required `.md` files)

---

## Scoring (100 points total)
**Phase 1 — 50 pts**
- Individual Prototype Functionality — 10
- Technical Implementation & Features — 5
- Interoperability & Connectivity Between Teams — **15** (largest single item)
- Security & Trust Mechanisms — 10
- Documentation & Code Quality — 5
- Demonstration & Presence — 5

**Phase 2 — 45 pts**
- Final Prototype Functionality — 10
- 3-Layer System Integration & Reliability — 10
- Response to Adversarial/Simulated Scenarios — **15** (largest single item)
- Final Presentation & Demonstration — 5
- Technical Documentation & Repository — 5

**Takeaway:** interoperability and adversarial robustness are worth more than raw individual features — the contract matters more than the code.

---

## Bonus Points (up to 5 pts)
- ≥1 Computer Society (CS) member — 1 pt
- ≥1 Young Professional (YP) member — 1 pt
- ≥1 Consultants Network (CN) member — 1 pt
- Joint CyberSecurity LG Workspace on Collabrec — 0.25 pt/member (max 1 pt)
- Joint AI LG Workspace on Collabrec — 0.25 pt/member (max 1 pt)

---

## Winners & Submission
- **3 winning teams**; prizes to be determined
- Submissions in **English**
- Contact for questions: **yp@ieee.tn**, **cs@ieee.tn**, **cn@ieee.tn**

---

## Why IEEE ENSI SB Should Engage
- High-visibility technical challenge under IEEE Region 8 / Tunisia Section — good branding and CV value for participants
- Cross-cutting skills: distributed systems, real-time data, simulation, cybersecurity, agentic/MCP-style tool design
- Bonus points reward cross-LG collaboration (AI + CyberSecurity) — a chance to activate multiple SB local groups together
- Early move matters: Phase 0 deadline is **17 Sep 2026** — action needed now to form teams

---

## What You'll Need: Tools, Knowledge & Hardware
No physical hardware is required — the Twin is a **simulated** environment, so a standard laptop per team member is enough. What matters is the software stack and the underlying skills.

**Software & tools:**
- A programming language for backend/API work (Python or Node.js are the most common choices for rapid API + real-time data work)
- Git & GitHub — required deliverable is a documented repo; use it from day one, not just at submission
- An API/interface framework to expose sensor readings and actuator actions (REST or WebSocket server); look into the **Model Context Protocol (MCP)** specifically, since the Twin layer must expose tools in an "MCP-style" — worth prototyping a minimal MCP server early
- A message/event mechanism for real-time streaming (WebSockets, MQTT, or a lightweight pub/sub) so City Brain and Guardian can consume the Twin's live feed
- Docker (or similar) to containerize each layer — useful since the three layers are built independently and must plug into each other cleanly
- A shared schema format (JSON Schema / OpenAPI) to define and freeze the "shared technical contract" between layers before integration
- API testing tools (Postman, curl, or similar) to test your own layer in isolation before a partner team connects

**Basic knowledge to build up:**
- REST/WebSocket API design and how to consume someone else's API from a written spec, not their code
- Core security concepts: authentication/signing of messages, anomaly/outlier detection, replay and spoofing attacks — essential for the Guardian layer, and for Twin/City Brain to defend against being fed bad data
- Basic data modeling for sensor readings and actuator commands (schemas, timestamps, units)
- For City Brain: simple decision logic or rule engines (a full ML model isn't required, but anomaly detection for Guardian may benefit from basic statistics or lightweight ML)
- Version control workflows (branches, PRs) for team collaboration and for the eventual multi-team repo merge

**Recommendation:** since teams are randomly matched twice and must interoperate with code they've never seen, prioritize learning to write and read a clear API contract (schema-first) over any specific framework — that skill transfers no matter which layer you're assigned.

---

## Proposed Next Steps
1. Announce the challenge to SB members (infosession 09 Sep)
2. Recruit and form teams (max 4 members each) — encourage CS/YP/CN cross-membership for bonus points
3. Decide whether to prepare a generic 3-layer proposal now (layer assignment isn't until 22 Sep)
4. Assign a mentor/point of contact for the Phase 0 report (due 17 Sep)
5. Track key dates on SB shared calendar
6. **Critical path: each team must have a working prototype finished by the 12 Nov 2026 Phase 1 deadline — only 2 days before the live pitch/demo at CSTAM on 14 Nov.** Build in buffer time before that deadline for triplet integration testing (connecting to partner teams' systems), not just individual-layer development.
