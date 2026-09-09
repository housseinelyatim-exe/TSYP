# The Living Map: Spatial Memory for Emergency Robots — TSYP14 Technical Challenge
### Presentation for the IEEE ENSI Student Branch Board

---

## Overview

**"The Living Map: Spatial Memory for Emergency Robots"** is a TSYP14 technical challenge organized jointly by **IEEE RAS (Robotics & Automation Society) Tunisia Chapter** and **IEEE AESS (Aerospace and Electronic Systems Society) Tunisia Section Chapter**, under the wider TSYP14 (IEEE Tunisian Student and Young Professional Congress) umbrella (IEEE Region 8, IEEE Tunisia Section, IEEE Young Professionals Tunisia, INSAT IEEE Student Branch).

**Scope & Topic:** In disaster response, underground exploration, and hazardous inspections, autonomous robots often must operate where **GPS and communication networks are unavailable**. The challenge focuses on **resilient communication in disconnected environments** — a first robot leaves critical information behind via small radio beacons, so a second robot can retrieve it and continue the mission without starting from zero.

**What teams must build, concretely:**
- Design beacon messages containing **what was found, where to go, and when it was written**.
- Build an **Outside Network Area** connecting the disconnected zone to the outside world.
- Translate robot-internal coordinates into **real-world GPS coordinates**.
- Transfer information to a **distant command post**.
- Brief the **Executor Robot** before it enters the zone.
- Build an **Executor Robot** that receives a mission and navigates using inherited beacon information.
- Display a **live map** at the command post.

**Challenge problem:** In collapsed buildings, underground mines, fire-damaged structures, or contaminated zones, robots must explore, sense, detect hazards, locate victims, and communicate despite limited connectivity. When a robot fails, leaves, or loses power, the knowledge it collected can disappear with it. The challenge: build a resilient autonomous system that can:

`Sense → Communicate → Preserve Critical Information → Enable Mission Continuity`

---

## Challenge Goal

Design and prototype a **two-robot system that gives an unmapped space its own memory.**

**Choose one environment:**
- Urban Search & Rescue
- Fire / Hazardous Building
- Mines / Tunnels
- Nuclear / Contaminated Zone

**The system must:**
- Build a **Writer Robot** that autonomously explores a GPS-denied space.
- Detect **at least 2 event types**.
- Deploy small radio beacons where relevant.

### System chain
`Writer explores → Events detected & beacons deposited → Outside Network receives & translates data → Wireless / Satellite communication → Command Post → Executor receives mission → Executor enters & navigates using beacons`

---

## Team Requirements & Core Rules (Challenge Instructions)

Each team must:
- Complete registration before the deadline.
- Choose one environment (from the list above).
- Detect **at least 2 event types**.
- Use **at least 2 physical robots**: a **Writer** and an **Executor**.
- Implement a functional **Outside Network Area**.
- Ensure **all** communication between the inside and outside passes through the Outside Network Area.
- **No direct link is allowed between the robots and the command post.**

---

## Technical Focus Areas

| Area | What it involves |
|---|---|
| **Writer Robot** | Autonomous navigation, exploration, decision-making in GPS-denied environments |
| **Event Detection & Beacon Deposition** | Sensing, deciding what information to record, beacon drop mechanism |
| **Beacon Design** | Compact message format, RF broadcast, message aging mechanism |
| **Frame Translation** | Private robot coordinates → real-world GPS coordinates |
| **Outside Network Area** | Command-post connection, satellite/wireless communication, data reception and forwarding |
| **Executor Robot** | Mission briefing, beacon-guided navigation, mission execution |
| **Technical Documentation** | System architecture, data flow, additional technical diagrams |

---

## Phase 1 — Initial Phase

### Required Deliverables
- **GitHub Repository**
- **Simulation Demo**
- **Short Technical Report** — max. **6 pages**
- **Implementation Plan**
- **Failure Cases**
- **Technical Solution & Architecture**

The solution must address: writer robot autonomy, event detection & beacon deposition, beacon message & signal design, frame translation, outside network architecture, executor robot, system architecture & data flow.

**Resource provided by organizers:** a System Architecture Diagram (referenced in the original materials).

---

## Phase 2 — Final Phase

Finalists must provide:
- **Pitching & Q&A**
- **Complete physical prototype**
- **Proposed solution** (write-up)
- **Technologies used**
- **Project architecture**
- **User manual**
- **GitHub Repository**

---

## Pitching Format

- Language: **English**
- **5 minutes** pitching
- **2 minutes** Q&A

---

## Scoring / Evaluation Criteria

**TOTAL SCORE: 100 points + 5 bonus points**

### Initial Phase — 45 points

| Criterion | Points |
|---|---|
| GitHub Repository | 4 |
| Simulation Demo | 8 |
| Short Technical Report | 2 |
| Innovation, Originality & Creativity | 5 |
| Implementation Plan | 3 |
| Failure Cases | 3 |
| **Technical aspects subtotal below** | |
| Writer Robot autonomy | 5 |
| Event detection & beacon deposition | 5 |
| Beacon message & signal design | 5 |
| Frame translation | 5 |
| Outside network area | 5 |
| Executor Robot | 5 |
| Technical solution diagrams | 5 |
| **Subtotal (Initial Phase)** | **45** |

*(Note: the source lists "Technical aspects of the solution" — 7 sub-items × 5 pts = 35 pts — as part of the Initial Phase evaluation alongside the 6 deliverable-quality items totaling 25 pts; the official total for the Initial Phase is stated as 45 pts, so weighting/consolidation details should be confirmed with organizers.)*

### Final Phase — 50 points

| Criterion | Points |
|---|---|
| Pitching and Q&A | 8 |
| Quality of proposed solutions | 8 |
| Technologies used | 5 |
| Physical prototype | 15 |
| Project Architecture | 5 |
| User Manual | 4 |
| GitHub Repository | 5 |
| **Subtotal** | **50** |

### Bonus — up to 5 points

| Bonus condition | Points |
|---|---|
| At least 2 IEEE AESS members in the team | 2 |
| At least 2 IEEE RAS members in the team | 2 |
| At least 1 YP (Young Professional) member with both RAS & AESS memberships | 1 |

---

## Timeline

| Date | Milestone |
|---|---|
| **14/09/2026** | Challenge Infosession |
| **05/10/2026** | ⚠️ **Phase 1 Submission Deadline** (GitHub repo, simulation demo, 6-page report, implementation plan, failure cases, architecture) |
| **01/12/2026** | ⚠️ **Final Submission Deadline** (physical prototype, live pitch + Q&A, full deliverable set) |

### ⚠️ Critical-path deadlines
- **Phase 1 (05/10/2026) requires a working simulation demo, not just a paper report** — simulation build time needs to start well ahead of early October.
- **Final Submission (01/12/2026) requires a complete *physical* prototype with two real robots (Writer + Executor), a working Outside Network Area, and a live pitch.** Physical robot integration, RF beacon hardware, and the "no direct robot-to-command-post link" constraint are the highest-effort, highest-risk parts of this challenge — hardware procurement and integration testing should begin immediately after Phase 1 results, not in the weeks before 01/12/2026.

---

## Prizes

**2 winning teams:**
- **1st Place:** $100 USD + Certificate
- **2nd Place:** $50 USD + Certificate

---

## Logistics

- **Team composition:** at least 2 physical robots required (Writer + Executor); team size not explicitly capped in the source material beyond the general registration requirement — confirm exact member limits with organizers.
- **Registration:** must be completed before the deadline to be eligible.
- **Submission:** "Submit your project and show us what you've built" (platform/channel to be confirmed).
- **Contact:** for inquiries or clarifications, email **aess@ieee.tn** or **ras@ieee.tn**.

---

## Tools, Knowledge & Hardware Needed

**Domain knowledge:**
- Autonomous robot navigation and exploration in GPS-denied environments (SLAM concepts, dead-reckoning, or equivalent localization strategies).
- RF/radio beacon communication design — message framing, broadcast protocols, and "message aging" (staleness handling).
- Coordinate-frame transformation (robot-local frame → real-world GPS frame).
- Disaster-response domain context for the chosen environment (Urban Search & Rescue, Fire/Hazardous Building, Mines/Tunnels, or Nuclear/Contaminated Zone).

**Technical / engineering skills:**
- Robotics middleware and control (e.g., ROS or equivalent) for autonomous exploration and decision-making.
- Event/hazard detection via onboard sensing (vision, gas/hazard sensors, etc.), and logic for deciding what's worth recording.
- Wireless/satellite communication link design between the Outside Network Area and the command post.
- Live-map visualization/dashboard development for the command post.
- System architecture documentation and data-flow diagramming.

**Hardware:**
- **At least 2 physical robots** — one Writer, one Executor.
- Small RF beacon hardware/modules for the Writer robot to deposit.
- Sensors for detecting at least 2 distinct hazard/event types (e.g., fire/heat, gas, structural, victim-detection).
- Communication hardware for the Outside Network Area (wireless/satellite link, gateway hardware).
- A command-post setup capable of receiving translated GPS data and rendering a live map.

---

## Why We Should Engage

- **Cross-society flagship robotics challenge:** backed jointly by IEEE RAS and IEEE AESS, giving ENSI strong visibility across two active technical societies.
- **Genuinely hands-on, hardware-first challenge:** unlike report-only competitions, this demands real autonomous robots and RF hardware — an excellent showcase for ENSI's robotics/embedded/telecom students and a strong CV/portfolio piece.
- **Clear, well-defined system architecture** (Writer → beacons → Outside Network → Command Post → Executor) makes for a strong learning project that touches robotics, RF communications, and safety-critical system design in one challenge.
- **Achievable prize money** ($100 / $50 USD + certificates) plus the broader recognition of placing well in a TSYP14 track.
- **Reasonable timeline for a hardware challenge:** Infosession in mid-September, Phase 1 in early October, and roughly two more months to build the physical prototype for December — enough runway if the team starts hardware work immediately after Phase 1.

## Next Steps

1. **Attend the Challenge Infosession on 14/09/2026** to clarify team-size limits, registration process, and any beacon/RF constraints not fully detailed in the flyer.
2. **Recruit a team with robotics, embedded systems, and RF/communications skills**, and register before the deadline.
3. **Decide on the target environment early** (Urban Search & Rescue, Fire/Hazardous Building, Mines/Tunnels, or Nuclear/Contaminated Zone) — this shapes hazard-detection sensor choices and the physical testing setup.
4. **Start hardware procurement immediately** (robot platforms, RF beacon modules, sensors) given the December physical-prototype deadline is hardware-heavy.
5. **Target an internal draft of the Phase 1 report and simulation demo well before 05/10/2026** to leave buffer for feedback and iteration.
6. **Plan integration/testing time for the "no direct robot-to-command-post link" constraint** — this is an architectural requirement that needs to be designed in from day one, not patched in later.
7. **Contact aess@ieee.tn or ras@ieee.tn** with any open questions before committing team resources.
