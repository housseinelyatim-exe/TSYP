# Review of "Architecture and attacks" (Track 2: False-Data Injection), with explanations

**Reviewed file:** `Architecture and attacks.docx.pdf`, 6 pages: the architecture, the repo layout, the attack matrix and Layers 1–4.
**Checked against:** the TSYP14 brief and the Phase 1 scoring grid (`challenge-tracks-submissions-timeline.md`).
**Phase 1 deadline:** 08/11/2026 (anonymous report + code).

Each point below explains **what the document says**, **why that's a problem** (what a jury member would think), and **what to change**. The short version from the earlier review is in `architecture-layers-review.md`.

---

## 1. What the design does

The system defends sensor data against someone who wants to insert false readings. It does this in two different ways, and that split is the core idea of the design:

1. **Cryptography (Layer 1).** Each reading is signed right next to the sensor. If anyone changes it afterwards (on the network or in the database), the signature no longer matches, so the change is caught with certainty.
2. **Detection (Layers 2–3).** If the attacker interferes **before** signing (for example by tampering with the sensor itself, or by heating it), the signature is valid but the data is false. Cryptography can't see that. The only option left is to spot that the values *look wrong*: compared with the sensor's own history, with its neighbors, with physics rules, and with satellite/reanalysis data.
3. **Decision (Layer 4).** It combines both answers into a trust score per sensor, puts suspicious sensors in quarantine, and records every decision in a log.

That split is **correct and is the strongest idea in the document**. The attack matrix (page 2) shows it visually: purple dots = caught by cryptography, green dots = caught by detection. Juries like a design where each attack has a clear owner.

Other strong points:
- **Signing at the source:** even if the gateway or the database is compromised, past data stays verifiable.
- **Same code path for the replay harness and the live system:** test results really describe the real system, and the results can be reproduced (fixed seeds, YAML scenarios).
- **`ablation.py`:** shows what each detector contributes. That is exactly the kind of evidence an evaluation section needs.
- **The "authentic but suspicious" case** in Layer 4 (valid signature + abnormal data). This is the insight that ties the two halves together, and it should be the center of the pitch.

---

## 2. Where the document stands against the scoring grid

| Phase 1 criterion | Pts | Where it's addressed | Status | Explanation |
|---|---|---|---|---|
| Threat model & relevance | 15 | Attack list | Partial | A list of attacks is not a threat model. It's missing *who* the attacker is, *what they can access*, and *what we assume is trustworthy*. |
| Architecture & trust mechanism | 15 | Architecture + L1 | Good | Some cryptographic details are vague (§4). |
| Signal / image processing | 15 | L2 | Weakest | L2 states its input and output, but not *how* the data is processed. |
| Detector design & evaluation | 20 | L3 | Weak | L3 is a list of options ("Kalman or ARIMA or LSTM"), not a design. There's no fusion method and no evaluation protocol. |
| Standard scenario & evasion | 20 | Harness, `adaptive.py` | Missing | The official dataset is never named, and the adaptive attacker isn't described anywhere. |
| Feasibility & local execution | 10 | One Python process | Implied | Nothing says "runs on a laptop, X GB RAM, no GPU". |
| Clarity & reproducibility | 5 | Repo layout | OK | Needs a README, seeds and a single run command. |

**Reading the table:** the best-developed parts (architecture, crypto) are worth 30 pts. The parts worth 55 pts (processing, detection, evasion) are the least developed. The writing effort should go there now.

---

## 3. The three priorities

1. **Name the official dataset and the standard scenario.** The brief requires them, and the whole document depends on them: which sensors exist, how many neighbors each one has, the time step, and which reference data is available. Without that, every detector choice is guesswork, and the jury will see that the design wasn't built around the official data.
2. **Turn L2 and L3 from lists into decisions.** One method per detector, plus a stated way to combine their scores and a stated evaluation method. A jury scores what you *will do*, not what you *could do*.
3. **Write the evasion part.** Describe an attacker who knows our detectors and tries to stay below the thresholds, then show how far they can go without being detected. That's 20 pts, and resistance to the held-out attack is also the first tie-breaker.

---

## 4. Architecture and attack matrix

### 4.1 Some matrix cells claim more than the system can do

A jury member who knows security will check the matrix cell by cell. Every overclaim costs credibility on the whole document.

**a) "Stored data rewrite" caught by L1b**
- *What the doc says:* L1b (the verifier) catches someone who edits readings in the database.
- *Why it's wrong:* L1b checks the signature **once, when the data arrives**. The rewrite happens **after** that check, so L1b never sees it. The architecture also has no database of raw signed readings at all.
- *Fix:* store each reading **with** its signature and prev_hash. Re-check signatures when the data is read, or with a periodic audit job. Add an "audit / re-verification" column to the matrix, or move the dot there.

**b) "Timestamp shift" caught by L1b**
- *Why it's partly wrong:* there are three different cases hidden in one row.
  - **Changing** a timestamp inside a signed record breaks the signature → caught by L1b. ✔
  - **Delaying** a valid record (holding it, then sending it late) leaves the signature valid. Only the freshness check (`out_of_window`) catches it, and that check only works if the sensor clocks are synchronized (NTP/GPS). That assumption must be stated.
  - **Changing the sensor clock before signing** is a category-A attack: the signature is valid. It isn't covered anywhere.
- *Fix:* split the row into "modify" vs "delay", and add "clock manipulation at source" to section A.

**c) "Delete / reorder" caught by the hash chain**
- *Why it's incomplete:* the hash chain only shows a missing record **when the next one arrives**. If the attacker cuts off the end of the stream, or silences the sensor during exactly the event they want to hide, no next record ever arrives and nothing is flagged.
- *Fix:* add a liveness check (heartbeat). If no message arrives within the expected period, the sensor gets a `gap`/`stale` status.

**d) "Slow drift" and "Colluding neighbors": primary catch = satellite**
- *The contradiction:* the architecture diagram labels the satellite cache **"Optional"**. An optional component can't be the *main* defense against two attacks.
- *Technical limit:* ERA5 has a resolution of about 31 km per hour, and SMAP 9–36 km. These sources describe a large area, not one exact point, so they only catch **large** shifts. A drift of a few percent will go through.
- *Fix:* either make the reference source mandatory, or downgrade those cells to "partial". In both cases, state the **minimum detectable bias** honestly (e.g. "we detect a shift ≥ X % after Y hours").

**e) "Ref. satellite" column**
- Every other column is a layer; this one is a data source. Rename it **"L3 cross-source"** so the matrix stays consistent.

### 4.2 Attacks missing from the list

These are the questions an expert jury is likely to ask. Including them yourselves shows the threat model is mature.

| Missing attack | Why it matters | Mitigation to state |
|---|---|---|
| **Compromised node / stolen key** | The attacker signs false data with a real key. L1 says it can't handle this, but the matrix doesn't show it, even though it's exactly the "authentic but suspicious" case L4 handles. | Add the row; L3 + L4 catch it. |
| **Calibration poisoning** | If a slow drift is injected *during* the "clean" period used to learn thresholds, every threshold shifts and the attack becomes "normal". | Calibrate on a verified period and cross-check it against the reference source. |
| **Reference-data poisoning** | If the satellite cache can be modified, the cross-source detector is fooled too. | Hash or sign the cached files. |
| **Sequence counter reset after a reboot** | If the counter goes back to 0 after a restart, old records become "valid" again, so replay becomes possible. | Store the counter persistently, or add a "boot epoch" to each record. |
| **Selective silence** | A compromised sensor simply sends nothing during the event. | Heartbeat (see 4.1c). |
| **Adaptive attacker** | Someone who knows CUSUM/EWMA and keeps each step below the threshold. `adaptive.py` exists in the repo, but the document never describes it. | Describe its strategy and measure how far it gets (§7). |

### 4.3 There's no threat model

Deliverable #1 (15 pts) asks for a **threat model**, not just a list of attacks. Half a page is enough:
- **Assets to protect:** readings, signing keys, the audit log, the products derived from the data.
- **Capabilities per attacker family:**
  - A = physical or firmware access to the sensor;
  - B = man-in-the-middle on the network;
  - C = write access to the database (insider or intrusion).
- **Trust assumptions:** the gateway *process* is trusted. Family C can write to the database but can't run code inside the pipeline. **This must be explicit**, because L1b–L4 all run in the same process: if that process is compromised, everything falls.
- **Out of scope:** what is explicitly not covered (e.g. denial of service, a compromised gateway process).

### 4.4 Smaller points
- "One of only two real network hops": name the second one (L4 → dashboard).
- Say **where demo data comes from**: the official dataset replayed through an emulated sensor plus a software signer. The brief allows this ("software or emulated trust anchor is valid"), so say it openly. Otherwise the jury will wonder where the physical sensors are.
- Metrics: the doc lists recall, false alarms, latency and overhead. The brief also asks for **memory** and **security overhead**. Give concrete numbers: bytes added per message (64 B signature + 32 B prev_hash + counter) and signing/verification time in µs.
- Repo: add `tests/`, a `README`, `requirements.txt`, a single run script (`run_all.sh` or `Makefile`), and a `.gitignore` that excludes keys. **Never commit a private key.** The repo must be anonymous from the first commit.
- **State "Track 2" at the top of the document.** Right now nothing says which track this is.

---

## 5. Layer 1: Provenance (signing and verification)

**Good points:** a clear goal, a minimal message format, a list of statuses passed on to L4 (instead of silently dropping bad records), and an honest limitations section.

**Issues:**

1. **"Ed25519 or HMAC": choose Ed25519.**
   *Why:* HMAC uses a **shared secret**, so the gateway must know every sensor's secret. Anyone who compromises the gateway or the database can then produce "valid" records for any sensor, which breaks the protection against family C. With Ed25519 the gateway only holds **public keys**, which can't be used to sign. The architecture already says Ed25519, so the L1 text should match.

2. **Specify exactly which bytes are signed (canonical CBOR).**
   *Why:* CBOR can encode the same data in several ways (key order, integer size…). If the sensor encodes one way and the gateway re-encodes another, a perfectly valid signature fails. Use deterministic CBOR (RFC 8949 §4.2) and state it.

3. **Define `prev_hash`.** It should be the hash of the **full** previous record, signature included. Otherwise the chain can be rebuilt with different signatures.

4. **Key lifecycle.** The doc says "key rotation is valid" without explaining it. Cover: how the key registry is filled, how a key is revoked, and add a **`key_id`** field to the message. Without it, the gateway doesn't know which key to verify with after a rotation.

5. **Statuses.** Separate `chain_break` (broken chain) from `gap` (missing records), give the `out_of_window` tolerance in seconds, and add `stale` (silent sensor).

6. **"Per reading or per small batch": choose one.** Batching reduces overhead but increases latency (you have to wait for the batch to fill). Choose, and give the trade-off as a measured number.

7. **TLS vs signature.** Say which TLS configuration is used (mutual TLS? one certificate per sensor?) and explain the difference: **TLS protects one hop, the signature protects the data end to end, even after storage**. It's a short sentence that shows the jury the team understands why both are needed.

8. **Cleanup:** remove the MQTT definition and the generic broker diagram. The jury knows MQTT, and that space is better used on points 1–7.

---

## 6. Layer 2: Signal processing (15 pts, the thinnest section)

**What exists:** the goal, the input and the output (`FeatureWindow`). The output is well chosen: keeping both `raw_value` **and** `clean_value`, and carrying `provenance_status` through, is the right call.

**What's missing:** the method itself. The section is worth 15 pts and is 6 lines long. The processing chain should be described step by step:

1. **Basic preparation:** convert units, put all sensors on the **same time step** (e.g. 10 min or 1 h, to match the dataset), and mark gaps explicitly. *Don't fill gaps silently*, because a gap can itself be a sign of attack.

2. **Resolve the central tension the doc names but doesn't answer:** "clean the data without erasing attack signatures". If you smooth the data before detecting, you also smooth away the attack. **Proposed rule:** *detectors work on raw values and residuals; the cleaned value is used only for imputation and neighbor comparison.* Write this rule down: it's a strong design argument and it answers the question before the jury asks it.

3. **Exclude untrusted sensors from neighbor comparisons.** If a sensor that failed L1 (or is quarantined by L4) still counts in its neighbors' average, it contaminates them. That creates a **feedback loop from L4 → L2**, which must appear in the diagram.

4. **Seasonal residual:** name the method (e.g. STL decomposition with a daily period, or harmonic regression) and the training window. The residual is "what remains after removing the normal daily cycle"; that's where an attack becomes visible.

5. **Rolling and spectral features:** give the window lengths. Explain *why* spectral features (power spectrum, autocorrelation): they detect **noise injection, over-smoothing and stuck values**, which a simple mean misses. Link them to those rows of the matrix.

6. **Neighbors:** how are they chosen? (k nearest within a radius R, same sensor type, similar elevation.)

7. **Reference data:** align satellite/reanalysis data to the sensor's location and time step, then **correct the systematic bias** (e.g. CDF matching). *Why:* a ground sensor and a 30 km pixel never give the same value. Without correction, the cross-source detector raises alarms constantly on normal data.

8. Give the **processing time and memory per window** (feasibility criterion).

---

## 7. Layer 3: Detection ensemble (20 pts)

**Good points:** a clear output (`score`, `p_value`, `evidence` per detector), threshold calibration on clean data with empirical quantiles or conformal prediction, and a sensible split into detector families.

**Issues:**

1. **Every detector is "X or Y or Z".** A jury scores a design, not a menu. A realistic Phase 1 set, each with its justification:

   | Family | Choice | What it catches | Why this choice |
   |---|---|---|---|
   | Temporal | Kalman residual + **CUSUM** | bias, slow drift | CUSUM accumulates small deviations, so it's made for slow drift |
   | Temporal | **EWMA on variance** | noise, over-smoothing | watches how much the signal varies, not just its level |
   | Spatial | leave-one-out kriging or GP (IDW if few sensors) | bias, mimicry, masking | predicts a sensor from its neighbors and compares |
   | Rules | range, rate of change, stuck value (n identical), dew point ≤ temperature | spikes, freezing | simple, explainable, almost no false alarms |
   | Cross-source | residual vs bias-corrected reference | drift, collusion | independent of the attacked sensors |
   | Unsupervised | **Isolation Forest** on the feature vector | the rest | light, no labels needed |

   **Drop LSTM, LSTM-autoencoder and GNN for Phase 1.** They're expensive to justify (training data, tuning) and hurt the feasibility criterion. At most, they could be a Phase 2 comparison. Remove the LSTM definition box too.

2. **Fusion is undefined.** The output is called `anomaly_posterior` (a posterior probability), but nothing explains how it's calculated.
   *Recommendation:* combine the detectors' **p-values** (Fisher's method, or the **Cauchy combination**, which stays valid even when detectors are correlated, as they are here).
   *Why not a supervised model trained on our own attacks?* Because it learns *our* attacks. Phase 2 includes a **held-out** attack never seen before, and a supervised model risks missing it. Combining p-values needs no attack examples, so it generalizes better.
   If you keep the word "posterior", you have to define a prior. Otherwise call it "fused anomaly score".

3. **`attack_family_hint`:** say how it's produced. Simple proposal: compare *which detectors fired* against the attack matrix. The matrix already **is** the lookup table.

4. **Control the false-alarm volume.** With many sensors × many time steps × many detectors, even a 1 % threshold per detector creates a flood of alarms. Set a target as **alarms per sensor per day**, and calibrate the fused threshold to meet it. A low false-alarm rate is the **second tie-breaker**.

5. **Missing evaluation protocol.** This is what turns "we have detectors" into "we've proven they work":
   - Split calibration / validation / test **by time** (never shuffle), so the future doesn't leak into the past.
   - Metrics **per attack family**: recall, false alarms, **detection delay** (essential for slow drift: catching it after 3 weeks is worthless), and event-level precision.
   - **Leave some attack families out during tuning**, to simulate the held-out Phase 2 attack.
   - **Evasion curve:** detection rate against attack size, plus the **maximum undetected impact** reached by the adaptive attacker (e.g. "a bias below 0.8 % stays invisible for 48 h"). This one plot covers most of the 20-pt "evasion" criterion.

---

## 8. Layer 4: Trust score and response

**Good points:** the most complete section. A signature failure overrides everything, the "authentic but suspicious" case is separate, hysteresis prevents flapping, raw readings are always kept, the audit log is hash-chained and linked to the brief's "processing history", and only trusted or imputed values are released.

**Issues:**

1. **The trust formula is missing.** "Combine provenance and anomaly into a 0–1 score" is not a formula.
   *Proposal:* invalid signature → score 0 (hard override); otherwise `trust_t = EWMA(1 − anomaly_t)`, i.e. a smoothed average of "normality".
   Give the thresholds as numbers: enter *suspicious* below 0.6, leave it above 0.75, enter *quarantine* below 0.3. The gap between entry and exit thresholds is what prevents flapping.

2. **Imputation can spread the attack.** If you replace a bad reading with its neighbors' estimate, and those neighbors are themselves attacked (collusion), you **launder** the false data into a "clean" value.
   *Fix:* impute **only from trusted neighbors**, otherwise fall back to the sensor's own Kalman prediction. Every imputed value released must carry `imputed=true` and its uncertainty.

3. **Leaving quarantine.** A clever attacker behaves well for a while to regain "trusted" status, then attacks again.
   *Fix:* require N clean windows **plus** analyst acknowledgment to leave quarantine, or at least record it in the log as an explicit decision.

4. **An "append-only" SQLite table isn't tamper-proof on its own.** Anyone with write access to the database can rewrite the **whole** chain consistently (recalculating every hash).
   *Fix:* periodically **sign the chain head** with a gateway key and export it outside the database (a file, the dashboard). Rewriting history then becomes detectable. This also fixes the "stored data rewrite" cell in the matrix (§4.1a).

5. **Dashboard "over the network":** TLS + authentication, or bind to localhost for the demo. Choose **Streamlit or FastAPI**, not both. Streamlit is faster for Phase 1.

6. **"Notify":** name the channel (a dashboard alert or a log entry is enough).

7. **Show both cases side by side in the dashboard:** "tampered in transit" (caught by L1) vs "authentic but suspicious" (caught by L3). It's the clearest way to explain the whole architecture in a 7-minute pitch.

---

## 9. Form and presentation of the PDF

Fix these once, at the end, after the content is right.

| # | Issue | Why it matters | Fix |
|---|---|---|---|
| 1 | Every bullet shows as an empty box (``) on pages 3–6 | The Google Docs export lost the bullet font. It looks broken. | Use the standard list style and check the PDF after export |
| 2 | Yellow highlights, red and blue text | They look like draft notes, not a report | Remove them. Put schemas in a monospace block |
| 3 | No title, no track, no introduction | The reader doesn't know what they're reading | Title, "Track 2", ½-page problem statement + threat model |
| 4 | The matrix (p.2) mentions L1b/L3 before the layers are explained (p.4–6) | The reader meets terms before their definitions | Order: Problem → Threat model → Architecture → L1–L4 → Attacks + matrix → Evaluation |
| 5 | Heading "Attack type is injected and which layer catches it" | Grammatically broken | "Attack coverage: which layer catches each attack" |
| 6 | Matrix label says "data is false", the text doesn't | Inconsistent | Use the same label in both places |
| 7 | Definition boxes (MQTT, LSTM, audit log) | ⅓ page that earns no points | Delete them or move them to an appendix |
| 8 | Inconsistent headings ("Layer 1 : provenance" vs "Layer 2 : Signal processing", "Detectors :") | Looks careless | "Layer N — Title", no space before colons |
| 9 | No page numbers, no figure captions | The two diagrams are the best content and aren't referenced | "Fig. 1", "Fig. 2" + captions |
| 10 | File named `….docx.pdf`, PDF title "Architecture and attacks.docx" | Unprofessional, and metadata matters for anonymity | Rename it, set a neutral title. Check Author is empty on every export (it is, for now) |
| 11 | L2 = 6 lines, L4 ≈ 1 page | The length is the reverse of the points available (L2+L3 = 35 pts) | Expand L2 and L3 with the decisions in §6–7 |
| 12 | Naming: "L1a/L1b" in the architecture, "two halves" in L1 | Inconsistent | Use L1a/L1b everywhere |

**Suggested template for each layer:** Goal → Input → **Method (decisions)** → Output → Metrics → Limitations. Today only L1 and L4 have a limitations section.

Also add **one table of all data contracts** (`VerifiedReading`, `FeatureWindow`, `DetectorOutput`, `FusedResult`, `TrustDecision`) matching `core/contracts.py`.

---

## 10. Action plan (in order)

| # | Action | Criterion it serves | Section |
|---|---|---|---|
| 1 | Confirm the official dataset + scenario; set sensors, neighbors, time step, reference source | All | §3 |
| 2 | Write the threat model (½ page) and fix the matrix | Threat model (15) | §4 |
| 3 | Write the L2 method | Processing (15) | §6 |
| 4 | Choose the L3 detectors + fusion | Detection (20) | §7.1–7.4 |
| 5 | Define the evaluation protocol, describe the adaptive attacker, produce the evasion curve | Detection (20) + Evasion (20) | §7.5 |
| 6 | Specify the L4 formula/thresholds and anchor the audit log | Architecture (15) | §8 |
| 7 | Settle L1 details (Ed25519, canonical CBOR, key_id, statuses) | Architecture (15) | §5 |
| 8 | Repo: README, single command, seeds, no keys, anonymity | Reproducibility (5) + Feasibility (10) | §4.4 |
| 9 | Final formatting pass and PDF check | Clarity | §9 |

**Bottom line:** the architecture is good and well thought out. The work left is to **turn options into decisions** and to **prove with numbers** that the detection works and resists an informed attacker. That's where most of the points are.
