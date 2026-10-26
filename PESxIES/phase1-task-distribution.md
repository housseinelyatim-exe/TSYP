# EnergyMind Tunisia — Phase 1 Task Distribution

*Deadline: **15 Oct 2026**. Today is 9 Oct, so we have **6 working days**. One member already owns the dataset.*

---

## 1. What Phase 1 actually asks for

| Deliverable | Contents | Points it feeds |
|---|---|---|
| **Project Proposal** | Scope, objectives, data/anomaly-simulation plan, preliminary design for **each of the 4 goals** | Adherence (10), Technical approach (20), Innovation (10) |
| **GitHub repo / Kaggle notebook** | Dataset, plus the code written during Phase 1 | Technical approach (20), Quality & clarity (10) |
| *(Bonus)* | Business scope: budget, deployment, continuous training, integration cost | +1 |

Phase 1 is graded on **design and data**, not on a finished product. So split the work by **deliverable section**, not by "who codes the big model".

---

## 2. The roles (5 people)

### 👤 A — Dataset & anomaly injection *(already assigned)*
The most important role: the anomaly-generation documentation is graded directly.
- Pick the baseline source: a Pandapower IEEE 14-bus time series, a smart-meter dataset, or STEG data.
- Build a **labelled dataset** with `normal`, `genuine_event` (surge or outage), `equipment_fault`, `sensor_drift`, `bias`, and `falsified` (FDI).
- Script the injection so it can be reproduced (`src/data/inject.py`, fixed seed).
- Write `docs/data_card.md`: the source, how each anomaly type is generated (formula and parameters), the class balance, and known limits.
- Provide the proposal section **"Data & anomaly-simulation plan"**.

### 👤 B — Detection (Goal 1)
- Build the physics baseline: a WLS state estimator, or a simple power-balance check, and compute residuals.
- Build a first detector: Isolation Forest on the residuals, compared with an autoencoder or One-Class SVM if time allows.
- Write a **genuine-event vs. data-fault** rule: if many correlated sensors deviate, it is a grid event; if one sensor deviates alone, it is a data problem.
- Report a precision/recall table per anomaly type in a notebook.
- Provide the proposal section **"Goal 1: Detection design"**.

### 👤 C — Explainability + escalation (Goals 2 & 3)
- Define the confidence score (detector score → calibrated 0–1).
- Wrap SHAP or LIME around B's model, using a dummy model until B's is ready.
- Define the **decision-log JSON schema**: what was detected, its confidence, the explanation, the action taken, and who approved it.
- Write an escalation table: confidence × severity → auto-act / auto-log / human approval. Cover over-trust and under-trust.
- Make a low-fidelity operator UI mockup (Figma or a Streamlit sketch).
- Provide the proposal sections **"Goal 2"** and **"Goal 3"**.

### 👤 D — Proposal lead / PM + Goal 4 + business
- Own the proposal document: scope, objectives, architecture diagram, and final editing.
- Write the Goal 4 design (shared learning across nodes): FedAvg-style sharing of anomaly signatures and calibration offsets, with raw data kept local. Include a "shared vs. local and why" table.
- Write the **business scope** paragraph for the bonus point.
- Run the daily 15-min sync and track the checklist in §5.

### 👤 E — Repo, integration & innovation
- Set up the repo skeleton on day 1 (structure in §4), the README, `requirements.txt`, and a Kaggle notebook that runs everything from start to finish.
- Join A's data, B's detector, and C's explanation and log into **one demo notebook**: input data → flag → explanation → escalation decision.
- Produce figures for the proposal: the anomaly examples plot, the confusion matrix, and a SHAP plot.
- Own the "innovation" angle and make sure the proposal states it clearly. Example: the physics-plus-ML hybrid, so explanations point to physical laws.

> **Only 4 people?** Merge E into D (PM + repo), and C takes the README.
> **Only 3 people?** A = data, B = detection + explainability, C = proposal + governance + Goal 4 + repo.

---

## 3. Keeping the dataset from becoming a bottleneck

Everyone depends on A, so **agree on a data contract on day 1** and have people work on fake data until the real data arrives.

**Schema (fixed on 9 Oct):**
```
timestamp, node_id, sensor_id, bus, V, I, P, Q, freq,
label, anomaly_type, anomaly_id, injected (0/1)
```

| Drop | Date | Contents |
|---|---|---|
| **v0** | 10 Oct evening | Small sample: baseline plus 2 anomaly types (drift, bias). Enough for B and C to start. |
| **v1** | 12 Oct | All 6 classes, full size, injection script committed |
| **final** | 13 Oct | Frozen. The data card is complete. No changes after this. |

Until v0 arrives, B and C use a 20-line synthetic generator (sine wave + noise + spikes) that follows the same schema.

---

## 4. Repo skeleton (E sets this up on 9 Oct)

```
energymind-tunisia/
├── README.md                 # scope, how to run, team
├── data/                     # A
│   ├── raw/  processed/
├── docs/
│   ├── data_card.md          # A
│   ├── escalation_policy.md  # C
│   ├── decision_log_schema.json  # C
│   ├── collective_learning.md    # D
│   └── proposal.pdf          # D
├── src/
│   ├── data/   (baseline.py, inject.py)   # A
│   ├── detect/ (wls.py, detector.py)      # B
│   └── explain/ (explain.py, escalate.py) # C
└── notebooks/
    ├── 01_dataset.ipynb      # A
    ├── 02_detection.ipynb    # B
    ├── 03_explain_escalate.ipynb  # C
    └── 00_end_to_end_demo.ipynb   # E
```

---

## 5. Day-by-day plan

| Day | A (Data) | B (Detect) | C (Explain/Gov) | D (PM/Proposal) | E (Repo/Integr.) |
|---|---|---|---|---|---|
| **Thu 9** | Pick source and lock the schema | Read up on WLS/FDI and start the dummy generator | Draft the decision-log schema | **Lock the scope slice** and write the proposal outline | Repo skeleton and README |
| **Fri 10** | **v0 drop** | Residuals + Isolation Forest on v0 | SHAP wrapper on a dummy model | Write scope/objectives and the architecture diagram | CI/run check and the Kaggle notebook shell |
| **Sat 11** | Add the remaining anomaly types | Event-vs-fault rule | Escalation table and over/under-trust | Goal 4 design doc | Start the end-to-end notebook |
| **Sun 12** | **v1 drop** and start the data card | Metrics per anomaly type | UI mockup | Business scope section | Plug in v1 and make figures |
| **Mon 13** | **Data freeze** and finish the data card | Final numbers and write the Goal 1 section | Write the Goal 2 and Goal 3 sections | Merge all sections into the proposal | End-to-end notebook runs cleanly |
| **Tue 14** | Review the proposal | Review the proposal | Review the proposal | **Final edit and PDF** | README polish and repo cleanup |
| **Wed 15** | — | — | — | **Submit (morning, not at midnight)** | Tag the release `v-phase1` |

---

## 6. Final checklist (D owns it)

- [ ] Scope slice stated in one sentence
- [ ] All **4 goals** have a design section (Goal 4 can be design only)
- [ ] Anomaly-generation method documented: data card + proposal section
- [ ] Dataset in the repo or linked (Kaggle/Drive if it is too large)
- [ ] Phase 1 code runs from the README instructions
- [ ] Confidence score, explanation and decision-log example shown
- [ ] Escalation thresholds table, with over-trust and under-trust addressed
- [ ] "Shared vs. local and why" privacy table
- [ ] Business scope paragraph (bonus)
- [ ] Team membership listed: PES / IES / YP / dual PES+IES (up to +4 bonus)
- [ ] Proposal written in English and proofread
