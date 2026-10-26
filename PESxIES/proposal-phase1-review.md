# EnergyMind Tunisia: Phase 1 Submission Review

*Reviewed 14 Oct 2026 (deadline 15 Oct). Sources: `energymind-tunisia/docs/proposal/proposal.pdf` (46 pp.) and the `energymind-tunisia/` repo.*

## Verdict

The technical content is strong. It covers every item the brief requires: scope, objectives, a data and anomaly-simulation plan, and a preliminary design for each of Goals 1–4. It also goes beyond the brief in two places. Goal 1 is measured on real data from your own simulator, and the numbers reproduce. The limitations are stated honestly throughout.

What could lose points is **packaging, not substance**. The repo isn't published. Team names are missing. Both bonus items are absent. A few claims in the PDF aren't backed by the repo. All of this can be fixed in a day.

### What I verified

| Check | Result |
|---|---|
| `pytest` | ✅ 8/8 pass (clean venv: pandas 3.0.6, scikit-learn 1.9.1) |
| `docs/goal1_detection/n1_experiment.py` | ✅ Runs in about 20 s. Reproduces Table 7 and Table 8 exactly: 2.3% FP, 30/36, 23/30, 6/8. Committed outputs are unchanged. |
| N1 event counts (§3.4) | ✅ They match `scripts/check_dataset.py`: 33 grid + 4 equipment, 25 corruption + 8 sensor, 8 falsification, 20 comm-loss |
| `docs/decision_log_schema.json` | ✅ Valid JSON |
| Eq. 18 / Table 26 (RDP ε) | ✅ The closed form is the exact minimiser, and the table values check out (e.g. σ=1, R=10 → 20.2; σ=8, R=52 → 4.7) |

---

## 🔴 Blockers: fix before submitting

1. **The repo is not on GitHub.** `energymind-tunisia/` is *untracked* inside your whole-workspace repo (`housseinelyatim-exe/TSYP`, which also holds other challenges). Phase 1 requires a GitHub repo and/or Kaggle notebook. Create a **standalone public repo** for `energymind-tunisia/` and push it. The 33 MB `.csv.gz` is under GitHub's 100 MB limit. Then put the repo URL on the proposal title page and in the README.

2. **No team identity anywhere.** In `proposal.tex`, `\author{}` is empty. The README team table is still `| … | … | … |`. Your own plan says listing membership (PES / IES / YP / dual) is worth **up to +4 bonus**. Add the team name, Student Branch, members and their society memberships to the title page and the README.

3. **The business-scope bonus (+1) is missing.** No section covers budget, deployment, continuous training or integration cost. Add about ½ page, e.g. "11 Deployment and Business Scope". Cover:
   - the cost per node (an edge box or a STEG head-end VM)
   - integration with the AMI head-end and SCADA
   - a retraining cadence (monthly recalibration plus the canary from Goal 4)
   - who pays: avoided non-technical losses vs. operator time

4. **Claim with no code: "property-based tests on 400 random events"** (§7.4, and twice in the Goal 3 report). `src/energymind/govern/policy.py` contains only `compare_to_reference`. There is no routing engine and no property test. Either remove the sentence, or change it to *"will be checked (Phase 2) by property-based tests…"*. O5 promises that "every number in this proposal comes from code in the repository", so a reviewer who opens the repo will notice.

5. **Generator code is missing, yet the proposal says the data is reproducible.** The data card says the data was "generated with a fixed random seed (2025), so the dataset is reproducible". However, no generator or injection script is in the repo. Your task plan called for `src/data/inject.py`. The proposal also has two phrases that suggest a third party made the data: "the difficulty ranking published with the dataset" and "suggested response given by the dataset authors". Decide which is true and say it plainly:
   - **If you built the data:** commit the generator and injection code. The brief marks how anomalies were generated as a graded item.
   - **If someone else built it:** credit them and drop the reproducibility claim.

---

## 🟠 High: consistency issues a careful judge will spot

6. **The detection stack finds fewer meter faults than One-Class SVM alone** (Table 7: stack 23/30 vs. OCSVM 25/30), and it has a higher FP rate (2.3% vs. 1.3%). The cause is in the code. The stack uses each learned detector at a 0.25% threshold (`FPR_ENS`), while the single-detector rows use 1%. Add one sentence under Table 7, e.g.:
   > "Inside the stack each learned detector runs at a stricter 0.25% threshold so that their union stays near 2%; that is why the stack catches two fewer meter-fault events than the One-Class SVM run alone at 1%."

7. **"Thresholds give a 1% false-positive rate on held-out clean days"** (§5.5.1). The table shows 0.9–2.1% (CUSUM 2.1%, OCSVM 1.3%). Reword: *"thresholds target 1% on a calibration split of the training folds; realised out-of-fold rates are 0.9–2.1%."*

8. **The event counts differ between sections without explanation.** §3.4 says 37 genuine / 33 meter-fault / 98 events. Table 7 says 36 / 30, and §5.5.1 says 74 events. Add one line explaining the exclusions: comm-loss events, the first week used for profile history, and mostly-missing days.

9. **Two different rule sets both use the IDs R0–R6.** Goal 2's cascade uses R0–R6 (R0 = supply lost). Goal 3's routing uses R0–R9 (R0 = input validity). Goal 3 then says "NO_DATA is handled by rule R0", but in Goal 2, NO_DATA is R1. Rename one set, e.g. cascade **D0–D6** and routing **P0–P9**, and apply it in the PDF, `cascade.py` and the log example.

10. **The code and the PDF disagree on the cascade:**
    - **R2 stuck meter:** the PDF uses φ = the longest frozen run, with φ ≥ τ. `cascade.py` and `thresholds.yaml` use φ = rolling std / typical std, with φ ≤ 0.05.
    - **R5:** the PDF says "CUSUM on the voltage offset, or π ≥ τ with ΔV > τ_V". The code says "CUSUM on neighbour ratio".
    - **Hard-coded thresholds:** the PDF says thresholds live in `configs/thresholds.yaml`, "not hard-coded". Nothing loads the YAML. The tests hard-code `TH`, and `n1_experiment.py` hard-codes the rule limits.

    Make the code match the PDF. Or add a small `load_thresholds()` and the sentence *"Phase 1 thresholds are hand-set prototypes; fitting is Phase 2."* The Fig. 10 caption says thresholds "are fitted", which is not true yet.

11. **Confidence bands differ between Goal 2 and Goal 3.** Goal 2 sets HIGH > 0.90 for every class. Goal 3 uses 0.85 for GENUINE_EVENT and adds a 0.30 margin rule. Pick one rule and state it in Goal 2 as well.

12. **The design text doesn't match your own results.** §5.4.3 calls Isolation Forest "our fast first ML pass", but §5.5.1 shows it is the weakest detector (11/36, 15/30, 2/8). Goal 2 also applies SHAP to the IF and the autoencoder, while the detections come mostly from OCSVM and the autoencoder. Update both:
    - demote IF to a cheap pre-screen, or drop it
    - plan KernelSHAP or permutation SHAP on OCSVM and the autoencoder

    Also say that the Phase 1 "autoencoder" is a 12-4-12 MLP on daily features (`MLPRegressor`), not the LSTM that §5.4.4 discusses. It also hits `max_iter=400` without converging (a warning on every fold). Raise `max_iter` or mention it.

---

## 🟡 Medium: references, layout and wording

13. **References**
    - Four bib entries are never cited: [29] McMahan, [30] Yin, [31] Blanchard, [32] Fung. They belong in §8.5.5: FedAvg → [29], coordinate-wise median → [30, 31], reputation and Sybil defence → [32]. Cite them there, because uncited entries look padded.
    - [17]–[23] have no authors, and [19] and [23] have no year or venue. Complete them.
    - [20] is an *Emergent Mind overview web page*. Replace it with a primary source, e.g. Guo et al., "On calibration of modern neural networks", ICML 2017, for calibration and Brier score.

14. **Layout**
    - **Page 35 is almost blank.** Figure 14 floated to the next page. Use `[!t]`/`[p]` placement or shrink the figure.
    - **The ASCII operator console** (§7.5) is split across pages 29–30. Wrap it in a non-breaking box, or redraw it as a TikZ figure. It is your only Goal 3 interface mock-up, so it should look intentional.

15. **Mixed spelling.** Goals 1 and 3 use *neighbourhood*. Goals 2 and 4 use *neighborhood*, as a result of merging parts by different authors. Pick one. The title uses British spelling.

16. **Typos and small fixes**
    - §8.5.2: "kept apart design" → "kept apart **by** design".
    - §5.5.2 says "share of the feeder's 10 meters", §6.2 says "the other 9 meters". Pick one.
    - Number formatting: "1 051 200" in §3 vs. "1,051,200" in §8.2.

17. **Length (46 pp.) and repetition.** The brief sets no page limit, but judges skim. Candidates to cut:
    - Textbook material in §5.4: the IF, OCSVM and autoencoder equations and toy figures, about 3 pages. These could go to the Goal 1 report, with one table kept.
    - §8.5, which restates §8.3–8.4.
    - The implementation-status disclaimers, which appear three times in §8.5.1, §8.5.8 and §8.9.

    Merge §8.5.8 into §8.9.

---

## ✅ Strengths to keep

- **The central question:** genuine grid event vs. bad data, answered with cross-sensor physics. It is clear, well grounded and carries through all four goals.
- **Real measured Goal 1 results** with an event-grouped CV, per-event Table 8, and an honest list of misses (bypass, bias, drift, clock shift). Most teams will submit only a design.
- **The non-trivial dataset design:** hard negatives (Ramadan, vacations, PV export) and the outage-as-zeros trap handled by R0.
- **Goal 3:** a monotone max-of-floors policy, "confidence never overrides consequence", blind-first review, and a check against the dataset's reference responses.
- **Goal 4:** a concrete sharing contract (C1–C4), a correct RDP calculation with an honest reading of it, C2 used as a negative control, and the real N3 → N1 coordinated-attack case for C4.
- **Label hygiene** enforced in code (`feature_columns`, `event_folds`).

## Suggested order for tomorrow

1. Push a standalone repo, then add the team, the repo URL and the authors (#1, #2): about 30 min
2. Business-scope section (#3): about 1 h
3. Remove or fix the unbacked claims (#4, #5, #10 caption): about 30 min
4. Consistency fixes (#6–#9, #11): about 1 h
5. References and layout (#13, #14), then rebuild the PDF with `build_parts.py` and re-check the page breaks
