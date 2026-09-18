# Edge AI & IoT for Resilient Smart Infrastructure — TSYP14 Technical Challenge

## Overview

**Edge AI & IoT for Resilient Smart Infrastructure** is a TSYP14 Technical Challenge organised under IEEE Region 8, IEEE Tunisia Section (Student Activities Committee & Technical Activities Committee), IEEE Young Professionals Tunisia Section, INSAT IEEE Student Branch, the **IEEE CAS (Circuits and Systems Society) Tunisia Chapter**, and the **IEEE CRFID Tunisia Chapter**.

**Scope & topic:** Edge AI · IoT · Embedded Systems · Smart Sensing · Wireless Communication · RFID · Intelligent Systems. Teams develop solutions for resilient infrastructure and real-world applications by combining sensing, intelligent processing, connectivity, and real-time action.

**Challenge problem:** Develop an intelligent connected system that addresses a real-world problem by:

> Collecting information → Processing it intelligently at the edge → Producing an appropriate response or action

The solution must demonstrate meaningful intelligence and decision-making **close to the source of the data** — a cloud-only architecture does not satisfy the challenge.

**Challenge goal:** Encourage students to design and demonstrate innovative Edge AI and IoT solutions combining sensing, intelligent processing, connectivity, and real-time action to address practical real-world challenges.

---

## Challenge Instructions (6 steps)

Every team must:

1. **Identify a real-world problem** — select a practical problem and define the proposed solution.
2. **Develop an Edge AI / IoT solution** — the system must integrate: Sensing → Edge Processing → Connectivity → Response/Action.
3. **Implement edge intelligence** — a meaningful processing capability must run at the edge; **cloud-only solutions are not sufficient**.
4. **Choose appropriate technologies** — teams are free to pick hardware, software, communication technologies, AI/ML methods, embedded technologies, or other appropriate technologies.
5. **Build a functional prototype** — the final solution must be demonstrated through a working prototype (hardware, software, or hybrid).
6. **Demonstrate the complete system** — a live demonstration showing: Sensing → Intelligent Processing → Decision-Making → Response/Action.

---

## Required Deliverables

- **Technical Report** — maximum **4 pages**, submitted **anonymously**, briefly covering: Problem · Proposed solution · System architecture · Main technologies · Intelligent processing approach · Innovation · Expected impact.
- **Functional Prototype** — hardware, software, or hybrid.
- **Presentation** — 5 minutes; must **remain anonymous until the evaluation process is completed**.
- **Live Demonstration** — mandatory; must show Sensing → Intelligent Processing → Decision → Resulting Action.

### Anonymity requirement
All submitted materials must remain anonymous during submission and evaluation. Do **not** include: team names, member names, university names, IEEE Student Branch affiliations, logos, email addresses, or other identifying information. **Any violation may result in immediate disqualification.**

---

## Timeline

| Milestone | Date |
|---|---|
| Challenge Infosession | **18/09/2026** |
| Phase 1 Submission Deadline | **20/11/2026** |
| Final Submission Deadline | **09/12/2026** |

> 🚩 **Critical-path flags:**
> - The **Infosession on 18/09/2026** is only days away — use it to clarify prototype-scope expectations and the anonymity rules before committing to a hardware design.
> - Only about **3 weeks** separate the Phase 1 deadline (20/11) from the Final deadline (09/12) — since a functional, live-demoable prototype (not just a report) is required, hardware/firmware integration work should start well before Phase 1 is submitted, not after.
> - Anonymity is enforced through **both** phases, including the Phase 2 presentation ("must remain anonymous until the evaluation process is completed") — unusual among TSYP14 challenges, where most Phase 2 pitches go non-anonymous. Build submission materials (report, slides, prototype labeling, video) with this in mind from day one.

---

## Scoring & Evaluation Criteria

**Total score: 100 points** (per the official poster).

### Phase 1 — Technical Proposal & Video Demonstration

| Category | Sub-criterion | Points |
|---|---|---|
| Non-Technical (6 pts) | Problem Relevance & Impact | 3 |
| | Innovation, Creativity & Originality | 3 |
| Technical (8 pts) | Quality of the Proposed Solution | 2 |
| | Technical Implementation & Edge AI/IoT Integration | 3 |
| | Functional Prototype & Video Demonstration | 2 |
| | CASS/CRFID Integration & Deployment Potential | 1 |
| **Phase 1 total** | | **14** |

### Phase 2 — Final Evaluation

| Category | Sub-criterion | Points |
|---|---|---|
| Non-Technical (2.5 pts) | Quality of Pitching & Presentation | 2 |
| | Final Defense & Compliance with Presentation Requirements | 0.5 |
| Technical (3.5 pts) | Live Prototype Demonstration | 2 |
| | Technical Questions & Answers | 1.5 |
| **Phase 2 total** | | **6** |

> ⚠️ **Discrepancy in the official poster:** the two phase subtotals (14 + 6) sum to **20 points**, not the stated **"TOTAL SCORE: 100 POINTS."** This is likely a scaling/weighting factor (e.g., each phase point ×5) that the poster doesn't spell out — worth a direct question to the organiser (wassim.jmal@ieee.org) before finalizing how much relative effort to put into each scored sub-criterion.

### Pitching
English · **5 min pitching** (Q&A is folded into the 1.5-pt "Technical Questions & Answers" line above, no separate duration given).

---

## Logistics

- **Team size: maximum 3 members** — the smallest team cap of any TSYP14 challenge reviewed so far.
- **Eligibility:** open to IEEE Student Branches.
- **Submission:** "Submit your project and show us what you've built."
- **Contact:** for inquiries or clarifications, email **wassim.jmal@ieee.org**.

### Prizes — 3 winning teams
All winners receive: official IEEE certificates, gifts/prizes (amount unspecified in the poster), and recognition during TSYP14.

---

## Tools, Knowledge & Hardware Needed

**Knowledge / skills**
- Embedded systems and firmware development for the chosen edge platform.
- Edge AI/ML: model selection and optimization for constrained compute (quantization, pruning, or lightweight architectures suited to microcontrollers/SBCs).
- Sensor selection and signal conditioning for the chosen real-world problem.
- Wireless communication protocols (e.g., Wi-Fi, BLE, LoRa, or RFID/NFC where relevant to the CRFID co-sponsorship).
- System architecture documentation and technical writing under a strict 4-page, anonymous format.
- English technical pitching within a short (5-minute) window.

**Tools**
- Embedded/edge ML frameworks (e.g., TensorFlow Lite Micro, Edge Impulse, or equivalent) appropriate to the chosen hardware.
- Firmware/IDE tooling for the target microcontroller or edge board.
- Video recording/editing for the anonymous demonstration material.

**Hardware**
- An edge-capable compute platform (e.g., ESP32, Raspberry Pi, Arduino-class board, or similar) capable of running the intelligent-processing step locally — **required**, since cloud-only solutions are explicitly disqualified.
- Sensors and, optionally, RFID/NFC hardware matching the chosen real-world problem and the CRFID co-sponsorship.
- A response/actuation mechanism to close the Sensing → Processing → Decision → Action loop for the live demo.

---

## Why IEEE ENSI SB Should Engage

- **Hard technical bar with a clear, demoable structure:** the mandatory "cloud-only is not sufficient" rule and the required live Sensing→Processing→Decision→Action demo make this a strong showcase for embedded/IoT skill-building, rather than a slide-deck exercise.
- **Small team size (max 3)** makes this the easiest TSYP14 challenge to field multiple ENSI teams for, spreading risk across several real-world problem choices.
- **Dual-society backing (CAS + CRFID)** rewards teams that lean into RFID/sensing integration specifically — a specific, gradeable criterion ("CASS/CRFID Integration & Deployment Potential") that most teams may overlook.
- **Anonymity enforced through Phase 2 pitching** is a distinctive, meritocratic feature — worth highlighting to members who want a fair, blind evaluation process.
- **Compressed prototype timeline (~3 weeks, Phase 1 → Final)** is a good forcing function for teams that want to practice fast, disciplined embedded-systems delivery.

## Next Steps

1. **Attend the Challenge Infosession on 18/09/2026** — clarify the Phase-1/Phase-2 scoring-scale discrepancy and any hardware-budget or component-sourcing guidance directly with the organisers.
2. **Form teams of up to 3 members** and pick a real-world problem where edge intelligence (not a cloud API call) is genuinely the right architecture.
3. **Select and order edge hardware immediately** — with only ~3 weeks between the Phase 1 and Final deadlines, sensor/board procurement can't wait until after Phase 1 is submitted.
4. **Design the anonymity workflow from day one**: a separate GitHub/submission identity, no branding on the physical prototype, and a presentation script with no institutional references, since anonymity is enforced through Phase 2 as well.
5. **Block the critical dates on the SB calendar:**
   - 18/09/2026 — Infosession
   - 20/11/2026 — Phase 1 Submission (Technical Report + Video Demonstration)
   - 09/12/2026 — Final Submission (Live Prototype Demonstration + Pitch)
6. **Contact wassim.jmal@ieee.org** to resolve the scoring-scale ambiguity and confirm any prize details before committing team resources.
