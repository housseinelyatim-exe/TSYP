# Ground Truth Under Attack — Tracks, Submission Specs & Deadline Timeline

TSYP14 Technical Challenge, hosted by IEEE CIS, GRSS and SPS Tunisia Chapters.
Teams pick **exactly one** of the three tracks below and defend it end-to-end through two submission phases.

---

## 1. The Three Tracks

Each track maps to one segment of the Earth-observation chain: **ground link → in-situ sensing → imagery**. Whichever track a team picks, the same six required deliverables and the same two-phase submission process apply (see sections 2–3).

### Track 1 — Secure Ground-Link Testbed
- **Segment:** the ground-link/communication link between the sensing platform and the receiving station.
- **Focus:** securing the ground-link segment against interference and tampering (the brief cites *documented navigation interference* as the motivating threat class).
- **What "defend it" means here:** demonstrate provenance and integrity of data as it crosses the link — e.g. authenticate the link, detect jamming/spoofing/interference, and show the corrupted or interfered signal is caught rather than silently passed downstream.
- **Relevant expertise:** GRSS (link/RF & remote-sensing context) + CIS (trust anchor, detection logic) + SPS (signal processing on the link).
- **Hardware:** no purchase required — a software/emulated trust anchor and local laptop execution are explicitly valid; a physical radio/ground-link testbed is optional, not required.

### Track 2 — False-Data Injection
- **Segment:** in-situ sensing (sensor-level data feeding the pipeline).
- **Focus:** detecting or preventing false-data injection into sensor readings before they propagate into downstream products.
- **What "defend it" means here:** build a detector that catches injected/falsified sensor data — plausible-looking but corrupted readings — and report how reliably it does so under the standard attack scenario.
- **Relevant expertise:** CIS (anomaly detection, security analytics) + GRSS (sensing domain knowledge) + SPS (statistical/signal-level detection).
- **Hardware:** no purchase required; optional sensor hardware for in-situ data is track-appropriate but not mandatory — solvable with public data and local execution.

### Track 3 — Trust the Pixel
- **Segment:** imagery / the product chain.
- **Focus:** verifying the integrity and provenance of imagery, and detecting synthesized or manipulated images (the brief cites *increasingly capable image synthesis* as the motivating threat class).
- **What "defend it" means here:** show that a manipulated or synthetic image can be flagged — via provenance/watermark verification, image-forensics/anomaly detection, or similar — before it reaches an analyst as trustworthy.
- **Relevant expertise:** SPS (image processing) + CIS (AI/statistical detection) + GRSS (remote-sensing imagery domain knowledge).
- **Hardware:** no purchase required; optional imaging/camera hardware is track-appropriate but not mandatory — solvable with public data and local execution.

> All three tracks share the same challenge goal: use authentic public data, apply the common standard scenario, detect or prevent the attack, and report **detection quality, false alarms, latency, memory and security overhead**.

---

## 2. Required Deliverables (all teams, all tracks)

Regardless of track, every team must complete all six:

| # | Deliverable |
|---|---|
| 1 | Threat model & segment analysis |
| 2 | Platform / architecture / trust anchor |
| 3 | Signal / image processing |
| 4 | AI or statistical detection |
| 5 | Adversarial validation & response |
| 6 | Documentation using the official reference datasets |

---

## 3. Submission Specification by Phase

### Phase 1 — Anonymous Report + Code Submission
**Deadline: 8 November 2026**

| Item | Spec |
|---|---|
| Anonymous Report | No names, unit names, logos, or identifying metadata |
| GitHub Repository | Code submission; must be scrubbed of identifying metadata before/at submission |
| Prototype | Working demonstration of the chosen track's detection/defense |
| Documentation | Must use the **official reference datasets** for the standard scenario |

- The administrative committee assigns each team a **team code** and sanitizes the repository before forwarding it to the jury.
- **Fully anonymous** — this is a hard constraint; a single slip (GitHub username, README credit, file metadata) can compromise a submission.
- Up to **7 finalists** advance to Phase 2.

### Phase 2 — Final Prototype & Pitch
**Deadline: 11 December 2026**

| Item | Spec |
|---|---|
| Working prototype | End-to-end functional system for the chosen track |
| Attack demonstration | Live **or** replayable, showing the attack and the defense/detection response |
| Pitch | English, **7 minutes** presentation + **3 minutes** Q&A |

- Submissions are **non-anonymous** at this stage (live pitch).
- The final session accommodates up to 7 finalist teams within a **1h30** session.

---

## 4. Deadline Timeline

| Milestone | Date |
|---|---|
| Challenge Infosession | **11/09/2026** |
| Phase 1 Deadline — Anonymous Report + Code | **08/11/2026** |
| Preselection Announcement | **10/11/2026** |
| Phase 2 Deadline — Final Prototype & Pitch | **11/12/2026** |

**Critical-path notes:**
- Only **2 days** separate the Phase 1 deadline (08/11) and the Preselection Announcement (10/11) — finalists must be ready to move immediately into Phase 2 build mode.
- That leaves roughly **one month** (10/11 → 11/12) to turn an anonymous prototype into a working, live-demoable, non-anonymous system with a rehearsed pitch.
- Phase 1 is not a formality: it's scored out of 100 and weighted 30% into the final score, so under-investing in it assuming "Phase 2 is what counts" is a mistake.

---

## 5. Scoring Reference (for context on submission weighting)

**Final Score = 30% × Phase 1 Score + 70% × Phase 2 Score** (each phase scored out of 100)

| Phase 1 Criterion | Points |
|---|---|
| Threat model & relevance | 15 |
| Architecture & trust mechanism | 15 |
| Signal / image processing | 15 |
| Detector design & evaluation | 20 |
| Standard scenario & evasion | 20 |
| Feasibility, affordability & local execution | 10 |
| Clarity & reproducibility | 5 |

| Phase 2 Criterion | Points |
|---|---|
| End-to-end functional prototype | 20 |
| Provenance / security control | 15 |
| Processing & local detection | 15 |
| Held-out standard attack & evasion | 20 |
| Metrics, efficiency & accessibility | 10 |
| Documentation & reproducibility | 10 |
| Pitch & technical questions | 10 |

Tie-break order: (1) held-out attack/evasion score → (2) lower false-alarm rate → (3) documented jury decision. No bonus points are awarded.

---

*Source: TSYP14 "Ground Truth Under Attack: Securing the Earth Observation Chain" official challenge brief. Contact for clarifications: ghassen.ltaif@ieee.org*
