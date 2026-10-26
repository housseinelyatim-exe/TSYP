# City Brain: Phase 1 Proposal (v2)

**TSYP14 · City Brain Convergence · City Brain layer**
**Version 2, 8 October 2026** · replaces [`city-brain-phase1-proposal.md`](city-brain-phase1-proposal.md) (v1, 5 Oct)
**Phase 1 submission:** 7 November 2026 · **CSTAM pitch + live demo:** 14 November 2026

---

## What changed since v1

| # | Team decision | What it replaces |
|---|---|---|
| 1 | **The LLM runs locally on a dedicated edge device** | "Local model on the demo laptop, cloud optional" |
| 2 | **A mathematical model drives all scoring**: evidence, priority, action utility, allocation | The informal utility formula and greedy allocator |
| 3 | **Mocks for both input and output**: mock sensors/Guardian in, mock actuators out | Mocks of the Twin and Guardian only |
| 4 | **MQTT for all input and output** | "WebSocket by default, MQTT if the triplet prefers" |

Everything else from v1 stays: reflex + LLM reasoning + policy gate, trust-weighted detection, Guardian-down policy, guardrails, why cards, scenarios.

---

## 1. In one sentence

> **An AI City Brain running fully on the edge: a local LLM reasons about the whole city, a mathematical model scores every option, and a deterministic gate guarantees safety, all connected over MQTT.**
>
> *The LLM proposes, the math scores, the gate guarantees.*

---

## 2. Architecture

```
                         ┌──────────────── MQTT broker (Mosquitto, TLS + ACL) ────────────────┐
                         │                                                                     │
  Twin / mock sensors ──▶│ city/{zone}/sensor/…    city/{zone}/call    twin/meta/…             │
  Guardian / mock     ──▶│ guardian/verdict/…      guardian/quarantine/…   guardian/status     │
                         │                                                                     │
                         └───────┬─────────────────────────────────────────────▲──────────────┘
                                 │ subscribe                                    │ publish
                ┌────────────────▼──────────────────────────────────────────────┴────────────┐
                │ CITY BRAIN                                                                 │
                │                                                                            │
                │  validate ─▶ detect ─▶ MATH MODEL ─▶ REFLEX ──┐                            │
                │                           ▲   │               ▼                            │
                │                           │   └──────▶  POLICY GATE ─▶ brain/cmd/…         │
                │                           │               ▲                                │
                │                    scores │ proposals     │ proposals                      │
                │                ┌──────────┴───────────────┴──┐                             │
                │                │ LLM on the EDGE DEVICE       │◀── brain/llm/request        │
                │                │ (local, offline)             │──▶ brain/llm/response       │
                │                └──────────────────────────────┘                            │
                └────────────────────────────────────────────────────────────────────────────┘
                                 │ publish
                                 ▼
  Twin / mock actuators ◀── brain/cmd/{type}/{id}  ──▶ twin/ack/{id}  (back to Brain)
  Timeline             ◀── brain/event
```

| Part | Runs on | Speed | Job |
|---|---|---|---|
| **Detection + math model** | Brain host | ms | Turns readings into anomaly scores, incident confidence, priority and action utility |
| **Reflex** | Brain host | ms | Picks the best-scoring rule action immediately; fallback when the LLM is busy or offline |
| **LLM reasoning** | **Edge device** | seconds | Whole-city understanding, merges incidents, reads call text, plans, proposes overrides |
| **Policy gate** | Brain host | ms | Checks every action from reflex and LLM: math score, trust, evidence, cooldown, quarantine |
| **MQTT** | Broker | ms | Single transport for readings, verdicts, commands, acks, events and LLM requests |

**The split between the LLM and the math:** the LLM never invents a number that decides an action. It changes the *picture* (merges incidents, reads severity from a call, proposes a plan), and every proposal it makes is scored by the same mathematical model as the reflex. This keeps decisions **explainable with numbers** and still lets the LLM handle what rules can't.

---

## 3. The local LLM on the edge device

### 3.1 Why a dedicated device
- **No internet dependency:** the demo works on our own hotspot with no cloud.
- **Edge-computing story:** "the city's brain runs on a box in the control room" is a stronger pitch than "we call an API".
- **Isolation:** the LLM can't affect the Brain core if it crashes or slows down; it's another MQTT client.
- **Security:** sensor data and call text never leave the local network.

### 3.2 How it connects
The LLM service is just another MQTT client:

| Topic | Direction | Content |
|---|---|---|
| `brain/llm/request` | Brain → device | City summary + available tools + reflex proposal and its score |
| `brain/llm/response` | device → Brain | Structured JSON: merged incidents, severity hints, proposed actions/plan, justification |
| `brain/llm/status` | device → broker | `online` / `offline` (MQTT Last Will), so the Brain knows instantly when it's gone |

MQTT 5 **correlation data** links each response to its request. **Message expiry** (10 s) drops answers that arrive too late to matter.

### 3.3 Model and device sizing (to measure in week 2)

| Device class | Realistic model | Notes |
|---|---|---|
| NVIDIA Jetson Orin (8–16 GB) | 3–8B, 4-bit quantized | Good balance; GPU acceleration |
| Mini PC / laptop with GPU | 7–8B, 4-bit | Fastest option |
| Raspberry Pi 5 (8 GB) | 1–3B, 4-bit | Works but slow; keep prompts and outputs very short |

**Rules for the prompt so it stays fast on small hardware:**
- Input: compact city summary only (≈ 1k tokens), never raw readings.
- Output: short JSON (≈ 150 tokens), validated against a schema. Free text only in `justification`.
- Temperature 0, fixed prompt version, every request/response logged for replay.
- Runtime: Ollama or llama.cpp server on the device; the model is chosen in `brain.yaml`.

**Week-2 benchmark:** for each candidate model on the real device, measure the time to answer a realistic summary, JSON validity rate, and the B11 result. Choose the smallest model that answers in **≤ 8 s** with **≥ 95 % valid JSON**.

### 3.4 What the LLM does

| Capability | Example |
|---|---|
| **Connect the dots** | Fire call + power spike + jam next door → one electrical fire blocking the main road |
| **Read free text** | *"Smoke from the substation, people trapped"* → fire, high severity, rescue needed |
| **Adjust the model's inputs** | Raises zone exposure ("school in session"), merges two incidents, flags a sensor as doubtful |
| **Plan in steps** | Close inbound roads → open upstream valve → if water still rises in 60 s, dispatch rescue |
| **Propose overrides** | "Reflex chose valve A; valve B avoids flooding the downstream zone" |
| **Explain** | One-line justification on every proposal, shown on the timeline |

---

## 4. The mathematical scoring model

All parameters below are **starting values**, set in `policy.yaml` and tuned on the scenarios.

### 4.1 Sensor anomaly score

For sensor *i* with reading *xₜ*, an exponentially weighted baseline:

```
μₜ = (1−α)·μₜ₋₁ + α·xₜ                α = 0.05
σ²ₜ = (1−α)·σ²ₜ₋₁ + α·(xₜ − μₜ)²
zₜ = (xₜ − μₜ) / max(σₜ, σ_min)
Sₜ = max(0, Sₜ₋₁ + |zₜ| − k)          CUSUM, k = 0.5
sᵢ = min(1, Sₜ / h)                    h = 5        → anomaly score ∈ [0, 1]
```

A single spike barely moves *S*; a sustained shift accumulates quickly. Hard physical limits from the Twin's metadata also set *sᵢ = 1*.

### 4.2 Trust weight from Guardian

| Guardian verdict | τᵢ |
|---|---|
| trusted | 1.0 |
| no verdict / Guardian offline | 0.6 |
| suspect | 0.3 |
| rejected / isolated | 0 |

### 4.3 Incident confidence (noisy-OR fusion)

For incident type *k* in zone *z*, combining evidence sources *i* with weights *wᵢ* (from `rules.yaml`):

```
C(z,k) = 1 − Π_i (1 − wᵢ · sᵢ · τᵢ)            ∈ [0, 1]
```

Why noisy-OR: each independent piece of evidence *raises* confidence, the result stays between 0 and 1, and a rejected sensor (τ = 0) contributes **nothing**, whatever value it reports.

**Thresholds (hysteresis):** open incident at *C ≥ 0.5*, close at *C < 0.25*. High-risk actions also require *C ≥ 0.7* (see 4.6).

### 4.4 Severity and priority

```
σ = clamp( (x − θ_alert) / (θ_max − θ_alert), 0, 1 )     severity from the worst reading
P = C · 4^σ · E_z · (1 + t / T)                           priority
```

| Symbol | Meaning | Value |
|---|---|---|
| θ_alert, θ_max | Alert and maximum levels for that sensor | From Twin metadata |
| 4^σ | Severity weight, 1 (minor) to 4 (critical) | — |
| E_z | Zone exposure: 1 normal, 1.5 high (port, school), 2 critical (hospital) | Config, LLM can raise |
| t, T | Time since the incident opened; urgency time constant | T = 60 s |

### 4.5 Action utility

For each candidate action *a* on incident *j*:

```
U(a, j) = P_j · e_a  −  λ_c · c_a  −  λ_r · r_a · (1 − V_j)  −  λ_s · switch_a
```

| Term | Meaning | Value |
|---|---|---|
| e_a | Expected effectiveness of the action for this incident type | 0–1, `rules.yaml` |
| c_a | Cost: travel time (zone hops) and units used, normalized | 0–1 |
| r_a | Risk class: low 0, medium 0.5, high 1 | `policy.yaml` |
| V_j | Verification strength: `0.6·[fresh trusted verdict] + 0.4·min(1, n_indep − 1)` | 0–1 |
| switch_a | 1 if it reassigns a busy unit (avoids constant switching) | 0/1 |
| λ_c, λ_r, λ_s | Weights | 0.5, 0.8, 0.3 |

An action is a candidate only if **U > 0**.

### 4.6 Allocation: optimal assignment

Each cycle (1 s), build a matrix of **open incidents × available units/actuators** filled with *U* (−∞ where incompatible), and solve the **maximum-weight assignment**:

```
maximize   Σ_j Σ_u  U(j,u) · x(j,u)
subject to Σ_u x(j,u) ≤ demand_j      (each incident gets what it needs)
           Σ_j x(j,u) ≤ 1             (each unit used once)
           x(j,u) ∈ {0,1}
```

Solved exactly with the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`), which takes milliseconds at our scale. Preemption comes out of the model naturally: a busy unit is reassigned only if the gain beats the switching penalty λ_s.

### 4.7 Decision rule (policy gate)

An action from the reflex **or** the LLM is executed only if:

| Check | Low risk | Medium risk | High risk |
|---|---|---|---|
| Utility | U > 0 | U > 0 | U > 0 |
| Confidence | C ≥ 0.5 | C ≥ 0.5 | **C ≥ 0.7** |
| Evidence | — | n_indep ≥ 2 | n_indep ≥ 2 **and** fresh trusted verdict |
| Cooldown / quarantine / whitelist | ✓ | ✓ | ✓ |
| If a check fails | blocked | blocked | **sent to the operator for one-click approval** |

**LLM override rule:** an LLM proposal replaces the reflex choice if `U(llm) ≥ U(reflex) − δ` (δ = 10 % of U(reflex)). If it scores lower than that, it goes to the operator with its justification. So the LLM can bring in what it knows, but every override is accountable in numbers.

### 4.8 Worked example (the numbers on the why card)

**Real flood at the port** (water 2.4 m, alert 2.0 m, max 3.0 m; Guardian healthy):

| Evidence | w | s | τ | w·s·τ |
|---|---|---|---|---|
| Water level | 0.6 | 0.9 | 1.0 | 0.54 |
| Emergency call "flood" | 0.3 | 1.0 | 1.0 | 0.30 |
| Rising trend | 0.3 | 0.8 | 1.0 | 0.24 |

- C = 1 − (0.46 × 0.70 × 0.76) = **0.755**
- σ = 0.4 → 4^0.4 = 1.74 · E_port = 1.5 · t = 0 → P = 0.755 × 1.74 × 1.5 = **1.97**
- Valve upstream: e = 0.8, c = 0.1, high risk, V = 1 → U = 1.97 × 0.8 − 0.05 − 0 = **1.53** → gate: C ≥ 0.7 ✓, 3 sensors ✓, trusted ✓ → **valve opens**

**Same flood, Guardian offline** (τ = 0.6 for all):
- C = 1 − (0.676 × 0.82 × 0.856) = **0.525** → incident opens (≥ 0.5)
- V = 0.4 → U(valve) = 0.525 × 1.74 × 1.5 × 0.8 − 0.05 − 0.8 × 0.6 = **0.57** > 0, but C < 0.7 → **valve held for operator approval**
- Traffic signals (low risk) → **act immediately**, marked `UNVERIFIED`

**Fake flood** (Guardian rejects the water sensor, no call, no trend):
- C = 1 − (1 − 0.6 × 1.0 × **0**) = **0** → no incident; Brain logs "water-level-04 rejected by Guardian: out_of_pattern"

This example goes on a slide as is: the same formula gives the right answer in all three situations.

---

## 5. MQTT: one transport for everything

### 5.1 Topic tree (proposed to the triplet)

| Topic | Publisher | Subscribers | QoS | Retained | Content |
|---|---|---|---|---|---|
| `twin/meta/zones` | Twin | Brain, Guardian | 1 | ✓ | Zones, adjacency, exposure |
| `twin/meta/sensors` | Twin | Brain, Guardian | 1 | ✓ | Sensor list, units, ranges, alert levels |
| `city/{zone}/sensor/{type}/{sensor_id}` | Twin | Brain, Guardian | 0 | — | Readings (high rate; freshest wins) |
| `city/{zone}/call` | Twin | Brain, Guardian | 1 | — | Emergency calls with free text |
| `city/units/{unit_id}` | Twin | Brain | 1 | ✓ | Unit status (free, en route, on scene) |
| `guardian/verdict/{sensor_id}` | Guardian | Brain | 1 | ✓ | Latest verdict per sensor |
| `guardian/quarantine/{device_id}` | Guardian | Brain, Twin | 1 | ✓ | Quarantined devices |
| `guardian/verify/request` → response topic | Brain → Guardian | — | 1 | — | Fresh check before a risky action (MQTT 5 request/response) |
| `brain/cmd/{actuator_type}/{actuator_id}` | Brain | Twin | 1 | — | Actuator commands with a unique `command_id` |
| `twin/ack/{actuator_id}` | Twin | Brain | 1 | — | Command acknowledgement + new state |
| `brain/event` | Brain | Timeline | 0 | — | Events for the timeline and logs |
| `brain/llm/request`, `brain/llm/response` | Brain ↔ edge device | — | 1 | — | LLM traffic |
| `{layer}/status` | each layer | everyone | 1 | ✓ | `online`/`offline` via **Last Will** |

### 5.2 Why MQTT fits our design

| MQTT feature | What it gives us |
|---|---|
| **Pub/sub** | Twin publishes once; Brain, Guardian and the timeline all receive it. No point-to-point wiring |
| **Retained messages** | On (re)connect the Brain instantly gets city metadata, latest verdicts and quarantines |
| **Last Will** (`guardian/status = offline`) | **Guardian-down detection for free**, which triggers our degraded mode (B4) |
| **QoS 1 for commands** | Commands aren't lost; `command_id` makes duplicates harmless (Twin ignores repeats) |
| **MQTT 5 message expiry** | Old readings and late LLM answers are dropped automatically |
| **MQTT 5 request/response** | Clean fresh-verdict request to Guardian, and LLM requests |
| **AsyncAPI** | Documents MQTT topics natively, so it becomes our `INTERFACE.md` backbone |
| **Industry standard for IoT** | Easy for any Phase 2 partner to connect: a client is a few lines in any language |

### 5.3 MQTT security (Security & Trust: 10 points)

| Measure | Detail |
|---|---|
| **TLS** | Broker on port 8883, self-signed CA shared within the triplet |
| **One account per layer** | Twin, Brain, Guardian, LLM device, timeline each log in with their own credentials |
| **ACLs** | Twin may publish only `city/#`, `twin/#`; Guardian only `guardian/#`; Brain only `brain/#`. **A compromised Twin client can't fake Guardian verdicts or Brain commands** |
| **Payload HMAC + timestamp + nonce** | End-to-end integrity on top of TLS, so a message relayed by the broker can still be verified |
| **Schema validation** | Every payload validated before it reaches the core; errors published to `brain/error` with clear codes |
| **Rate limiting** | Per-topic message rate monitored; a device flooding the broker raises an alert to Guardian |

**Who runs the broker:** propose that it runs on our edge device or a triplet laptop on **our own hotspot** (not venue Wi-Fi), started by the root `docker-compose.yml`.

### 5.4 Message example

```json
// topic: city/port/sensor/water_level/water-level-04
{
  "msg_id": "twin-7f3a-000182",
  "time": "2026-11-14T10:22:03Z",
  "sensor_id": "water-level-04",
  "zone_id": "port",
  "type": "water_level",
  "value": 2.4,
  "unit": "m",
  "auth": { "nonce": "9c1e2f", "sig": "base64(...)" }
}
```

```json
// topic: brain/cmd/valve/valve-port-up
{
  "command_id": "brain-cmd-0042",
  "correlation_id": "twin-7f3a-000182",
  "action": "open",
  "params": { "percent": 80 },
  "reason": "flood/port C=0.755 U=1.53",
  "auth": { "nonce": "a81f0c", "sig": "base64(...)" }
}
```

---

## 6. Mocks: input and output

So the Brain can run and be demonstrated completely alone (R1), we mock **both sides** of it:

| Mock | Side | Publishes / subscribes | Modes |
|---|---|---|---|
| **Mock sensors** (Twin input) | Input | Publishes `twin/meta/*`, `city/…/sensor/…`, `city/…/call`, `city/units/…` from scenario files | Normal day, rush hour, flood, fire, accident, compound incident, attack (fake fires), foreign format (B9) |
| **Mock Guardian** | Input | Publishes `guardian/verdict/…`, `guardian/quarantine/…`, `guardian/status`; answers verify requests | `trust_all`, `reject:<sensor>`, `slow:<ms>`, `down`, `flip_flop`, `quarantine:<device>` |
| **Mock actuators** (Twin output) | Output | Subscribes `brain/cmd/#`, publishes `twin/ack/…` and **feeds the effect back** into mock sensors (valve opens → water level falls) | `ok`, `no_ack`, `stuck` (ack but no effect, for B6), `slow` |
| **Mock LLM** | Output/Input | Answers `brain/llm/request` with scripted JSON | `scripted`, `offline`, `malformed`, `slow`, so LLM-dependent tests run without the device |

**Scenario files** (`scenarios/b2_flood.yaml`) describe the timeline of readings, the Guardian mode, the actuator behaviour and the **expected outcome**. `./scenarios/run b2` starts the mocks, runs it, saves `logs/b2-<timestamp>.log` and prints PASS/FAIL. The same scenario can also run against the real partner layers by changing the broker address in `brain.yaml`.

---

## 7. Safety and security summary

| Threat | Defence |
|---|---|
| Spoofed sensor data | Trust weight τ = 0 for rejected sensors → zero contribution to C; independence rule n ≥ 2 |
| Fake-incident flood | Rate guardrail (> 5 new incidents/min → incident storm), priority-only service, fresh verdicts required |
| Prompt injection in call text | Text is labelled as data; LLM output is schema-validated; **every LLM proposal must pass the math score + gate** |
| LLM hallucination | Gate checks every sensor/zone/actuator ID against `twin/meta/*` |
| LLM device offline | Last Will on `brain/llm/status` → reflex continues alone, timeline shows `REASONING: OFFLINE` |
| Guardian offline | Last Will on `guardian/status` → degraded mode (τ = 0.6, high-risk actions need approval) |
| Forged messages on the broker | TLS + per-layer accounts + ACLs + payload HMAC + nonce |
| Command duplicates / replays | `command_id` deduplication, nonce cache, timestamp window |
| Actuator failure | Closed-loop check: expected effect within a deadline, else retry → alternative → alert Guardian |

---

## 8. Demo scenarios (our part of the Test Book)

| ID | Scenario | What the jury sees |
|---|---|---|
| B1 | Calm day + rush hour | C stays below 0.5: Brain does **not** overreact |
| B2 | Real flood at the port | C = 0.76 → valve opens → water drops → resolved |
| B3 | Fake flood | τ = 0 → C = 0: no action, Guardian's reason logged |
| B4 | Guardian offline during a flood | Last Will detected → signals act, valve waits for approval |
| B5 | Fire + accident, one ambulance | Assignment matrix shown; the higher-U incident gets the unit |
| B6 | Stuck valve (mock actuator `stuck`) | No effect → alternative valve → Guardian alerted |
| B7 | Ten fake fires in one minute | Incident storm; units not drained |
| B8 | Best valve quarantined | Assignment skips it, picks the next best U |
| B9 | Foreign Twin format | Works with only the mapping file changed |
| B10 | ⭐ Prompt injection in an emergency call | LLM proposal blocked by the gate (U/evidence fail) |
| B11 | ⭐ Electrical fire blocking a road | LLM merges three incidents; new plan scores higher and replaces the reflex |
| B12 | ⭐ LLM device unplugged mid-flood | Reflex keeps the city safe; nothing unsafe happens |

Every scenario: one command → one log file → PASS/FAIL.

---

## 9. How this maps to the score (50 pts)

| Criterion | Pts | Our answer |
|---|---|---|
| Interoperability & collaboration | 15 | MQTT topic tree documented in AsyncAPI, retained metadata, config-only partner switch, mapping file, shared timeline over MQTT, B9 |
| Prototype functionality | 10 | Edge LLM reasoning, math model, optimal assignment, closed loop; B1, B2, B5, B6, B11 |
| Security & trust | 10 | TLS + ACL + HMAC, gate over the math model, trust weights, Last Will degraded modes, prompt-injection defence; B3, B4, B7, B8, B10, B12 |
| Technical implementation | 5 | Formal model, clean architecture, tests per formula |
| Documentation & code quality | 5 | `INTERFACE.md` + AsyncAPI, why cards with numbers, report in the 6 required subheadings |
| Demonstration | 5 | Live timeline, numbers on screen, unplug-the-LLM moment, fully offline |

---

## 10. Tech stack

| Need | Choice |
|---|---|
| Language | Python 3.11 |
| MQTT | Mosquitto broker (Docker) · `aiomqtt` client (MQTT 5) |
| Data models | pydantic v2 + JSON Schema |
| Math | NumPy · SciPy (`linear_sum_assignment`) |
| LLM on the edge device | Ollama or llama.cpp server · 4-bit quantized model chosen by benchmark · small MQTT bridge service |
| Spec | AsyncAPI 3 (MQTT bindings) |
| Config | YAML: `brain.yaml`, `rules.yaml`, `policy.yaml` (all model parameters), `partner_mapping.yaml` |
| Tests | pytest (unit tests per formula), scenario runner with PASS/FAIL |
| Run | Docker Compose: broker + Brain + mocks with one command |

---

## 11. Plan: about 4 weeks to submission

| Week | Goal | Done when |
|---|---|---|
| **1 · 8–11 Oct** (remaining days) | MQTT foundations | Broker with TLS + ACL running · topic tree agreed with the triplet · mock sensors + mock actuators publish/subscribe · events reach `brain/event` |
| **2 · 12–18 Oct** | Math model + device benchmark | Anomaly, confidence, priority, utility implemented with unit tests · reflex + gate · **LLM device set up, models benchmarked, one chosen** · B1–B3 PASS on mocks |
| **3 · 19–25 Oct** | Full system | Assignment solver, closed loop, Guardian Last Will policy · LLM bridge over MQTT with proposals scored by the math model · B4–B8, B11 · **first joint run with real partners** |
| **4 · 26 Oct–1 Nov** | Hardening | Why cards with numbers on the timeline · prompt-injection tests · B9, B10, B12 · parameter tuning · AsyncAPI final |
| **2–7 Nov** | Deliver | Report, pitch deck, two rehearsals on our hotspot with the edge device · **submit 7 Nov** |

### Changes to the team plan

| Role | New or changed responsibility |
|---|---|
| **P1 · Tech lead** | Broker setup (TLS, accounts, ACLs), topic tree, AsyncAPI spec, triplet agreement on topics |
| **P2 · Detection** | Formulas 4.1–4.4 (anomaly, trust, noisy-OR confidence, severity, priority) with unit tests |
| **P3 · Reflex & resources** | Formulas 4.5–4.6 (utility, Hungarian assignment), closed loop |
| **P4 · LLM reasoning** | **Edge device owner:** setup, model benchmark, MQTT bridge, prompts |
| **P5 · LLM tools & safety** | LLM response schema, override rule (4.7), prompt-injection defence, mock LLM |
| **P6 · Gate & security** | Gate decision table (4.7), payload HMAC, Last Will handling, rate monitoring |
| **P7 · Mocks & demo** | Mock sensors, mock actuators with feedback, mock Guardian, scenario runner, timeline (subscribes `brain/event`) |

---

## 12. Risks

| Risk | Plan B |
|---|---|
| The edge device is too slow for the chosen model | Benchmark in week 2; drop to a smaller model, shorter prompts, or run the LLM on the strongest laptop |
| Device fails on stage | Reflex + math model keep working (B12 is literally this); bring a spare power supply and SD card/disk image |
| Triplet partners don't want MQTT | Unlikely, but a small bridge adapter (WebSocket/REST ↔ MQTT) keeps our core unchanged |
| Broker becomes a single point of failure | Broker in Docker with auto-restart; retained messages restore state on reconnect; spare laptop can host it |
| Model parameters badly tuned | All in `policy.yaml`; scenario runner gives PASS/FAIL after every change |
| Scope too large | Cut operator chat and rule learning first; never cut the gate, the math model or the mocks |

---

## 13. Decisions needed now

1. **Confirm the edge device** (exact model, RAM, GPU or not) so P4 can start the benchmark.
2. **Agree the MQTT topic tree** (section 5.1) with the Twin and Guardian teams this week.
3. **Decide who hosts the broker** (our edge device or a triplet laptop) and who holds the CA and the accounts.
4. **Approve the model parameters** in section 4 as starting values.
5. **Ask the Twin team** to publish `twin/meta/*` as retained messages, unit status, and calls with free text.
