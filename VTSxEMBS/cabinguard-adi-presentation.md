# CabinGuard-ADI — TSYP14 Technical Challenge
### Presentation for the IEEE ENSI Student Branch Board

---

## Overview

**CabinGuard-ADI** is a technical challenge under **TSYP14** (IEEE Tunisian Student and Young Professional Congress), jointly organized by:

- IEEE Region 8
- IEEE Tunisia Section (Student Activities Committee & Technical Activities Committee)
- IEEE Young Professionals Tunisia Section
- IEEE VTS (Vehicular Technology Society) — Tunisia Section Chapter
- IEEE EMBS (Engineering in Medicine and Biology Society) — Tunisia
- INSAT IEEE Student Branch

**Scope & Topic:** Modern vehicles are becoming rolling sensor platforms — cameras, steering surfaces, seat sensors, in-cabin motion sensors, and CAN-bus telemetry. CabinGuard-ADI challenges teams to detect **acute driver-incapacitation (ADI) medical events** — epileptic seizure, cardiac syncope/arrhythmia, severe hypoglycemia, or acute stroke — as early and reliably as possible, and to connect that medical decision to a **secure, minimum-risk vehicle response**.

**Problem statement:** Sudden loss of driving capacity can stem from different medical causes with different physiological signatures. The goal is *not* to identify or restrict people with a medical history, but to recognize dangerous deterioration early enough to reduce harm — while avoiding unsafe false alarms.

Key challenges the teams must wrestle with:
- Wearables require user compliance (can't assume the driver is wearing one).
- Existing driver-monitoring systems mainly target fatigue/distraction, not medical events.
- Single-modal sensing causes false positives.
- Biometric data and safety-critical messages require protection.
- Sensor, network, or processing failures must never produce unsafe vehicle actions.

---

## Challenge Goals

1. **Early ADI Detection** — detect physiological and behavioral changes with minimal false alarms.
2. **Multi-Etiology Classification** — distinguish between different medical events and normal driving.
3. **Complete System Architecture** — integrate sensing, processing, detection, control, and communication.
4. **Data Protection & Secure Communication** — protect biometric data and critical messages.
5. **Fail-Safe Vehicle Response** — enable alerts, controlled deceleration, safe stopping.
6. **Privacy-Preserving Emergency Broadcast** — share minimal anonymized data for effective emergency response.
7. **Scientific & Engineering Honesty** — document assumptions, limitations, uncertainties, and performance.

**Required end-to-end pipeline:**
`Sensors → Data Processing → Medical Detection → Cybersecurity → Vehicle Safety`

**Required emergency-response chain (on high-confidence detection):**
`Alert → Verification → Controlled Deceleration → Safe Positioning → Safe Stop`

The system must also demonstrate: sensor/communication failure handling, protection of sensitive biometric data, rejection of tampered or unauthorized messages, scientific justification, privacy preservation, and safe failure behavior.

**Minimum solution requirements:**
- **Medical Event Detection:** at least 2 medical-event classes + 1 normal-driving class.
- **Multimodal Reasoning:** combine relevant in-cabin sensing modalities to reduce false positives.
- **Secure Vehicle Interface:** connect the detection decision to a safe vehicle response.
- **Emergency Communication:** transmit minimum-necessary, anonymized, etiology-aware information.

---

## Phase 1 — Research & Concept Validation

Phase 1 focuses on: Problem Definition • Medical Relevance • AI/Detection Approach • System Architecture • Cybersecurity • Evaluation Design.

Teams **may** use simulated data, synthetic data, public de-identified data, and literature-derived assumptions. **A complete prototype is NOT required at this stage.**

### Required deliverable: IEEE-Style Research Paper (max. 5 pages)

Standard IEEE conference-paper structure, including as applicable:
- Abstract
- Introduction & Motivation
- Related Work / State of the Art
- Problem Definition
- Proposed Methodology
- System Architecture
- Medical Event Detection Approach
- Cybersecurity & Threat Model
- Experimental / Evaluation Methodology
- Expected Results or Preliminary Results
- Conclusion
- References

### Component 2: Proposed System Architecture
Teams must provide a clear end-to-end architecture:
`Sensors → Data Acquisition → Preprocessing → Detection/Fusion → Safety Decision → Vehicle Response → Secure Communication`

Must identify: proposed sensors, data sources, AI/ML or detection method, decision mechanism, communication interfaces, safety mechanisms, cybersecurity controls, privacy considerations.

### Component 3: Detection & AI Methodology
Teams should specify: target medical events, normal-driving class, detection/classification approach, input features/data, proposed model or algorithm, expected detection latency, confidence/uncertainty strategy, false-positive/false-negative considerations.

### Component 4: Security & Threat Model
Teams must identify: protected assets, trust boundaries, communication vulnerabilities, privacy risks, tampered/replayed/missing data, unauthorized commands, and relevant cybersecurity threats.

### Component 5: Preliminary Validation / Benchmarking
Evidence supporting feasibility, e.g.: literature-based justification, experiments on public datasets, simulation results, baseline comparison, preliminary model results, analytical justification. **A complete prototype is NOT required.**

### Component 6: Optional Proof-of-Concept Prototype (bonus, not a prerequisite)
Examples: a preprocessing pipeline, a trained baseline model, a simulator, a simple detection module, a dashboard, a simulated communication layer.

### Component 7: Phase 1 Live Pitch
Details to be announced ("discussed soon").

> **Important note from organizers:** Teams are *not* expected to have a complete final system or real-sensor implementation at this stage. The paper should clearly explain what they propose, why it is relevant, how it will work, and how it will be evaluated in Phase 2.

---

## Phase 2 — Full-System Prototype & Real-Time Validation

Finalists (selected from Phase 1) transform their concept into a **functional end-to-end prototype**.

### Required implementation
Real sensors and/or an approved physical or simulated vehicle environment, such as: vehicle simulator, CAN interface, robotic platform, embedded platform, or another approved environment.

**Final system pipeline:** `Real Sensors → Data Acquisition → Detection/Fusion → Safety Decision → Vehicle/Simulator Response → Secure Emergency Communication`

### Real-Time Detection requirements
- Detection of ≥2 medical-event classes
- Normal driving
- Real-time or near-real-time operation
- Detection latency reported
- Confidence/uncertainty where applicable

### Secure Emergency Communication requirements
- Secure transmission
- Minimal necessary information
- Anonymization/privacy protection
- Appropriate authentication/integrity mechanisms
- Handling of communication failure

### Safety & Cybersecurity Validation
Teams must demonstrate their system under controlled failure/adversarial scenarios, such as:
- Sensor failure
- Communication failure
- Processing failure
- Tampered data
- Replayed messages
- Missing data
- Unauthorized commands

...and then demonstrate the corresponding safe/rejection behavior. **At least one controlled cybersecurity or data-integrity attack/fault scenario must be demonstrated.**

### Phase 2 Deliverables
1. **Updated IEEE-Style Research Paper (max. 6 pages)** — extends the Phase 1 paper with: final methodology, implemented architecture, experimental setup, real-world implementation, quantitative results, detection latency, classification performance, safety evaluation, cybersecurity evaluation, limitations, discussion, conclusion.
2. **Functional End-to-End Prototype** demonstrating the complete pipeline: `Sensing → Processing → Detection → Safety Decision → Vehicle Response → Secure Communication`. *"This is where you require actual implementation."*
3. **Vehicle/Safety Response demonstration**, e.g.: medical event detected → confidence assessment → safety decision → vehicle action → emergency notification. Exact vehicle action depends on the team's proposed scenario.

---

## Rules & Criteria

- Open to Student Branches.
- **Maximum 5 members per team.**
- Teams must address **at least 2 medical-event classes + normal driving**.
- Phase 1 may use simulated, synthetic, or public de-identified data.
- Phase 1 does **not** require a complete working prototype.
- Phase 1 proof-of-concept implementations are allowed and may strengthen a team's evaluation (bonus, not required).
- Phase 2 finalists **must** develop a functional end-to-end prototype.
- Phase 2 **must** use real sensors and an approved physical, embedded, robotic, CAN, or vehicle-simulation environment.
- Solutions must address safety, cybersecurity, and privacy.
- Phase 2 teams must demonstrate controlled handling of system failures and/or malicious/tampered data.
- All experiments and datasets must respect applicable privacy and ethical requirements.

---

## Timeline

| Date | Milestone | Notes |
|---|---|---|
| **15/09/2026** | Challenge Infosession | Kickoff / Q&A |
| **01/11/2026** | ⚠️ **Phase 1 Submission Deadline** | IEEE-style paper (max. 5 pages) due |
| **6–8 November 2026** | Phase 1 Pitching — Day 2 of the IEEE Vehicular Technology Summit (VTS) Tunisia 2026 | Selected Phase 1 participants get up to 2 free passes per Student Branch; no registration fee for presenting members |
| **12/12/2026** | ⚠️ **Final Submission Deadline** | Updated paper (max. 6 pages) + functional prototype due |

### ⚠️ Critical-path deadlines
- **The Phase 1 paper deadline (01/11/2026) sits only 5–7 days before the Phase 1 live pitch (6–8 Nov 2026)** at the VTS Summit. There is essentially no buffer between finishing the paper and presenting it live — pitch prep (slides, demo rehearsal, Q&A prep) must start **before** the paper is finalized, not after.
- **The Final Submission (12/12/2026) bundles both the updated paper *and* the working prototype.** Since Phase 2 requires real sensors/hardware and a demonstrated fault/attack scenario, hardware integration and adversarial-scenario testing (the most time-consuming parts) need to be scheduled well before this date — not squeezed in during the final week.

---

## Pitching Format

- Language: **English**
- **4 minutes** presentation
- **2 minutes** demo
- **2 minutes** Q&A

(Applies to the live pitch stages; Phase 1 pitch details to be confirmed by organizers.)

---

## Scoring / Evaluation Criteria

**TOTAL: 105 points + up to 4 bonus points**

### Phase 1 — 55 points

| Criterion | Points |
|---|---|
| Detection Reliability & Robustness | 10 |
| Multi-Etiology Differentiation | 10 |
| Clinical & Epidemiological Grounding | 10 |
| Vehicle Architecture | 10 |
| CAN/V2X Message Design & Real-Vehicle Integrability | 10 |
| Fail-Safe & Fault Handling Design | 5 |
| **Subtotal** | **55** |

### Phase 2 — 50 points

| Criterion | Points |
|---|---|
| Cybersecurity & Privacy Design | 15 |
| Code Quality & Benchmarking Reproducibility | 15 |
| Report Quality & Architecture Documentation | 10 |
| Live Pitch | 5 |
| Innovation & Creativity | 5 |
| **Subtotal** | **50** |

### Bonus — up to 4 points

| Bonus condition | Points |
|---|---|
| At least one IEEE VTS member on the team | +1 |
| At least one IEEE EMBS member on the team | +1 |
| Documented engagement with a clinical/biomedical, EMS, cybersecurity, or automotive-industry contact for validation | +2 |

---

## Logistics

- **Team size:** maximum 5 members per team.
- **Eligibility:** open to Student Branches.
- **Deliverables:**
  - Phase 1: IEEE-style research paper, max. 5 pages.
  - Phase 2: Updated IEEE-style research paper, max. 6 pages + functional end-to-end prototype.
- **Submission:** "Submit your project and show us what you've built" (submission channel/platform to be confirmed via organizers).
- **Contact:** for any inquiries or clarifications, email **vts@ieee.tn** or **embs@ieee.tn**.
- **Perks:** Selected Phase 1 participants receive up to 2 free passes per Student Branch to the IEEE VTS Summit Tunisia 2026, with no registration fee for presenting members.

---

## Tools, Knowledge & Hardware Needed

**Domain knowledge:**
- Basics of the target medical conditions: epileptic seizure, cardiac syncope/arrhythmia, severe hypoglycemia, acute stroke — physiological/behavioral signatures relevant to driving impairment.
- Driver-monitoring / automotive HMI concepts (distinguishing medical events from fatigue/distraction).
- Automotive networking: CAN-bus, V2X messaging.
- Cybersecurity fundamentals: trust boundaries, authentication/integrity, replay/tamper attack models, threat modeling.
- Privacy-preserving data handling / anonymization techniques.
- IEEE conference paper writing (structure, referencing, technical writing).

**Technical / AI skills:**
- Multimodal sensor fusion (cameras, in-cabin motion sensors, seat sensors, steering input, CAN telemetry).
- Signal processing and feature extraction from physiological/behavioral data.
- Classification/detection modeling (ML/DL), including confidence/uncertainty estimation and false-positive/negative trade-off analysis.
- Real-time or near-real-time system design and latency benchmarking.
- Secure communication protocol design (encryption, authentication, integrity checks).

**Hardware / platforms (Phase 2 especially):**
- A vehicle simulator, CAN interface, robotic platform, or embedded platform (or another organizer-approved environment).
- Real sensors — e.g., cameras, motion sensors, seat sensors — matching the team's chosen modalities.
- A test setup capable of injecting controlled faults/attacks (sensor failure, communication failure, tampered/replayed/missing data, unauthorized commands) to validate fail-safe behavior.

**Data (Phase 1):**
- Simulated data, synthetic data, public de-identified datasets, or literature-derived assumptions are all acceptable — no real patient data required at this stage.

---

## Why We Should Engage

- **Cross-society, high-visibility challenge:** backed by IEEE Region 8, IEEE Tunisia Section, IEEE VTS, and IEEE EMBS — strong networking and visibility opportunity for ENSI's Student Branch.
- **Direct access to the IEEE Vehicular Technology Summit Tunisia 2026** (6–8 November 2026) for teams that clear Phase 1 — free passes and no registration fee for presenters is a concrete, tangible incentive.
- **Genuinely interdisciplinary:** combines embedded systems, AI/ML, automotive networking (CAN/V2X), cybersecurity, and biomedical/clinical reasoning — a strong showcase for ENSI students across multiple specializations, and a natural fit for cross-club collaboration (e.g., with a biomedical or cybersecurity-focused club).
- **Low barrier to entry for Phase 1:** no real hardware, real patients, or complete prototype required — teams can validate their concept with simulated/synthetic/public data and literature review, lowering the initial commitment while still competing for 55 of the 105 points.
- **Bonus points reward exactly the kind of outreach IEEE branches are built for:** IEEE VTS/EMBS membership and engaging a real clinical, EMS, cybersecurity, or automotive-industry contact for validation — worth up to 4 extra points and a good excuse to build external partnerships.
- **Realistic, safety-critical problem space:** the fail-safe design, cybersecurity threat modeling, and privacy-preservation requirements make this a strong portfolio/CV project beyond the competition itself.

## Next Steps

1. **Attend/relay the Challenge Infosession on 15/09/2026** to get full submission and pitch details as they're released.
2. **Recruit an interdisciplinary team of up to 5 members** — ideally mixing embedded/AI, cybersecurity, and someone comfortable researching the medical/clinical angle.
3. **Assign an early owner for the IEEE-style paper** (max. 5 pages) — given the tight gap between the 01/11/2026 deadline and the 6–8 Nov pitch, target an internal draft deadline well before 01/11/2026 to leave time for pitch prep.
4. **Reach out early to a clinical/biomedical, EMS, cybersecurity, or automotive-industry contact** for the +2 bonus points — this takes lead time to arrange, so start now rather than in Phase 2.
5. **Encourage members to join IEEE VTS and/or IEEE EMBS** to secure the +1/+1 bonus points.
6. **If selected for Phase 2, plan hardware/prototype work (sensors, CAN/simulator environment, fault-injection testing) starting immediately after Phase 1 results** — don't wait until close to 12/12/2026, since Phase 2 requires a full working prototype plus a demonstrated attack/fault scenario.
7. **Contact vts@ieee.tn or embs@ieee.tn** with any open questions before committing team resources.
