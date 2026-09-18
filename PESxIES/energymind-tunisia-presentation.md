# EnergyMind Tunisia (Architects of the Energy Noosphere: A Human-AI Collective Intelligence Network for Energy Resilience) — TSYP14 Technical Challenge

## Overview

**EnergyMind Tunisia** is a TSYP14 Technical Challenge organised under IEEE Region 8, IEEE Tunisia Section (Student Activities Committee & Technical Activities Committee), IEEE Young Professionals Tunisia Section, INSAT IEEE Student Branch, the **IEEE PES (Power & Energy Society) Tunisia Chapter**, and the **IEEE IES (Industrial Electronics Society) Tunisia Section Chapter**.

**Scope & topic:** the challenge invites participants to build the **trust layer** of Tunisia's energy systems — an AI that detects when data or equipment is failing, faulty, or feeding the system false information, and decides transparently when it can act alone and when a human must decide.

**Challenge problem:** Tunisia's grid faces growing strain from seasonal peaks, fast-expanding renewable energy, increasing smart meters, and growing numbers of IoT devices. These create more points where a fault, miscalibration, or biased reading can silently corrupt the data automated systems rely on. As AI takes on more grid decisions, the question is not only whether it predicts well, but **can it be trusted, and who is accountable when it is wrong?** Teams must design an AI system that stands between raw energy data and automated action.

---

## Challenge Goal — 4 required components

Teams choose one part of the energy system to monitor — **Microgrid · Factory power line · Smart-metered neighborhood · Simulated grid segment** — and must address all four goals below for that chosen slice:

### 1. Anomaly & Bias Detection
Monitor incoming energy/grid data (Voltage, Current, Power Quality, Smart-Meter Readings) and detect: equipment faults, degraded sensors, biased readings, corrupted/falsified readings, and natural equipment failures. The system must distinguish a **genuine grid event** (e.g. a real surge or outage) from a **data-quality problem**, because each requires a different response.

### 2. Confidence Scores & Explainability
Every flagged event must produce a verdict a human can understand and verify: a confidence score, a plain-language explanation, and an auditable decision log recording what was detected, concluded, and why. Teams are encouraged to use interpretable approaches (SHAP, LIME, rule-backed models, interpretable ensembles) — **black-box scoring that can't be examined should be avoided.**

### 3. Human-AI Escalation & Governance
Clearly define what the AI can do independently versus when a human operator must decide: define thresholds for automatic corrective actions, define situations requiring human approval, provide an operator interface for rapid review/override/approval, and address **both** over-trust and under-trust of the AI.

### 4. Shared Learning Across the Noosphere
Design and document how multiple nodes (factories, neighborhoods, microgrids) could share anomaly patterns, calibration insights, and other relevant knowledge — explicitly addressing privacy (what is shared, what remains local, and why). **A working single-node prototype is required; multi-node sharing may remain a documented design only.**

---

## Challenge Instructions

**I. Scope Definition** — each team defines the specific slice of the energy system it will monitor and designs the solution against all four Challenge Goals above.

**II. Datasets** — real fault/anomaly-labeled grid data is rare, so simulation is expected. Teams may inject synthetic faults, sensor drift, biased readings, or falsified readings into real or realistic baseline data from public sources, **STEG open data**, or simulated equivalents. **Teams must document how the anomalies were generated.**

**III. Technical Insights & Hints**

| Area | Suggested approaches |
|---|---|
| Anomaly Detection | Isolation Forest · Autoencoders · One-Class SVM · Statistical outlier methods |
| Explainability | SHAP · LIME · Rule-backed scoring · Readable decision logs |
| Escalation Logic | Rule-based thresholds · Confidence-based routing |
| Collective Defense | Lightweight multi-agent concepts · Federated concepts · Documented sharing protocol |
| Evaluation | Detection precision/recall · False-positive rate · Explanation quality · Response latency |

---

## Challenge Phases — Breakdown

### Phase 1: Ideation & Data Exploration
**Deliverables:**
- **Project Proposal** covering: Scope · Objectives · Data/anomaly-simulation plan · Preliminary design for each of the 4 Challenge Goals.
- **GitHub Repository and/or Kaggle Notebook** containing the dataset and the code developed during Phase 1.

### Phase 2: Solution Development & Deployment
**Deliverables:**
- **Full Project Report** covering the complete workflow, escalation logic, and collective-defense design.
- **GitHub Repository** containing the full solution code, trained models, and application files.
- **Demo Video** showcasing the working solution.
- **5-minute Presentation** summarizing project, results, and impact.

### Pitching format
English · **5 min presentation** · **3 min demo**

---

## Timeline

| Milestone | Date |
|---|---|
| Challenge Infosession | **17/09/2026** |
| Phase 1 Submission Deadline | **15/10/2026** |
| Phase 2 Final Submission Deadline | **12/12/2026** |

> 🚩 **Critical-path flags:**
> - The **Infosession on 17/09/2026** is imminent — attend it to clarify what counts as an acceptable "realistic baseline" energy dataset before committing to a data-simulation plan.
> - About **4 weeks** separate Phase 1 (15/10) from the Infosession, then nearly **2 months** run from Phase 1 to the Final deadline (12/12) — comfortably the longest Phase-1-to-Final runway among the TSYP14 challenges reviewed, but the scope is also the most research-heavy (anomaly detection **and** explainability **and** escalation governance **and** a documented multi-node sharing design), so this time should be budgeted across all four goals early, not spent perfecting only the anomaly-detection model.
> - Because labeled real fault data is rare, **the anomaly-injection methodology must be designed and documented from the start** — this is graded directly under "Technical Approach" (20 of Phase 1's 50 points) and cannot be bolted on late.

---

## Scoring & Evaluation Criteria

**Total score: 100 points**

### Phase 1 — Pre-selection (50 points)

| Criterion | Points |
|---|---|
| Adherence to Challenge Requirements | 10 |
| Technical Approach | 20 |
| Quality & Clarity of Deliverables | 10 |
| Innovation and Creativity | 10 |

### Final Phase (45 points)

| Criterion | Points |
|---|---|
| Technical Approach | 20 |
| Prototype Functionality & Features | 10 |
| Live Presentation Quality | 5 |
| Quality & Clarity of Deliverables | 10 |

### Bonus (5 points)

| Bonus condition | Points |
|---|---|
| At least one PES member on the team | 1 |
| At least one IES member on the team | 1 |
| At least one YP member on the team | 1 |
| At least one member holding **both** PES and IES membership | 1 |
| Covering the business scope — budget, solution implementation, production, continuous training, integration and deployment cost | 1 |

*(50 + 45 + 5 = 100 — this poster's scoring adds up cleanly, unlike some other TSYP14 challenge posters.)*

---

## Logistics

- **Team size: maximum 5 members**, open to Student Branches.
- **Submission:** "Submit your project and show us what you've built."
- **Contact:** for inquiries or clarifications, email **ranimdamak@ieee.org** or **mohamedali.krichen@ieee.org**.

### Prizes — 3 winning teams
Prizes **to be announced** — will be finalized and officially confirmed before TSYP14.

---

## Tools, Knowledge & Hardware Needed

**Knowledge / skills**
- Anomaly/outlier detection for time-series or tabular sensor data (Isolation Forest, Autoencoders, One-Class SVM, statistical methods).
- Explainable AI (XAI) techniques — SHAP, LIME, or rule-backed/interpretable models — and how to turn a model verdict into a plain-language, auditable explanation.
- Rule-based / threshold-driven escalation and decision-routing design (human-in-the-loop system design).
- Basic grid/power-systems domain knowledge (voltage, current, power quality, smart-meter data) sufficient to distinguish a genuine grid event from a data-quality fault.
- Data simulation/augmentation methodology: injecting and documenting synthetic faults, sensor drift, and bias into baseline data.
- Privacy-aware system design (what is shared vs. kept local across nodes) and, optionally, lightweight multi-agent or federated-learning concepts for the "Noosphere" sharing design.
- Business-case framing (budget, deployment/integration cost, continuous training) for the 1-point bonus criterion.
- English technical writing and pitching (5-min presentation + 3-min demo).

**Tools**
- Python ML/data-science stack (scikit-learn, PyOD, or similar) for anomaly detection, plus SHAP/LIME libraries for explainability.
- **GitHub** and/or **Kaggle Notebook** — both explicitly named as acceptable Phase 1 submission formats.
- Dashboard/UI tooling (e.g., Streamlit, a lightweight web app) for the required human-operator review/override interface.
- Video recording/editing for the Phase 2 demo video.

**Hardware**
- **No special hardware is required** — this is a data/software challenge; a working single-node prototype can run entirely on standard laptop-class compute against simulated or public/STEG grid data.
- Real hardware (e.g., an actual smart meter or microgrid testbed) is not mandated and would only be a differentiator, not a requirement, unlike the CAS or SIGHT/NEXUS TSYP14 challenges.

---

## Why IEEE ENSI SB Should Engage

- **Pure software/data challenge with no hardware barrier to entry:** unlike several other TSYP14 challenges (CAS, SIGHT/NEXUS, VTS×EMBS), a working submission needs no physical prototype or component sourcing — lowering the cost of fielding a team.
- **Directly relevant, high-demand skill set:** anomaly detection + explainable AI + human-in-the-loop governance is squarely in the "trustworthy AI" space that's valuable on a CV regardless of whether a team places.
- **Clean, additive scoring (50 + 45 + 5 = 100)** makes it easy to plan effort allocation across phases — unlike some sibling challenges where the published rubric doesn't sum to the stated total.
- **Longest Phase 1 → Final runway reviewed so far (~2 months)** gives a team more room to iterate on the hardest part of the brief — the collective-defense/privacy design — without the extreme time pressure seen in some other TSYP14 challenges.
- **Dual-society bonus structure (PES + IES + YP)** is a concrete, low-effort recruiting incentive ENSI SB can act on immediately when forming the team.

## Next Steps

1. **Attend the Challenge Infosession on 17/09/2026** — confirm what "realistic baseline" energy data is acceptable and whether organiser-provided STEG data (or access to it) will be shared.
2. **Form a team of up to 5 members**, ideally including at least one PES member, one IES member, one YP, and one member with dual PES/IES membership to capture the full 4-point membership bonus.
3. **Pick one energy-system slice** (microgrid / factory line / smart-metered neighborhood / simulated segment) early, since the anomaly-simulation plan and preliminary design for **all four** Challenge Goals are due at Phase 1 (15/10/2026).
4. **Design and document the synthetic-anomaly-injection methodology from day one** — it's explicitly required documentation and is graded under Phase 1's 20-point Technical Approach criterion.
5. **Prioritize interpretable methods (SHAP/LIME/rule-backed models) over black-box models from the start**, since explainability is a first-class, separately-scored requirement, not an add-on.
6. **Block the critical dates on the SB calendar:**
   - 17/09/2026 — Infosession
   - 15/10/2026 — Phase 1 Submission (Project Proposal + GitHub/Kaggle)
   - 12/12/2026 — Phase 2 Final Submission (Full Report, GitHub, Demo Video, 5-min Presentation)
7. **Contact ranimdamak@ieee.org or mohamedali.krichen@ieee.org** with any open questions on dataset access or scope before committing team resources.
