# Ground Truth Under Attack: Securing the Earth Observation Chain — TSYP14 Technical Challenge

## Overview

**Ground Truth Under Attack: Securing the Earth Observation Chain** is a TSYP14 Technical Challenge hosted collaboratively by three IEEE Tunisia chapters: the **IEEE Computational Intelligence Society (CIS) Tunisia Chapter**, the **IEEE GRSS Tunisia Section Chapter** (Geoscience and Remote Sensing), and the **IEEE Signal Processing Society (SPS) Tunisia Chapter** — under IEEE Region 8, IEEE Tunisia Section, IEEE Young Professionals Tunisia Section, and INSAT IEEE Student Branch.

**Scope & topic:** Earth-observation products support decisions in agriculture, insurance, water management and disaster response. Their trustworthiness depends on evidence of origin, time, integrity and processing history across the sensing, communication and product chain. Teams select **one segment** — ground link, in-situ sensing, or imagery — and build a **verifiable defensive prototype** combining the three chapters' expertise:
- Remote sensing (GRSS)
- Signal/image processing (SPS)
- Computational intelligence and security analytics (CIS)

**Challenge problem statement:** documented navigation interference, false-data injection and increasingly capable image synthesis show that plausible-looking data may still be untrustworthy. A failure may remain **silent** — the pipeline continues to operate while a corrupted observation reaches the analyst. The challenge focuses on:
- Provenance
- Integrity verification
- Anomaly detection
- Controlled adversarial testing

**Challenge goal:** select one track and defend it —
- Use authentic public data
- Apply the common standard scenario
- Detect or prevent the attack
- Report detection quality, false alarms, latency, memory and security overhead

> No purchase is required — a software or emulated trust anchor and local laptop execution are valid.

## Thematic Tracks (each team chooses exactly one)

| Track | Focus |
|---|---|
| **Track 1** — Secure Ground-Link Testbed | Securing the ground-link segment |
| **Track 2** — False-Data Injection | Detecting/preventing false-data injection |
| **Track 3** — Trust the Pixel | Verifying imagery integrity/provenance |

## Required Deliverables (all teams must complete all six)

1. Threat model & segment analysis
2. Platform / architecture / trust anchor
3. Signal / image processing
4. AI or statistical detection
5. Adversarial validation & response
6. Documentation using the official reference datasets

## Challenge Phases — Breakdown

### Phase 1: Anonymous Report + Code Submission (Deadline: 8 November 2026)

**Deliverables:**
- Anonymous Report
- GitHub Repository
- Prototype
- Documentation

The administrative committee assigns a **team code** and **sanitizes the repository** before forwarding it to the jury. Up to **7 finalists** advance to Phase 2.

> ⚠️ **Important note (verbatim from organisers):** Phase 1 submissions are **fully anonymous** — no names, unit names, logos or identifying repository metadata.

### Phase 2: Final Prototype & Pitch (Deadline: 11 December 2026)

Finalists build a **working prototype** and present a **live or replayable attack demonstration** during TSYP14.

> Phase 2 deliverables are **non-anonymous** due to the live pitch.

**Pitching format:** English · **7 min pitching** · **3 min Q&A**

> The final session will accommodate **up to 7 finalist teams within a 1h30 session**.

## Timeline

| Milestone | Date |
|---|---|
| Challenge Infosession | **11/09/2026** |
| First (Phase 1) Submission Deadline | **08/11/2026** |
| Preselection Announcement | **10/11/2026** |
| Final (Phase 2) Deadline | **11/12/2026** |

> 🚩 **Critical-path flags:**
> - The **Infosession on 11/09/2026** is only days away.
> - The **Preselection Announcement lands just 2 days after the Phase 1 deadline** (08/11 → 10/11) — finalists get essentially no ramp-up notice and must immediately pivot into Phase 2 build mode, leaving only about **one month** (10/11 → 11/12) to turn an anonymous prototype into a working, live-demoable, non-anonymous end-to-end system with a 7-minute pitch.
> - **Anonymity compliance in Phase 1 is a hard, easy-to-violate constraint** — no names, unit names, logos, or identifying repository metadata. A single slip (e.g., a GitHub username, README credit, or file metadata) could compromise a submission before the committee even sanitizes it — teams should build with anonymity in mind from day one, not scrub it at the last minute.
> - Only **7 of however many teams enter** advance — Phase 1 quality (especially Detector Design & Evaluation and Standard Scenario & Evasion, the two highest-weighted 20-point items) is the real gate; teams should not under-invest in Phase 1 assuming Phase 2 is where it "really" counts, since Phase 1 is also scored out of 100 and rolled into the weighted final score.

## Scoring & Evaluation Criteria

**Total score: 100 points**, computed as a **weighted blend across phases**:

> **Final Score = 30% × Phase 1 Score + 70% × Phase 2 Score**

(Each phase is itself scored out of 100 points before weighting.)

### Phase 1 — Anonymous Selection (100 points, weighted 30% of final score)

| Criterion | Points |
|---|---|
| Threat model & relevance | 15 |
| Architecture & trust mechanism | 15 |
| Signal / image processing | 15 |
| Detector design & evaluation | 20 |
| Standard scenario & evasion | 20 |
| Feasibility, affordability & local execution | 10 |
| Clarity & reproducibility | 5 |

### Phase 2 — Final Prototype & Pitch (100 points, weighted 70% of final score)

| Criterion | Points |
|---|---|
| End-to-end functional prototype | 20 |
| Provenance / security control | 15 |
| Processing & local detection | 15 |
| Held-out standard attack & evasion | 20 |
| Metrics, efficiency & accessibility | 10 |
| Documentation & reproducibility | 10 |
| Pitch & technical questions | 10 |

### Tie-break order
1. Held-out attack/evasion score
2. Lower false-alarm rate
3. Documented jury decision

### Bonus points
**No bonus points are awarded.** Membership/status in GRSS, SPS, CIS, YP or WIE does **not** affect the score. Hardware, prototype presentation and business-scope coverage are already evaluated within the criteria above.

## Logistics

### Rules & eligibility
- **This challenge is for Student Branches (SB) only.**
- **Team size: 5 members maximum.**
- Teams must choose **exactly one track**.
- Teams must use the **official reference datasets** for the standard evaluation scenario.
- Phase 1 submissions must remain **anonymous**.
- Phase 2 submissions are **non-anonymous** (live pitch).
- Up to **7 teams** are selected as finalists.

### Deliverables by phase
| Phase | Deliverables |
|---|---|
| Phase 1 | Anonymous Report, GitHub Repository, Prototype, Documentation |
| Phase 2 | Working prototype, live/replayable attack demonstration, 7-min pitch + 3-min Q&A |

### Submission
> "Submit your project and show us what you've built."

### Contact
For any inquiries or clarifications: **ghassen.ltaif@ieee.org**

### Prizes — 3 winning teams, total pool 1500 DT
| Place | Prize |
|---|---|
| 1st | **800 DT** |
| 2nd | **500 DT** |
| 3rd | **200 DT** |

## Tools, Knowledge & Hardware Needed

**Knowledge / skills**
- Threat modeling for sensing/communication/product chains (segment analysis of ground link, in-situ sensing, or imagery)
- Cryptographic or trust-anchor concepts for provenance and integrity verification (software or emulated trust anchor is acceptable — no special hardware purchase required)
- Signal processing and/or image processing fundamentals, depending on chosen track
- AI/ML or statistical anomaly-detection methods (detector design and evaluation is a 20-point criterion in Phase 1 and folds into Phase 2's held-out attack evaluation)
- Adversarial testing / red-teaming methodology — designing and evaluating evasion attempts against your own detector
- Metrics reporting discipline: detection quality, false-alarm rate, latency, memory, and security overhead must all be reported
- Technical writing under anonymity constraints (Phase 1 report) and live technical pitching in English (Phase 2)

**Tools**
- **GitHub** for the Phase 1 code repository (must be scrubbed of identifying metadata before submission)
- Official reference datasets provided by organisers for the standard evaluation scenario (required, not optional)
- Signal/image processing libraries and AI/ML frameworks appropriate to the chosen track
- Reproducible documentation tooling (Clarity & Reproducibility and Documentation & Reproducibility are explicit scored criteria in both phases)

**Hardware**
- **No purchase required** — a software or emulated trust anchor and local laptop execution are explicitly valid.
- Track-dependent optional hardware: ground-link/radio testbed components (Track 1), sensor hardware for in-situ data (Track 2), or imaging/camera hardware (Track 3) — but all tracks are solvable with public data and local/software execution alone.

## Why IEEE ENSI SB Should Engage

- **Deep technical credibility:** hosted jointly by CIS, GRSS and SPS, this challenge sits squarely in cutting-edge security/AI/signal-processing territory — strong for ENSI SB members building a portfolio in cybersecurity, remote sensing, or applied AI.
- **Meritocratic, anonymized Phase 1:** scoring explicitly states membership/status in GRSS, SPS, CIS, YP or WIE does not affect the score — a level playing field where technical quality alone decides advancement, which is motivating for less-established teams.
- **Highest prize pool of the three challenges reviewed so far:** 1500 DT total (800/500/200 DT), a meaningful incentive for competitive teams.
- **SB-only eligibility** means ENSI SB is competing directly against peer Student Branches rather than open categories — a clear, comparable benchmark of ENSI's standing within IEEE Tunisia.
- **Team size up to 5** allows a slightly larger, more specialized team than the other TSYP14 challenges reviewed (which cap at 3–4), enabling role split across threat modeling, signal/image processing, detection/AI, and adversarial testing.

## Next Steps

1. **Attend the Challenge Infosession on 11/09/2026** — only days away; use it to clarify anonymity requirements and get the official reference datasets/standard scenario details.
2. **Form a team of up to 5 members** with complementary skills (security/threat modeling, signal or image processing, ML/AI detection, and adversarial testing) and pick **one track** (Ground-Link Testbed / False-Data Injection / Trust the Pixel).
3. **Build anonymity into the workflow from day one** — separate GitHub org/account for submission, no branding, no identifying metadata — rather than trying to scrub it right before the 08/11/2026 deadline.
4. **Block the critical dates on the SB calendar:**
   - 11/09/2026 — Infosession
   - 08/11/2026 — Phase 1 (Anonymous Report + Code) due
   - 10/11/2026 — Preselection Announcement (only 2 days later — be ready to move immediately into Phase 2 if selected)
   - 11/12/2026 — Final Deadline (working prototype + live/replayable demo + pitch)
5. **Decide on SB-level support:** consider pairing the team with CIS/GRSS/SPS-affiliated mentors if available, and budget internal review time for the Phase 1 report given its 30% weight and the tight 1-month Phase 1→Phase 2 runway if selected.
