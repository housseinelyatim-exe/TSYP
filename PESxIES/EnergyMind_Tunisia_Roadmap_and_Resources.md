# EnergyMind Tunisia — Roadmap Sketch & Research Resources

*Prepared for the supervisor / PM ahead of the team kickoff meeting.*

---

## 1. Project Snapshot

| Item | Detail |
|---|---|
| Challenge | EnergyMind Tunisia — TSYP14 Technical Challenge |
| Core ask | Build an AI "trust layer" that detects faulty/biased/falsified grid data, explains its verdicts, and knows when to defer to a human |
| Scope choice | One slice: microgrid, factory power line, smart-metered neighborhood, or simulated grid segment |
| Team size | Max 5 members |
| Phase 1 deadline | **15 October 2026** — Project Proposal + GitHub/Kaggle repo |
| Phase 2 deadline | **12 December 2026** — Full report, code, trained models, demo video, 5-min presentation |
| Scoring | 50 (Phase 1) + 45 (Final) + 5 (bonus) = 100 |

The four graded goals, in one line each:
1. **Detect** — tell equipment faults / sensor drift / bias / falsification apart from real grid events.
2. **Explain** — every flag needs a confidence score, plain-language reasoning, and an audit log. No black boxes.
3. **Govern** — define what the AI can act on alone vs. what needs a human, with an operator interface.
4. **Share (design only)** — document how multiple nodes could share anomaly knowledge without leaking raw data. Only the single-node prototype must actually work.

---

## 2. Roadmap Sketch

### Phase 1 — now through 15 Oct (≈3 weeks)

| Week | Focus | Owner(s) | Output |
|---|---|---|---|
| 1 | Lock scope slice; set up grid model (IEEE 14/57-bus via MATPOWER/Pandapower, or STEG data if available); define "normal operation" baseline | Domain + data engineer | Working data pipeline, baseline dataset |
| 1–2 | Implement WLS state estimator (physics baseline); design and start coding the fault-injection methodology (drift, bias, falsified readings) and **document it as you go** | Data engineer + domain expert | Documented anomaly-injection methodology (this is graded directly, 20/50 points) |
| 2 | Build the first detector: ML classifier (autoencoder or random forest) on WLS residuals | ML engineer | Working single-node detector, precision/recall on injected faults |
| 2 | In parallel, start explainability + decision-log scaffolding using placeholder detector outputs — don't wait for the detector to be "done" | Explainability/governance owner | SHAP/LIME wrapper, decision-log format |
| 2–3 | Draft escalation logic (confidence thresholds → auto-log vs. human-approval) and a low-fidelity operator review mockup | Governance owner | Escalation policy doc + mockup |
| 3 | Write the collective-learning design doc (what's shared vs. local, and why) — stays design-only for Phase 1 | Whole team (short) | 1–2 page design doc |
| 3 | Assemble Project Proposal (scope, objectives, data/anomaly plan, preliminary design per goal) + business-case paragraph (bonus point) | Writer / PM | Submitted proposal + repo |

### Phase 2 — 15 Oct through 12 Dec (≈2 months)

| Stage | Focus |
|---|---|
| Weeks 1–3 | Harden the detector: tune thresholds, expand fault-injection coverage, add a lightweight forecasting baseline (N-BEATS) if the scope benefits from early-warning drift detection |
| Weeks 3–5 | Build the real operator interface (Streamlit or similar): review, override, approve flagged events |
| Weeks 5–7 | Stress-test: adversarial/out-of-distribution scenarios, measure response latency, refine escalation thresholds against over-trust/under-trust |
| Weeks 7–8 | Formalize the collective-learning protocol as a document (and, if time allows, a toy multi-node simulation) |
| Final 2 weeks | Full report, demo video, presentation rehearsal (5 min talk + 3 min demo) |

---

## 3. Architecture Sketch (recap)

```
Data sources (meters, sensors, IoT)
        ↓
Physics baseline: WLS state estimator
        ↓
Residual computation (measured vs. physics-consistent estimate)
        ↓
ML detector on residuals (autoencoder / random forest)
        ↓
Correlation check (single sensor vs. multi-sensor deviation)
        → distinguishes sensor fault vs. genuine grid event
        ↓
Explainability layer: SHAP/LIME + plain-language decision log
        ↓
Escalation & governance: confidence-based routing
        ↓                          ↘
Auto-logged (high confidence)     Human operator (low confidence / high severity)
        ↓
Collective learning network (design-only): shared anomaly patterns, no raw data
```

This replaces a pure statistical/ML-only detector with a **physics-plus-ML hybrid** (state estimation residuals), which makes the genuine-event-vs-data-fault distinction more defensible and gives explainability a natural anchor ("this reading deviates from the physics-consistent estimate by X").

---

## 4. Research Papers & Resources

Grouped by the part of the system they inform. Priority reflects what's realistic to actually implement in a 3-week Phase 1 vs. what's a Phase 2 stretch or design-reference only.

### 4.1 Detection — physics + ML hybrid (core, Phase 1 priority)

| Reference | Why it matters | Priority |
|---|---|---|
| Schweppe & Wildes, "Power System Static-State Estimation" (1970) — foundational WLS state estimation | The classical physics baseline for your detection pipeline; well-documented, standard in every power-systems textbook | **High** — implement first |
| Liu, Ning & Reiter, "False Data Injection Attacks Against State Estimation in Electric Power Grids" (CCS 2009) | The seminal paper on why state estimators can be fooled by coordinated falsified readings — directly informs your bias/falsification detection design and what adversarial scenarios to test | **High** — read before designing fault injection |
| Liu, Ting & Zhou, "Isolation Forest" (ICDM 2008) | Simple, fast, interpretable-ish point-anomaly detector; good first-pass baseline on residuals or raw readings | **High** — easy to implement, scikit-learn built in |
| Schölkopf et al., "Estimating the Support of a High-Dimensional Distribution" (One-Class SVM, 2001) | Alternative anomaly baseline; useful comparison point for the evaluation section | Medium |
| Autoencoder-based anomaly detection (general technique, many surveys e.g. Chalapathy & Chawla, "Deep Learning for Anomaly Detection: A Survey," 2019) | Reconstruction-error detectors are strong on multivariate drift; use on WLS residuals rather than raw sensor streams for better interpretability | **High** |
| Deng & Hooi, "Graph Deviation Network" (AAAI 2021) | Learns a sensor-relationship graph and flags deviations — a good match for your "correlation check" step (comparing a flagged sensor against its neighbors); more relevant to Phase 2 if time allows | Medium — Phase 2 stretch |

### 4.2 Forecasting baselines (optional, useful for early-warning drift)

| Reference | Why it matters | Priority |
|---|---|---|
| Oreshkin et al., "N-BEATS" (NeurIPS 2020) | Fast, interpretable, strong per-series forecaster — good early-warning signal for drift before it becomes a flagged anomaly; code available (Element AI) | Medium |
| Wu et al., "Graph WaveNet" (IJCAI 2019) | Learns spatio-temporal dependencies across a sensor graph; needs real grid topology + substantial data, so only worth it if your scope has rich multi-sensor time series | Low for Phase 1 — Phase 2 stretch only |
| Li et al., "Diffusion Convolutional RNN / DCRNN" (ICLR 2018) | Similar tradeoffs to Graph WaveNet; fixed (not adaptive) graph, so needs known electrical topology | Low for Phase 1 |
| Lim et al., "Temporal Fusion Transformer" (ICLR 2021) | Handles exogenous covariates (weather, time-of-day) well; heavier to tune, best if load/PV forecasting becomes a differentiator later | Low for Phase 1 |
| Raissi, Perdikaris & Karniadakis, "Physics-Informed Neural Networks" (Journal of Computational Physics, 2019) | Embeds power-flow equations directly into the network; more robust to noisy/sparse data but slower and harder to set up — the natural Phase 2 upgrade to the WLS baseline | Low for Phase 1 — name-check it in the proposal as future work |

### 4.3 Explainability (core, graded directly)

| Reference | Why it matters | Priority |
|---|---|---|
| Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions" (SHAP, NeurIPS 2017) | Standard, well-supported explainability method; works on the residual-based classifier | **High** |
| Ribeiro, Singh & Guestrin, "Why Should I Trust You?" (LIME, KDD 2016) | Lighter-weight alternative/complement to SHAP, good for quick plain-language explanations | **High** |
| Molnar, *Interpretable Machine Learning* (open book, ongoing) | Practical reference for turning model outputs into human-readable verdicts and for choosing interpretable-by-design models over black boxes | **High** — good onboarding read for the whole team |

### 4.4 Escalation, governance & human-AI trust (core, graded directly)

| Reference | Why it matters | Priority |
|---|---|---|
| Amershi et al., "Guidelines for Human-AI Interaction" (CHI 2019) | Widely cited design guidelines for exactly this kind of human-in-the-loop review interface — directly useful for the operator dashboard design | **High** |
| General literature on confidence-based routing / selective prediction (e.g. Geifman & El-Yaniv, "Selective Classification for Deep Neural Networks," NeurIPS 2017) | Formal grounding for "when should the model defer instead of act" — useful for justifying your threshold design in the report | Medium |

### 4.5 Collective / federated learning (design-only for Phase 1)

| Reference | Why it matters | Priority |
|---|---|---|
| McMahan et al., "Communication-Efficient Learning of Deep Networks from Decentralized Data" (Federated Averaging, AISTATS 2017) | The standard reference for how nodes could share model updates instead of raw data — cite this to ground the "Noosphere" sharing design | Medium — needed for the design doc, not for code |
| Dwork, "Differential Privacy" (ICALP 2006, and follow-on survey work) | Gives you vocabulary and a defensible answer to "what is shared, what stays local, and why" — the privacy question the brief explicitly asks | Medium — cite in the design doc |

---

## 5. Tools & Datasets

**Simulators / grid models**
- MATPOWER, Pandapower (transmission power-flow, Python-friendly)
- OpenDSS / GridLAB-D (distribution-level, if the scope includes PV/smart meters)
- IEEE test cases (14-bus, 57-bus) as a fallback if STEG data access doesn't come through

**ML / data stack**
- scikit-learn, PyOD (anomaly detection)
- SHAP, LIME libraries
- PyTorch or PyTorch Forecasting if N-BEATS/TFT are used

**Interface**
- Streamlit or a lightweight web app for the operator review/override interface

**No special hardware required** — this runs entirely on laptop-class compute against simulated or public/STEG data.

---

## 6. Key Dates

| Date | Milestone |
|---|---|
| 17/09/2026 | Infosession (already occurred — confirm what was shared re: STEG data access) |
| 15/10/2026 | Phase 1 submission: Project Proposal + GitHub/Kaggle repo |
| 12/12/2026 | Phase 2 final submission: Report, code, trained models, demo video, presentation |

---

*Compiled from the official TSYP14 challenge brief, the internal ML/Physics survey, the PM's presentation notes, and general power-systems/ML literature.*
