# Goals 1–4 vs. the EnergyMind dataset, node N1 only: compatibility check and fixes

**Scope of this check:** the Phase 1 prototype runs on **node N1 only**. Every number below is computed on N1's rows. N2 and N3 are ignored, except where Goal 4 needs them as "future nodes".

| Goal | Report |
|---|---|
| 1 | `mizan-anomaly-detection/main.pdf` (anomaly & bias detection) |
| 2 | `Confidence Scores and Explainability.pdf` |
| 3 | `human_ai_escalation_governance_report.pdf` |
| 4 | `Shared Learning Across the Noosphere.pdf` |

> **Dataset changes needed: none.** Every problem is fixed in the report text, a rule, a feature or the evaluation protocol. The two things the data lacks (asset criticality for Goal 3, a model-wide bias for Goal 4's C2) are handled by a separate overlay file (`configs/assets.yaml`) or by an injection done in the experiment code at run time.

---

## N1 at a glance

| | N1 |
|---|---|
| Profile | Coastal suburb, one transformer |
| Rows | 525,600 (30 meters × 17,520 half-hours, 2025) |
| Feeders | **N1-F1, N1-F2, N1-F3, 10 meters each** |
| Customer classes | res_medium 13 · res_large 7 · small_commercial 6 · res_small 4 |
| Rooftop PV | **only 3 meters** (N1-M002, N1-M005 on F1; N1-M019 on F2) |
| Meter models | NB-IoT 13 · GPRS 12 · PLC 5 |
| Events | **98** |
| Row labels | normal 93.84% · falsification 2.70% · sensor_fault 2.43% · equipment_failure 0.63% · grid_event 0.30% · comm_loss 0.08% · data_corruption 0.02% |
| Clean feeder balance gap | median 4.4%, p95 **12.4%** (wider than the dataset-wide 9.5%) |

**Events by 4-class diagnosis and time split (train Jan–Aug · valid Sep–Oct · test Nov–Dec):**

| Class | Subtypes in N1 (events) | Total | train / valid / test |
|---|---|---:|---|
| GENUINE_EVENT | outage 7, load_shedding 7, voltage_sag 9, voltage_swell 4, demand_surge 6, cable_fault 2, transformer_degradation 1, transformer_trip 1 | 37 | 23 / 8 / 6 |
| METER_FAULT | bias_step 1, gain_drift 2, clock_shift 1, voltage_offset_drift 1, stuck_value 3, negative_value 8, saturation 6, spike_gain 8, unit_error_x1000 3 | 33 | 23 / 4 / 6 |
| SUSPICIOUS_DATA | **one event each** of the 8 falsification subtypes | 8 | 6 / 2 / **0** |
| NO_DATA | comm_dropout_burst | 20 | 13 / 4 / 3 |

**The time split cannot work in N1:**
- The test period (Nov–Dec) has **zero falsification and zero sensor-bias events**.
- Valid (Sep–Oct) has only `fdi_inflate` and `coordinated_fdi`.

**Rare events in N1, by date and feeder** (one event each unless noted):

| Start | Subtype | Feeder | Meters |
|---|---|---|---:|
| 31 Jan | cable_fault | F1 | 4 |
| 4 Feb | partial_reduction_bypass | F2 | 1 |
| 9 Feb | selective_bypass | F2 | 1 |
| 12 Feb | stuck_value | F1 | 1 |
| 23 Feb | clock_shift | F1 | 1 |
| 19–21 Mar | transformer_degradation → trip | all | 30 |
| 10 Apr | voltage_offset_drift | F1 | 1 |
| 19 Apr, 18 May | gain_drift (×2) | F2 | 1 |
| 25 Apr | fdi_evasion | F2 | 1 |
| 2 May | fdi_scale | F3 | 1 |
| 11 May | meter_zeroing | F1 | 1 |
| 5 Jun | bias_step | F1 | 1 |
| 9 Aug | fdi_replay | F2 | 1 |
| 6 Sep | cable_fault | F2 | 6 |
| 12 Sep | fdi_inflate | F3 | 1 |
| **14 Oct** | **coordinated_fdi** | **F1** | **3** |

---

## Goal 1: Anomaly & Bias Detection (Mizan), on N1

### What fits ✅

- **The report's setup is close to N1:** "one transformer, about 50 smart meters, rooftop PV". N1 has one transformer, 30 meters and 3 PV homes.
- **All detector inputs exist:** feeder balance, V·I·PF, 30-min profiles, weather and calendar.
- **Clean training data:** fit on `gt_label == "normal"` rows (93.8% of N1).
- **The physics rule catches data-only FDI:** E/(V·I·PF·t) is 0.65 for `fdi_scale`, 0.69 for `fdi_evasion`, 0.64 for `coordinated_fdi`, and 1.68 for `fdi_inflate`.
- **The README's IF baseline (ROC-AUC 0.757) was computed on N1**, so it is the right reference.

### How each bias shows up in N1 (medians)

| Subtype | E / (V·I·PF·t) | V − feeder V | Feeder gap % | Visible to |
|---|---:|---:|---:|---|
| *normal* | 1.00 | −0.9 V | 4.4 (p95 12.4) | — |
| `bias_step` | **1.00** | +0.1 | 1.5 | the meter's own history only |
| `gain_drift` | **1.00** | −1.4 | 4.3 | the meter's own history only |
| `partial_reduction_bypass` | **1.00** | −2.2 | **10.9** (inside the normal range) | the meter's own history only |
| `selective_bypass` | **1.00** | −1.4 | 19.9 | balance gap, hour-of-day profile |
| `meter_zeroing` | — | −0.3 | 12.6 (borderline) | zero-run rule |
| `fdi_scale` / `fdi_evasion` / `coordinated_fdi` | 0.65 / 0.69 / 0.64 | ≈ −1.5 | 6.7 / 10.3 / 18.5 | physics rule |
| `fdi_inflate` | 1.68 | −1.1 | **−5.4** | physics rule; the gap goes negative |
| `fdi_replay` | 1.03 | −1.7 | 4.2 | week-lag similarity only |
| `voltage_offset_drift` | 0.97 | **+6.3** | 3.4 | V vs. feeder V |
| `clock_shift` | 1.00 | −0.4 | 2.5 | lag correlation |

### Problems and fixes

**1.1 The physics rule can't see sensor bias or physical theft.** *(Revised after running the detectors on N1; see the Goal 1 report §5.1.)*
- **Problem:** `bias_step`, `gain_drift` and both bypasses keep the ratio at 1.00. Table 1 pointed "slow drift / constant bias" at physics.
- **What the N1 experiment showed:** my first recommendation, "per-meter CUSUM against the neighbours as the main bias detector", does **not** work on this data. A household's daily share of its feeder varies far more than a 7–14% bias, so that CUSUM catches almost nothing at a 1% false-positive rate.
- **Fix applied in the report:**
  - Table 1 now says what each fault looks like in the data.
  - Sensor bias and bypass are honestly listed as **the hard cases**: flagged on ≤ 18% of their days. This matches the README's difficulty ranking.
  - The physics rule is described as the detector for data-only falsification.

**1.2 The feeder balance.** *(Revised after the experiment.)*
- **Problem:** judged on half-hour rows, the gap looks noisy (p95 12.4%). At **daily** resolution it is much tighter (about 0.6 points of day-to-day noise), but it is **seasonal**: F1's gap falls from about 5% in winter to 1–3% in spring and summer because of PV export. A fixed reference therefore raises false alarms all summer.
- **What works:** a CUSUM on the daily gap, with a seasonal reference frozen during alarms and h calibrated on clean feeder-days (in alarm 5.2% of the time). It alarms **8–16 days** after the start of both bypasses, the bias and both drifts. It names the **feeder**, not the meter, and attributing the alarm to the right meter fails.
- **Fix applied in the report:**
  - The balance is described as feeder-level evidence.
  - Fig. 1 now says the gap moves in either direction.
  - Phase 2 plan: model the expected gap from load, PV and temperature, then run CUSUM on the residual.

**1.3 Voltage bias is easy but missing from the report.**
- **Problem:** in `voltage_offset_drift` the meter reads **+6.3 V above** its feeder head. That is impossible, because voltage only drops along the line.
- **Fix in the report:**
  - **Fig. 3, layer 1:** add a box, "Meter V vs. feeder-head V (24-h median)".
  - **Table 1:** add a row, *Voltage sensor offset* → *meter V persistently above feeder V* → *Feeder-head comparison + CUSUM*.
  - The repo already implements it as `rules.voltage_above_feeder`.

**1.4 Solar homes break the physics rule, but only 3 meters in N1.**
- **Problem:** on clean rows, a ±5% check fires on 0.76% of non-PV rows and **39%** of PV-home rows. With the export gate, it fires on **0.06%** of all clean N1 rows.
- **Fix in the report (§3 / layer 1):** *"Physics consistency is skipped while the meter exports (`pv_export_kwh > 0`); in N1 this affects 3 of 30 meters."*

**1.5 Setup and units.**
- **Problem and fix in the report:**

  | Where | Current text | Replace with |
  |---|---|---|
  | §1 | "one transformer, about 50 smart meters, rooftop PV" | "one transformer (node N1), 30 smart meters on 3 feeders of 10, 3 with rooftop PV" |
  | Fig. 2 caption | "15-min samples" | "30-min samples" (set the `gen.py` step to 0.5 h) |
  | §5.1 | "12-hour windows… 48 samples at 15 min" | "24-hour windows (48 samples at 30 min)" |
  | Table 1 / Table 4 | Drift "+2–6%" | "±2–6% (in N1 both `gain_drift` events under-read)" |
  | Table 4 caption | Replay "another day" | "the same half-hour one week earlier" |
  | §4.3 | "share of zero increments" | "share of repeated values, share of zero readings" |
  | Table 1 | "Spike, dropout" | "Spike, impossible value". Then add: *"Missing readings are not scored; they are passed on as 'no data'."* |
  | Table 4 | "Noise" column | Remove it, or mark it *"robustness test, not in the dataset"* |

**1.6 Fault types missing from Table 1.**
- **Problem:** N1 has 25 corruption events, plus `clock_shift`, `voltage_offset_drift` and hard negatives (Ramadan, summer vacations, heat waves, post-outage pickup). Table 1 lists none of them.
- **Fix in the report:**
  - **Table 1:** add *Sign or unit error* → *E < 0, E = 99.999, ratio to profile > 100* → *Range rule*.
  - **Table 1:** add *Clock shift* → *all channels delayed 1–3 h* → *Lag cross-correlation with the feeder-head current*.
  - **§4.1:** *"The profile is conditioned on hour, weekday, holiday, Ramadan and temperature."*
  - **§5:** *"Genuine events are expected to trigger layers 1–3; separating them from data problems is Goal 2's job."*

**1.7 The experiment.**
- **Problem:**
  - Table 4 uses `gen.py` injections far from the dataset's (spike ±18–42% vs. ×8–40; bias ×1.015–1.05 vs. ×0.86–1.14; theft −12% vs. ×0.4–0.8).
  - In N1 every falsification subtype has **exactly one event**, so per-subtype recall would be 0% or 100%.
- **Fix in the report:** add **§5.2, "Results on N1"**:
  - **Training:** fit on N1 normal rows. **Inputs:** all columns except `gt_*`, `annual_kwh_target` and `fault_weight`.
  - **Split:** grouped K-fold by `gt_event_id` (`energymind.data.event_folds`). The time split is impossible, see the table above.
  - **For the 33 METER_FAULT and 37 GENUINE_EVENT events:** per-class recall and FPR.
  - **For the 8 single falsification events and the 5 sensor-bias events:** a per-event table showing detected yes/no, which detector fired first, and the delay from event start. No percentages.
  - **Comparison:** the README's N1 baselines (IF AUC 0.757; physics rule recall 0.31 at 0.31% FPR).

**1.8 Interface with Goal 2.**
- **Fix in the report (end of §5):** *"Per flagged reading Mizan passes to Goal 2: the fused score, each detector's score, the neighbourhood support s (share of the 10 feeder meters flagged at t), and the per-channel autoencoder error."*

---

## Goal 2: Confidence Scores and Explainability, on N1

### What fits ✅

- **The physics rule R3 is meaningful.** Data-only FDI breaks the ratio (0.64–0.69 / 1.68). Clean meters already have about 1% error, so "add measurement noise" is not needed.
- **R2:** `stuck_value` freezes all channels.
- **R4:** grid events in N1 hit a **median of 10 meters = the whole feeder**. Transformer events hit all 30. `cable_fault` hits 4–6, the meters downstream of the fault.
- **The verdict card "0 of 9 other houses on feeder F2" matches N1 exactly:** 10 meters per feeder.
- **R3 before R4 is the right order:** `coordinated_fdi` (3 of 10 meters on F1, ratio 0.64) is caught by R3 before it could pass as collective.

### Problems and fixes

**2.1 Outages are zeros, not missing values, so R2 calls them "stuck sensor".**
- **Problem:**

  | N1 subtype | Rows | Energy blank | V = 0 |
  |---|---:|---:|---:|
  | outage | 370 | 0.3% | 99.7% |
  | load_shedding | 250 | 0% | 100% |
  | cable_fault | 34 | 0% | 100% |
  | transformer_trip | 30 | 0% | 100% |
  | comm_dropout_burst | 429 | **100%** | 0% |

  R2 (frozen) fires before R4, so all **684 supply-loss rows** in N1 become METER_FAULT. Separately, 3.75% of clean N1 rows have E = 0.
- **Fix in the report:**
  - **Fig. 1 / Table 3:** insert **R0 before R1**: *"V = 0 or `meter_event_code = power_fail` → GENUINE_EVENT: outage if s ≥ τs, local supply loss (cable fault) if 2–6 meters, notify if 1."* `power_fail` appears on 205 event rows in N1.
  - **R2:** require *V > 0 and not exporting*.
  - **Table 2:** add the evidence term **v₀ = 1[V = 0]**.
  - Implemented in `explain/cascade.py`.

**2.2 R3 and solar homes.**
- **Problem:** the naive R3 fires on 39% of clean rows from N1's 3 PV homes.
- **Fix in the report:**
  - **Table 2:** skip ρ when `pv_export_kwh > 0`. With that gate, R3 fires on 0.06% of clean N1 rows.
  - **Units:** P = `energy_kwh` / 0.5 h, so E = V·I·PF·Δt / 1000.
  - **§1.10:** replace the "derived channels" risk with *"Data-only falsification corrupts energy alone, while sensor bias and physical bypass scale energy and current together; R3 targets the former."*

**2.3 Falsification has no verdict class.**
- **Problem:**
  - N1 has 8 falsification events (14,175 rows, 2.7%).
  - `selective_bypass` (F2) and `meter_zeroing` (F1) are isolated, physically consistent and come in hour-long bursts, so they land in **R6, "appliance switching on"**.
  - Goal 3 needs **SUSPICIOUS_DATA**.
- **Fix in the report:**
  - **§1.1 scope:** *"…equipment and measurement problems, suspected data manipulation, and genuine electrical events."*
  - **Add R5b before R6:** *"Isolated, consistent, energy ≥ 30% below the house's own profile for ≥ τπ steps, and feeder gap above the N1 clean p97 → SUSPICIOUS_DATA (possible bypass)."*
  - **Split R3 by direction:** *energy below V·I* → SUSPICIOUS_DATA (data-only FDI); *impossible value* → METER_FAULT (corruption).
  - **Tamper codes are weak evidence only:** N1 falsification rows carry 3 `magnetic_tamper` + 1 `cover_open`, against 55 false codes on clean rows.

**2.4 The data split.**
- **Problem:** §1.6 fits τ and β on Sep–Oct and tests on Nov–Dec. In N1, Sep–Oct holds 2 falsification events and 0 sensor-bias events; Nov–Dec holds none of either.
- **Fix in the report (§1.6, "Data used for fitting"):** replace it with *"Baselines use N1 normal rows Jan–Aug. τ and the Platt coefficients are fitted by grouped 5-fold cross-validation over N1's 98 events (grouped by `gt_event_id`); all metrics are out-of-fold, per event, with Wilson 95% intervals."*

**2.5 Evaluation inputs that don't exist in the dataset.**
- **Fix in the report:**
  - **§1.9:** add the subtype → channel table:
    - energy: `fdi_*`, corruption;
    - voltage: `voltage_offset_drift`;
    - all channels: `bias_step`, `gain_drift`, `stuck_value`, `clock_shift`, the bypasses, `meter_zeroing` (score only the scope and the verdict for these).
  - **"Subtle severity set":** define it as *the first 7 days of the 2 `gain_drift` events and the `bias_step` event, plus `fdi_evasion`*, or delete it.

**2.6 Goal 1 inputs and R5.**
- **Fix in the report:**
  - **§1.4:** take Goal 1's fused score, per-detector scores, s, and per-channel errors (see 1.8).
  - **k\* in R3:** use the per-channel error instead of the largest |z|.
  - **R5:** use *"CUSUM alarm on the meter-to-neighbour ratio, or slope over 14 days"*. The N1 `gain_drift` events last about 9 weeks.
  - **R1:** isolated comm loss → **NO_DATA**, not METER_FAULT.

---

## Goal 3: Human–AI Escalation and Governance, on N1

### What fits ✅

- **The 4 classes map one to one** (see the class table above): GENUINE_EVENT 37 events, METER_FAULT 33, SUSPICIOUS_DATA 8, plus 20 comm-loss events for R0.
- **Event-level evaluation:** 98 events via `gt_event_id`.
- **The reference policy for N1** (`gt_expected_response`, in rows):

  | Label | auto_log | auto_correct | notify_operator | human_decision |
  |---|---:|---:|---:|---:|
  | grid_event | 1,100 | | 500 | |
  | equipment_failure | 50 | | | 3,244 |
  | sensor_fault | | 151 | 3,711 | 8,922 |
  | data_corruption | | 112 | | |
  | falsification | | | | 14,175 |
  | comm_loss | | 78 | 351 | |

### Problems and fixes

**3.1 No asset criticality in the data.**
- **Problem:** N1 has residential meters and 6 `small_commercial` meters only. There is no hospital or industrial asset, and the feeder-head meter is never faulty.
- **Fix in the report (§3.3.2 and §3.10):**
  - Criticality comes from **`configs/assets.yaml`** (already in the repo): `res_*` → LOW, `small_commercial` → MEDIUM (F1 2, F2 3, F3 1), feeder heads → HIGH, **N1-F3 → CRITICAL ("health centre, assumed")**.
  - **Severity from scope:** 1 meter < 6 h → LOW; ≥ 6 h or 2–6 meters → MEDIUM; whole feeder (10 meters) → HIGH; whole node (30 meters, transformer) → CRITICAL.
  - **Scenarios built on N1 events:**
    - S2 = a `voltage_sag` on N1-F3;
    - S4 = a `demand_surge` on a `small_commercial` meter;
    - S6 = the 4 Feb `partial_reduction_bypass` on F2;
    - S3 = re-based on the 19 Apr `gain_drift` (F2), because the feeder-head meter is never faulty.

**3.2 The routing contradicts the reference policy.**
- **Problem:**
  - R6 sends METER_FAULT to G1, but N1's `gain_drift`, `bias_step` (8,922 rows) are `human_decision` and `clock_shift` / `voltage_offset_drift` (3,711 rows) are `notify_operator`.
  - Load shedding, sags and surges are `auto_log` in the data, but G2a in the report.
- **Fix in the report:**
  - **Table R6:** add *"METER_FAULT lasting ≥ 24 h or affecting billing → ≥ G2b"* and *"scheduled or self-clearing GENUINE_EVENT → G0"*.
  - **§3.9:** add *agreement with the reference policy* (`auto_log` → G0, `auto_correct` → G1, `notify_operator` → G2a, `human_decision` → ≥ G2b). Count below reference as a missed escalation, above as a false escalation. Implemented in `govern/policy.py`.

**3.3 Too few events for per-class calibration.**
- **Problem:** "n = 412" exceeds all **98 N1 events**. SUSPICIOUS_DATA has 8 events, one per subtype.
- **Fix in the report:**
  - **§3.4.1:** *"Calibration is validated for a class only with ≥ 30 out-of-fold events. In N1 this holds for GENUINE_EVENT (37) and METER_FAULT (33), not for SUSPICIOUS_DATA (8), which is therefore capped at MEDIUM and always reviewed."*
  - **§3.6:** show the real count per class.

**3.4 The interface with Goal 2.**
- **Fix in the report:** the diagnosis input is the 4-class probabilities from Goal 2's multinomial Platt calibration (see 2.3).

**3.5 OOD.**
- **Fix in the report (§3.9):** *"OOD is exercised on N1 hard-negative periods (Ramadan, August vacations) and, in Phase 2, by running the N1 models on N2/N3."*

---

## Goal 4: Shared Learning, with N1 only

**Main issue:** with one node there is no Noosphere to share across. The brief allows multi-node sharing to stay a documented design in Phase 1. On N1 alone there are two honest options:

| Option | What it means | Fix in the report |
|---|---|---|
| **A. Design only (minimum)** | Keep the protocol; run nothing multi-node | §1.2: *"The Phase 1 prototype runs on N1; N2 and N3 are reserved as the other nodes for Phase 2."* Delete the 3-node experiment claims |
| **B. Feeders as sites (recommended)** | Treat N1-F1, F2, F3 as three sites. Each has its own head meter, balance and 10 meters | Add a §1.2 paragraph: *"In Phase 1 the protocol is exercised between the three N1 feeders; they share a transformer and weather, so heterogeneity is lower than between real nodes."* |

Option B fits the data well, because the attack families reach the feeders at different times:

| Family | Seen first on | Reaches the other feeder later |
|---|---|---|
| Physical bypass | **F2** (4 and 9 Feb) | **F1** `meter_zeroing`, 11 May |
| Data-only FDI | **F2** `fdi_evasion` (25 Apr), **F3** `fdi_scale` (2 May), F2 `fdi_replay` (Aug), F3 `fdi_inflate` (Sep) | **F1** `coordinated_fdi`, **14 Oct** (F1's first FDI) |
| Sensor drift | **F2** `gain_drift` (Apr, May) | **F1** `bias_step` (5 Jun) |

### Problems and fixes

**4.1 The dataset facts in §1.1–1.2 describe all 3 nodes.**
- **Fix in the report:**
  - **§1.2 / Table 1:** state the N1 scope (525,600 rows, 30 meters, 3 feeders).
  - **§1.1:** replace "2–4 times per node" with *"in N1 each falsification subtype occurs exactly once in the year"*.

**4.2 There is no experiment.**
- **Fix in the report:** add **§1.6, "Feeder-site experiment (N1)"**. Train each feeder's screening model on its own data and score the next attack on another feeder in three setups:
  - local only;
  - local + C1 family centroids from the other feeders;
  - local + C3 (FedAvg vs. coordinate-wise median).

  Main case: does F1 detect the **14 Oct `coordinated_fdi`** earlier when it has received the data-only-FDI signature learned on F2/F3 between April and September? Report the detection delay, per event.

**4.3 The C4 urgent alert.**
- **Fix in the report:** use the same timeline. *"F3's operator confirms `fdi_inflate` (12 Sep) → signed fingerprint → F1 holds it as a prior before 14 Oct."* Measure F1's delay with and without the prior.

**4.4 The canary check.**
- **Problem:** "per-subtype recall must not decrease" rests on 1 event per subtype, and 0–4 falsification events per feeder.
- **Fix in the report (§1.5.7):**
  - Use recall **per family** on the union of the other feeders' events, and gate only on families with ≥ 3 events (data-only FDI has 5, corruption 25).
  - Extend the grid check to include `equipment_failure`.

**4.5 C2 calibration insights.**
- **Problem:**
  - Meters per model and feeder: GPRS 5 / 3 / 4, NB-IoT 3 / 5 / 5, **PLC 2 / 2 / 1**. With k ≥ 3, PLC is suppressed on every feeder.
  - There is no model-wide bias in the data. On clean rows the summary is about 0 for every model (checked: −0.0006, −0.0002, +0.0011).
  - The log ratio is −∞ while exporting.
- **Fix in the report (§1.5.3):**
  - *"Computed on clean rows with `pv_export_kwh = 0` and E > 0; PLC suppressed (fewer than 3 meters per site)."*
  - *"On N1 C2 is a **negative control** (≈ 0 for all models). A positive test injects +3% gain on all NB-IoT meters in the experiment code (dataset unchanged)."*

**4.6 Privacy numbers.**
- **Fix in the report:** with K = 3 sites, Table 3 stays valid. Add one sentence: *"Feeder sites inside one node share an operator, so the privacy threat between them is lower than between nodes; the ε values are reported for the multi-node design."*

---

## Priority order (N1)

1. **Goal 2, 2.1:** add R0, the supply-loss rule. Without it, all 684 N1 outage rows are called stuck sensors.
2. **Goals 2 and 3, 2.3 and 3.4:** add SUSPICIOUS_DATA with the R5b bypass rule, and pass 4-class probabilities.
3. **All goals, 1.7, 2.4, 3.3 and 4.4:** use grouped CV by event. N1's Nov–Dec has no falsification or bias events, so report rare events one by one.
4. **Goal 1, 1.1–1.3:** make CUSUM the main bias detector, set the balance threshold from N1 (≈ 13–15%), and add the voltage rule (+6.3 V).
5. **Goal 1, 1.5:** fix the setup text (N1: 30 meters, 3 × 10, 30 min, 24-h windows) and add §5.2 with the N1 results.
6. **Goal 3, 3.1 and 3.2:** use the asset overlay (N1-F3 critical) and score the policy against `gt_expected_response`.
7. **Goal 4, option B:** feeders as sites, with the F2/F3 → F1 transfer and the C4 alert before 14 Oct.
