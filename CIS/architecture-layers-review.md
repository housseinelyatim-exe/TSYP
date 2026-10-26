# Review: Architecture & Attacks + Layers 1–4 (Track 2: False-Data Injection)

Reviewed: `Architecture and attacks.docx`, `Layer 1.docx` to `Layer 4.docx` (the Layer 4 version updated 10/10), plus the two embedded diagrams (system architecture, attack-coverage matrix).
Checked against the TSYP14 brief and the Phase 1 rubric (see `challenge-tracks-submissions-timeline.md`).

---

## 1. Verdict

The architecture is solid. It splits the problem the right way: cryptography (L1) catches attacks after signing, and detection (L2–L3) catches attacks before signing. The attack matrix makes that split clear, and it's the best artifact in the set. The plan to run the offline harness through the same code path as the live system is a strong reproducibility choice, and the layers map neatly onto the rubric:

| Rubric item (Phase 1) | Pts | Covered by | Current state |
|---|---|---|---|
| Threat model & relevance | 15 | Attack list | **Partial.** Attacks are listed, but there is no attacker model or trust boundaries |
| Architecture & trust mechanism | 15 | Arch doc + L1 | **Good**, with a few crypto details missing |
| Signal / image processing | 15 | L2 | **Weakest.** Only input and output are defined, with no method |
| Detector design & evaluation | 20 | L3 | **A menu of options, not a design.** No fusion method, no evaluation protocol |
| Standard scenario & evasion | 20 | Harness, `adaptive.py` | **Missing.** The official dataset and the adaptive attacker are never described |
| Feasibility & local execution | 10 | Single Python process | Implied but not stated (laptop, RAM, no GPU) |
| Clarity & reproducibility | 5 | Repo layout | OK. Needs seeds, a README and a one-command run |

**The 3 most urgent fixes:**
1. **Name the official reference dataset and the standard scenario.** None of the five docs mentions them, but they are mandatory and they decide which sensors, neighbors and reference data you actually have.
2. **Turn L2 and L3 from option lists into decisions.** Pick one method per detector, define fusion, and define the evaluation protocol.
3. **Write the evasion story** (the adaptive attacker plus a detectability-vs-impact curve). It's worth 20 pts, and the held-out attack decides the first tie-break.

---

## 2. Architecture & attacks doc

### What works
- Signing at the source, so provenance survives a compromised downstream. Correct, and well argued.
- Separate attack families A, B and C, each tied to the layer that catches it.
- An offline harness with seeded YAML scenarios and deterministic replay, so results are reproducible.
- `eval/ablation.py`, which shows each detector's contribution. Juries like this.

### Problems

**a) Some cells of the attack matrix are wrong or overclaimed**

| Row | Issue | Fix |
|---|---|---|
| **Stored data rewrite → L1b** | L1b runs **at ingest**, but the rewrite happens **after** verification, so L1b never sees it. Also, no raw-record store appears anywhere in the architecture. | Store each record together with its signature and prev_hash. Re-verify on read or with a periodic audit job, and anchor the audit-log head (see L4). Add a column such as "Re-verify / audit". |
| **Timestamp shift → L1b** | If the timestamp is inside the signed payload, *changing* it is just value tampering. *Delaying* a valid record keeps the signature valid and is caught only by the `out_of_window` freshness check, which needs synced sensor clocks (assumption: NTP or GPS time at the sensor). A timestamp shifted **before signing** (compromised sensor clock) is a category-A attack and isn't covered. | Split the row into "modify" (signature) and "delay" (freshness window). Add "clock manipulation at source" to section A. |
| **Delete / reorder** | The hash chain only detects a deletion when the *next* record arrives. Dropping the tail, or silencing the sensor entirely during an event, goes undetected. | Add a liveness/heartbeat check: a `gap` status raised when nothing arrives for longer than the expected period. |
| **Slow drift and colluding neighbors → "Ref. satellite" as primary catch** | The architecture diagram marks the satellite cache as **"Optional"**. Two primary catches can't depend on an optional component. Also, ERA5 (~31 km, hourly) and SMAP (9–36 km) are coarse, so they only catch *large* shifts. | Make the reference source mandatory, or downgrade those cells to "partial". Give the minimum detectable bias honestly. |
| "Ref. satellite" column | It's a detector, not a layer. | Rename it "L3 cross-source" so the columns stay consistent. |

**b) Attacks missing from the list** (an expert jury will ask about these)
- **Compromised node with valid keys / key theft.** Layer 1 mentions it as a limitation, but it's missing from the matrix. It's exactly the "authentic but suspicious" case that L4 reports, so show it.
- **Calibration poisoning.** A slow drift injected *during* the clean training/calibration window shifts every threshold. Mitigation: calibrate on a vetted period and cross-check it with the reference source.
- **Reference-data poisoning.** Tampering with the satellite cache. Mitigation: hash or sign the cached files.
- **Sequence-counter reset after a reboot.** It lets an attacker replay old records. Mitigation: persist the counter, or add a boot epoch to the record.
- **Selective suppression at the source.** A compromised node sends nothing during the event it wants to hide.
- **Adaptive / threshold-aware evasion.** An attacker who knows the detectors keeps each step under the CUSUM/EWMA thresholds. `adaptive.py` exists, but the docs never describe it.

**c) No threat model.** Deliverable #1 (15 pts) needs more than a list of attacks. Add half a page covering:
- **Assets:** readings, keys, audit log, products.
- **Attacker capabilities per family:** A = physical or sensor-firmware access, B = network man-in-the-middle, C = database/insider access.
- **Trust assumptions:** the gateway *process* is trusted, and C assumes write access to the database but not code execution in the pipeline. Say this explicitly, because L1b through L4 share one process.
- **Out of scope.**

**d) Minor**
- The doc says the link is "one of only two real network hops". Name the second one (L4 → dashboard).
- The diagram should say *where the data comes from* in a demo: the official dataset replayed through an emulated sensor plus a software signer. That's allowed ("software or emulated trust anchor is valid"), so state it openly.
- Metrics list "recall, false alarms, latency, overhead". The brief explicitly requires **memory** and **security overhead** as well. Report bytes per message (64 B signature + 32 B prev_hash + seq) and sign/verify time in µs.
- Repo: add `tests/`, a `README`, `requirements.txt` or a lockfile, a `Makefile` or `run_all.sh`, and a `.gitignore` for keys (**never commit private keys**). Keep the repo anonymous from the first commit.
- None of the docs says which track this is. State **Track 2** at the top.

---

## 3. Layer 1: Provenance

**Good:** clear goal, a minimal record format, an explicit status enum that is passed on to L4 instead of just dropping bad records, and an honest limitations section.

**Issues:**
1. **The doc says "Ed25519 or HMAC". Pick Ed25519.** With HMAC the gateway holds every sensor's secret, so a gateway or database compromise lets an attacker forge "valid" records. That breaks the category-C story. Ed25519 only needs public keys on the gateway, and the architecture doc already says Ed25519.
2. **Canonical encoding.** You sign CBOR, so you must use deterministic/canonical CBOR (RFC 8949 §4.2). Otherwise the verifier re-encodes the record slightly differently and valid signatures fail. Specify exactly which bytes are signed.
3. **Define `prev_hash`.** Is it the hash of the full previous record *including* its signature? It should be.
4. **Key lifecycle.** The doc mentions key rotation but doesn't describe it. Cover: how `keyregistry` is provisioned, how a key is revoked, and what the `key_id` in the record is (it's missing from the message format; add it).
5. **Status enum.** Distinguish `chain_break` from `gap`. Define the `out_of_window` tolerance in seconds. Add `stale` (heartbeat timeout).
6. **Batching.** "Per reading, or per small batch". Pick one. Batching cuts overhead but adds latency, so state the trade-off as a measured number.
7. **Cleanup:** the stray text `3265805114300` is a broken image-anchor artifact. Delete it. Shorten the MQTT definitions to one line; the report doesn't need the generic broker diagram.
8. **Missing:** MQTT/TLS configuration (mutual TLS? per-sensor client certs?). Note that TLS protects the hop and the signature protects the data end to end. That distinction is a nice point for the report.

---

## 4. Layer 2: Signal processing (thinnest doc, 15 pts)

Only the goal, input and output are defined. The output schema is good: keeping both `raw_value` and `clean_value`, and carrying `provenance_status` through, is the right call. The doc needs the actual processing chain:

1. **Ingest hygiene:** unit normalization, then resampling onto a common time grid (state the grid, e.g. 10 min or 1 h, to match the dataset), then gap marking. Don't interpolate silently.
2. **The key tension** (the doc names it but doesn't solve it): "clean without erasing attack signatures". Proposed rule: **detectors run on raw values and residuals. `clean_value` is used only for imputation and neighbor consensus.** Write this down; it's a strong design argument.
3. **Provenance-aware consensus:** readings that fail L1 (or come from sensors L4 has quarantined) must be **excluded** from the neighbor features. Otherwise one bad sensor contaminates its neighbors. This creates a feedback loop from L4 to L2, so draw it in the architecture diagram.
4. **Seasonal residual:** name the method (e.g. STL with a daily period, or harmonic regression) and the training window.
5. **Rolling and spectral features:** window lengths. Spectral features (Welch PSD, FFT band energy, lag-1 autocorrelation) are what catch noise injection, flattening and stuck-at, so connect them to those rows of the matrix.
6. **Spatial:** how neighbors are defined (k-nearest within a radius R, same sensor type, similar elevation).
7. **Reference data:** spatial and temporal alignment of ERA5/satellite data to the sensor point, plus **bias correction** (e.g. CDF matching), because in-situ and gridded products differ systematically. Without that correction the cross-source detector raises false alarms constantly.
8. Report the processing latency and memory per window.

---

## 5. Layer 3: Detection ensemble (20 pts)

**Good:** a clear output contract (`score`, `p_value`, `evidence`), calibration on clean windows with conformal or empirical-quantile thresholds, and a sensible split into detector families.

**Issues:**
1. **Every detector is a list of "X or Y or Z".** The report needs one choice per family, justified on cost, data needs and the attacks it targets. A feasible Phase 1 set:
   - Temporal: **Kalman (or SARIMA) residual + CUSUM** (drift, bias) **+ EWMA on variance** (noise, flatten).
   - Spatial: **leave-one-out kriging or GP residual**. IDW also works if the dataset has few sensors.
   - Rules: range, rate-of-change, stuck-at (n identical values), and cross-variable checks (dew point ≤ temperature).
   - Cross-source: a residual against the bias-corrected reference.
   - Unsupervised: **Isolation Forest** on the feature vector.
   - Drop the LSTM, LSTM-autoencoder and GNN for Phase 1. They're expensive to justify and they hurt the feasibility score. They could be a Phase 2 ablation at most.
2. **Fusion is undefined**, yet the output is called an `anomaly_posterior`. Recommended: **p-value combination** (Fisher, or the Cauchy combination test, which stays valid when detectors are correlated). It's unsupervised, keeps calibration intact, and won't overfit your own injected attacks. A supervised stacker trained on your attack library risks failing on the **held-out** Phase 2 attack. If you keep the word "posterior", define the prior.
3. **`attack_family_hint`:** say how it's derived. Proposal: match the pattern of detectors that fired against the attack matrix (the matrix already *is* the lookup table).
4. **Control the false-alarm budget.** With many sensors × time steps × detectors, per-detector α = 0.01 still produces a lot of alarms. Set the target as an **alarm rate per sensor-day** and calibrate the fused threshold to it. A lower false-alarm rate is **tie-break #2**.
5. **Evaluation protocol (missing):**
   - Calibration, validation and test splits by **time**, with no leakage.
   - Metrics per attack family: recall, FAR, **detection delay** (essential for slow drift), and precision at the event level as well as the point level.
   - **Hold back some attack families or parameters during tuning** to simulate the held-out Phase 2 attack.
   - **Evasion curve:** detection rate vs attack magnitude, and the *maximum undetected impact* the adaptive attacker achieves (e.g. "a bias under 0.8 % goes undetected after 48 h"). That one plot covers most of the "evasion" criterion.

---

## 6. Layer 4: Trust score & response (updated version)

**Good:** the strongest of the layer docs. It has a signature-failure override, a separate *"authentic but suspicious"* case (which shows good insight), hysteresis, a "keep raw" rule, a hash-chained audit log tied to the brief's "processing history", and "only trusted or imputed values released".

**Issues:**
1. **The trust score formula is unspecified.** Proposal: `provenance invalid → 0` (hard override); otherwise `trust_t = EWMA(1 − posterior_t)`. Give the hysteresis thresholds as numbers, e.g. enter suspicious < 0.6 and exit > 0.75; enter quarantine < 0.3.
2. **Imputation can spread the attack.** If neighbors collude, or are themselves suspicious, imputing from them launders the false data. Impute **only from trusted neighbors** and fall back to the sensor's own Kalman prediction. Every imputed value released downstream must carry an `imputed=true` flag and its uncertainty.
3. **Quarantine exit:** a compromised node can behave cleanly to get back into trusted state. Leaving quarantine should need N clean windows **plus analyst acknowledgment**, or at least be logged as a decision.
4. **An append-only SQLite table isn't tamper-proof on its own.** Anyone with database access can rewrite the whole chain consistently. Periodically **sign the chain head with a gateway key and export it** (to a file or the dashboard). This is also what makes "Stored data rewrite" detectable (§2a). Put a pointer here and fix the matrix.
5. **Dashboard "over the network":** add TLS and authentication, or bind to localhost for the demo. Choose either Streamlit *or* FastAPI. Streamlit is quicker for Phase 1.
6. "Notify": name the channel (dashboard alert or log is enough).
7. Keep both cases visible in the dashboard: **"tampered in transit"** (L1) vs **"authentic but suspicious"** (L3). That split is the clearest way to present the whole architecture during the 7-minute pitch.

---

## 7. Format / consistency notes for the report

- Use one naming scheme: the arch doc uses L1a/L1b and the layer docs say "two halves". Use L1a/L1b everywhere.
- Each layer doc should follow the same template: **Goal → Input → Method (decisions) → Output → Metrics → Limitations**. Today only L1 and L4 have limitations sections.
- Define every data contract (`VerifiedReading`, `FeatureWindow`, `DetectorOutput`, `FusedResult`, `TrustDecision`) in one table so it matches `core/contracts.py`.
- Remove textbook definitions (MQTT, LSTM, audit log) from the report, or move them to a glossary. The jury doesn't need them.

## 8. Suggested next actions (priority order)

1. Confirm the official dataset and the scenario, then fix the sensor types, neighbors and reference source.
2. Write the threat model (½ page) and fix the attack matrix (§2a, §2b).
3. Fill in L2's method (§4) and choose L3's detectors and fusion method (§5.1–5.2).
4. Define the evaluation protocol and the adaptive attacker. Produce the evasion curve.
5. Specify the L4 trust formula and the audit-head anchoring.
6. Repo hygiene: README, one-command reproduction, seeds, no keys, anonymity.

---

## 9. Addendum (12/10): the merged PDF, `Architecture and attacks.docx.pdf`

**What changed since the 10/10 review:** almost nothing. The PDF is the five .docx files combined into one 6-page export from Google Docs. I compared the text line by line. The only differences are:
- The stray `3265805114300` anchor in L1 is gone (§3.7 is done).
- The attack descriptions (A/B/C) now come after the matrix.

None of the content issues in §1–§8 have been fixed yet. The matrix still overclaims for stored rewrite, timestamp shift and the satellite cells, and it's still missing several attacks. There's still no threat model, L2 still has no method, L3 still offers "X or Y or Z" choices with no fusion method, and L4 still has no trust formula. Everything in §8 still applies, in the same order.

### New issues that only show up in the compiled PDF

| # | Issue | Fix |
|---|---|---|
| 1 | **Every bullet shows as an empty box (``)** on pages 3–6. The Symbol-font bullets didn't survive the Google Docs export. | Use the standard bulleted-list style, then re-export and check the result. |
| 2 | **Drafting marks are still in:** yellow highlights, red text for schemas and blue text for data flows. In a report they look like unfinished notes. | Remove the highlights. Put schemas in a monospace code block and data flows in plain text or a table. |
| 3 | **No title, no track, no introduction.** Page 1 opens straight on "Architecture". | Add a title, "Track 2: False-Data Injection", and a ½-page problem statement + threat model (§2c) before the architecture. |
| 4 | **Odd order:** the attack descriptions (p.3) come after the matrix (p.2), and the layers come after the attacks. The matrix columns refer to L1b/L3 before those layers are defined. | Suggested order: Problem → Threat model → Architecture → L1–L4 → Attack matrix + descriptions → Evaluation. |
| 5 | **Heading grammar:** "Attack type is injected and which layer catches it". | "Attack coverage: which layer catches each injected attack". |
| 6 | **Inconsistent matrix labels:** the matrix header says "A. Before signing (signature stays valid, **data is false**)", but the text heading leaves out "data is false". Section C's heading has no space before it (p.3). | Use the same label in both places and fix the spacing. |
| 7 | **Textbook boxes are still in** (MQTT + broker diagram, LSTM, audit-log definition). They take about ⅓ page and score nothing. The LSTM definition is there to support a detector we recommend dropping (§5.1). | Delete them, or move them to a glossary/appendix. |
| 8 | **Inconsistent headings:** "Layer 1 : provenance" (lowercase, space before the colon) vs "Layer 2 : Signal processing", and "Detectors :", "General overview :". | Use "Layer N — Title" with no space before colons. |
| 9 | **No page numbers, figure captions or figure numbers.** The two diagrams are the strongest content and should be referenced from the text as "Fig. 1" and "Fig. 2". | Add captions and page numbers. |
| 10 | **File name** `….docx.pdf`; the PDF Title metadata is "Architecture and attacks.docx". | Rename it (e.g. `report.pdf`) and set a neutral Title. **Anonymity:** there's no Author field right now (good). Check this again on every export, plus the image metadata and the Google Docs revision owner. |
| 11 | **Length/balance:** L2 is 6 lines, while L4 is about 1 page. The rubric gives L2 (signal processing) 15 pts and L3 (detector) 20 pts. | Grow L2 and L3 to roughly match L4 once the §4/§5 decisions are made. |

### Bottom line
Merging everything into one document is the right step toward the Phase 1 report (deadline **08/11**, ~4 weeks out). This version is a formatted copy of the same drafts, though, not a revision. Next: apply §8 items 1–3 (dataset/scenario, threat model and matrix fixes, L2/L3 decisions). Do the formatting pass (table above) last, and only once.
