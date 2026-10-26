# Mizan report vs. EnergyMind simulated dataset: compatibility check (anomaly & bias detection)

- **Report:** `mizan-anomaly-detection/main.pdf`, Phase 1 technical note. **Scope: anomaly and bias detection only.** This means pipeline layers 1–4: rules, statistics, the ML ensemble and score fusion, answering *"is this reading unusual or biased?"*
- **Out of scope here:** the event-vs-data reasoner (layer 5), verdict and routing (layer 6), the response policy (`gt_expected_response`) and the handling of communication loss. Those belong to other parts of the project, so they are not judged below.
- **Dataset:** `energymind_full_joined.csv`: 1,051,200 rows, 60 meters on 7 feeders in 3 nodes, 30-min steps, year 2025.
- **Method:** I read the report and the README, then measured on the CSV how each fault type shows up in the readings: reported energy vs. true energy, energy vs. V·I·PF·0.5 h, meter voltage vs. feeder-head voltage, and the feeder balance gap. Medians are taken per `gt_subtype`.

## Verdict

**The detection approach fits the dataset, but the report's bias story does not match how the data's biases behave.**

The detector families are the right ones, every input they need is in the data, and the dataset's labels let you score them. Three problems remain:

1. **Sensor bias in the dataset is physically consistent.** It scales energy *and* current together, so the V–I–P physics rule cannot see it.
2. **The feeder energy balance is too blunt for one biased meter.** Each feeder has 7–10 meters, so one meter that is off by 10% moves the gap by about 1%, which is inside its normal spread.
3. **Units, setup and the experiment's fault sizes differ from the dataset.**

---

## 1. What already matches ✅

| Report element | Dataset support |
|---|---|
| Rules: range, rate, flat-line | Data has impossible values to catch: `saturation` (99.999), `unit_error_x1000` (~1000×), `spike_gain` (×8–40), `negative_value` |
| Robust z on residuals from a time-of-day profile | Possible. Clean 30-min profiles exist per meter, with weather and calendar fields (`temp_c`, `ghi_wm2`, `is_ramadan`, `is_weekend`, `is_public_holiday`) to build the profile |
| CUSUM for drift and persistent shifts | Fits `gain_drift`, `bias_step` and `voltage_offset_drift`, which are long (thousands of rows each) and slow or stepwise |
| Energy balance, feeder vs. Σ meters | Present (`energy_balance_gap_pct`) |
| V–I–P consistency | Present. On clean rows, energy ≈ V·I·PF·0.5 h |
| IF / OCSVM / autoencoder trained on clean windows | Filter `gt_label == "normal"` (93.2% of rows). Inputs are the 50 non-label columns |
| Thresholds at a fixed false-positive rate | Exact labels let you measure FPR and recall per subtype |
| IF as a baseline | README reference: ROC-AUC 0.757 (N1) |

## 2. How each bias actually shows up in the data

Medians per subtype. "E / true" uses the oracle column and is for analysis only. The other three columns are signals a detector can see.

| Subtype (bias-like) | E / true | E / (V·I·PF·t) | V − feeder V | Feeder gap % | Visible to |
|---|---:|---:|---:|---:|---|
| *normal (reference)* | 1.00 | 1.00 | −1.1 V (p5–p95: −7.0…+0.5) | 4.3 | — |
| `bias_step` (×0.86–0.93 / ×1.07–1.14) | 0.93 | **0.99** | −0.3 | 3.2 | own history only |
| `gain_drift` (slow, mostly under) | 0.98 | **1.00** | −0.9 | 4.7 | own history only, very weak |
| `partial_reduction_bypass` | 0.58 | **1.00** | −2.0 | 11.9 | balance gap, own history |
| `selective_bypass` | 0.26 | **1.00** | −1.6 | 18.9 | balance gap, hour-of-day profile |
| `meter_zeroing` | 0.00 | — | −1.0 | 13.1 | zero-run rule, balance gap |
| `fdi_scale` | 0.65 | **0.65** | −1.1 | 7.1 | physics rule |
| `fdi_evasion` | 0.57 | **0.57** | −2.9 | 9.0 | physics rule |
| `coordinated_fdi` (3 meters) | 0.52 | **0.60** | −1.3 | 16.6 | physics rule, balance gap |
| `fdi_inflate` | 1.71 | **1.70** | −0.9 | **−2.0** | physics rule; the gap goes *negative* |
| `voltage_offset_drift` | 1.00 | 0.98 | **+2.9** | 3.1 | meter V *above* feeder V (impossible on a feeder) |
| `stuck_value` | 1.15 | 1.00 | −2.8 | 0.8 | flat-line rule (all channels frozen) |
| `fdi_replay` | 1.00 | 1.00 | −1.9 | 4.8 | week-lag similarity only |
| `clock_shift` (1–3 h delay) | 1.00 | 1.00 | −1.0 | 3.2 | cross-correlation with neighbours or feeder |

**What this means for the report:**

- **The physics rule catches data-only falsification well (`fdi_*`). It is blind to sensor bias and physical theft.** `bias_step`, `gain_drift` and the bypasses all keep E/(V·I·PF·t) ≈ 1.00. The report's Table 1 gives "Slow drift, gain error" and "Constant bias" as targets without saying this.
- **The energy balance does not catch "Constant bias" (Table 1) in this data.** A ×0.9 bias on one meter out of 7–10 shifts the feeder gap by about 1%. The normal gap ranges from 1.8% to 9.5%, and the median gap during `bias_step` (3.2%) is even *below* normal, because some steps go up. The balance only flags **large** reductions: bypass, zeroing, coordinated FDI.
- **CUSUM on each meter's own history is the main bias detector, and the report should say so.** Run it on the ratio of the meter to its own past profile or to its feeder neighbours. The dataset's sensor biases are visible only there.
- **The balance can go negative.** `fdi_inflate` drives it to −2% and corruption drives it to large negative values. Fig. 1 says a data problem makes the gap "grow". It should say the gap can move in either direction.
- **Voltage bias is easy, and the report doesn't mention it.** A meter reading above its feeder head is impossible, because voltage only drops along the line, so `voltage_offset_drift` can be caught with a simple rule against `feeder_voltage_v`.
- **PV homes break the physics rule.** On normal rows, E/(V·I·PF·t) has p5 = 0.0, because exporting homes show current with zero import. Gate the rule on `pv_export_kwh == 0` or use import + export.

## 3. Factual mismatches in the text ❌

| # | Report says | Dataset has | Fix |
|---|---|---|---|
| 1 | "15-min samples" (Fig. 2); "12-hour windows… 48 samples at 15 min" (§5.1) | **30-min** steps | Use 30 min; 48 samples = **24 h** |
| 2 | "one transformer, about 50 smart meters" | 60 meters, 7 feeders (**7–10 meters each**), 3 nodes | Describe the real setup. It sets how weak the balance is per meter |
| 3 | "Noise" anomaly (σ = 0.07) | No added-noise fault | Drop it, or label it as an extra robustness test |
| 4 | Replay = "another day" | Same half-hour **one week earlier** | Detector should compare against the week lag |
| 5 | Window feature "share of zero increments" | Interval energy, not a cumulative register | "share of repeated values" (stuck) and "share of zero readings" (zeroing) |
| 6 | Drift: "+2–6%" (implies upward) | `gain_drift` is mostly **under-reading**, labelled from 1% | Make it two-sided; the dataset case is mostly downward |
| 7 | Table 1 "Dropout" as a point anomaly | Missing rows are blank, not values | Exclude blanks from scoring; that is not detection's job |

## 4. Detection targets not covered in Table 1 ⚠️

- **Data corruption:** `negative_value`, `saturation`, `unit_error_x1000`, and `spike_gain` at ×8–40. A single range or sign rule catches them, but `negative_value` is rated *hard* in the README baseline, so state the sign rule explicitly.
- **`voltage_offset_drift`:** add a "meter V > feeder V" rule (see §2).
- **`clock_shift`:** every channel stays internally consistent and only the timing moves. Only lagged cross-correlation with neighbours or the feeder current will see it.
- **Hard negatives the detectors must not flag**, listed in the README: Ramadan shift, summer vacations (genuinely low use, which looks like a downward bias), heat-wave surges, PV export, and post-outage surges. They belong in the false-positive discussion next to "evening peak".
- **Genuine events (`grid_event`, `equipment_failure`)** *will* trigger the detectors. That is correct at this stage, since separating them is layer 5's job. Say this explicitly, and choose the evaluation target accordingly (§5).

## 5. The experiment (§5.1, Table 4)

The experiment runs on `gen.py` toy data, and its injection sizes are far from the dataset's. The Table 4 recalls therefore don't carry over:

| Type | Report | Dataset |
|---|---|---|
| Spike | ±18–42% | ×8–40 |
| Bias | ×1.015–1.05 | ×0.86–0.93 or ×1.07–1.14, for 3–11 weeks |
| Theft | −12% at the evening peak | ×0.4–0.8, or zeroing for 5–8 h |
| Stuck | 12–23 samples | 3–48 h (6–96 samples) |
| Drift | +2–6% linear | mostly downward, labelled from 1% |

**Recommended: re-run the same five detectors on the dataset.**

- **Split:** train on `normal` rows from Jan–Aug, set thresholds on Sep–Oct, test on Nov–Dec. This is the README split; a random split leaks seasonality.
- **Inputs:** drop all `gt_*` columns plus `annual_kwh_target` and `fault_weight`.
- **Two targets, matching the scope:**
  - *Anomaly detection:* `gt_label != "normal"`. Genuine events count as hits.
  - *Bias / untrustworthy-data detection:* `gt_data_trustworthy == 0`.
- **Reporting:** give recall per `gt_subtype` with the FPR, and compare with the README baselines (IF ROC-AUC 0.757; physics rule recall 0.31 at 0.31% FPR).
- **Caveat:** most bias and falsification subtypes have only **2–4 events in the year**. Check that each one appears in the test split, or report per-event recall.

## 6. Priority fix list

1. Fix the units and setup: **30 min**, **24-h windows**, **60 meters / 7 feeders**.
2. Rewrite the bias rows of Table 1:
   - *Sensor bias and drift* → per-meter CUSUM against the meter's own profile or its neighbours. Physics and balance are blind to it.
   - *Data-only falsification* → V–I–P rule.
   - *Large physical reduction* → balance gap.
   - *Voltage bias* → meter V vs. feeder V.
3. Add the corruption and clock-shift rows. Drop "noise". Make drift two-sided.
4. Add a short note to Fig. 1 that the gap can go negative, and gate the physics rule for PV homes.
5. Re-run §5.1 on the dataset with the two targets above, or put the dataset results next to the toy run.
