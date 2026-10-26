# City Brain Layer: Improvement Options for Phase 1

**Context:** Phase 0 proposal (section 4, City Brain) reviewed against the *Phase 1 Specifications* (24 Sep → 14 Nov 2026).
**Phase 1 submission:** 7 November 2026 · **CSTAM pitch + demo:** 14 November 2026

---

## 0. What Phase 1 changes about our Brain design

| Phase 0 assumed | Phase 1 actually says | Impact on Brain |
|---|---|---|
| A frozen contract supplied by the organizers | **No imposed contract.** The triplet picks the architecture and protocols | Our schema is only a proposal. Brain has to adapt to whatever the triplet agrees on, and the jury scores "how easily it connects to *other* teams" |
| Re-pairing more than once | Same triplet until CSTAM, then a reshuffle for Phase 2 | Interoperability with strangers still decides who makes the finals |
| Nothing on mocks or logs | **R1–R4**: run alone with mocks of Twin and Guardian, one-page `INTERFACE.md`, config-driven partner addresses, one trigger → one log, live timeline, collaboration evidence | These are new deliverables our design doesn't cover yet |
| Scoring unknown | Interop **15**, Security & Trust **10**, Prototype **10**, Tech **5**, Docs **5**, Demo **5** | 25 of the 50 points come from interop and trust, not from how smart the Brain is |
| — | Report needs "**how it picks an actuator**" | Our design maps each incident to exactly one actuator, so we have nothing to say here yet |

### Gaps in the current Brain design

1. **No behaviour defined for when Guardian is down or slow.** Yet one of the brief's example scenarios is "one layer goes down and the city keeps running".
2. **The fallback contradicts itself.** When the LLM is unavailable it "dispatches the most conservative action". For a valve or a grid switch, it isn't clear what "conservative" means.
3. **The decision cache (Tier 2)** is hard to demo, can go stale, and adds little with only 4 incident types.
4. **No resource limits, priorities or competing incidents.** That is where a Brain can actually show intelligence.
5. **No check that an action worked.** The incident goes `dispatched → resolved` without verifying that the water level actually dropped.
6. **Brain has no security of its own.** An attacker could flood fake incidents to exhaust our units.
7. **Thresholds are hard-coded per zone**, which breaks when we connect to a different Twin.

---

## 1. Decision engine core

| Option | Pros | Cons |
|---|---|---|
| **A1. Keep the 3-tier cascade (rules → cache → LLM)** | Already written, so the report text exists. Sounds sophisticated | The cache tier is hard to justify. An LLM on the action path adds latency, non-determinism and a dependency on stage Wi-Fi |
| **A2. Rules + LLM, drop the cache** | Simpler and easier to explain | The LLM still decides actions, so the safety story stays weak |
| **A3. Rules + utility scoring/allocator, with the LLM as a non-blocking advisor** ⭐ | Deterministic and explainable. Gives a real answer to "how it picks an actuator". The LLM adds an "analyst note" on the timeline without being able to cause harm. Works offline | Needs a scoring function and some tuning |
| **A4. State machine / behaviour tree per incident** | Clean lifecycle with escalation steps (warn → act → escalate). Easy to show visually | More code. Overkill if there are few incident types |
| **A5. LLM agent with MCP tool-calling as the main decider, plus rule guardrails** | Impressive demo and flexible | Non-deterministic, slow, needs internet, hard to defend under jury questions. Risky for the 10 security points |
| **A7. Reflex rules + LLM reasoning agent, with every action passing a deterministic policy gate** ⭐ *(revised pick)* | The LLM is the real intelligence: sees the whole city, plans, overrides rules, reads call text. Still safe offline and under attack | More work than A3. Needs prompt-injection handling and a latency test of the local model |
| **A6. Trained ML classifier** | Can handle fuzzy patterns | No real data, so it overfits our own mock. Hard to explain. Same problem Phase 0 already rejected for Guardian |

## 2. Incident detection

| Option | Pros | Cons |
|---|---|---|
| **B1. Threshold + persistence (current)** | Trivial and transparent | Brittle across different Twins. Slow to react. Can't tell rush hour from a jam without hand-tuning |
| **B2. Change detection (EWMA/CUSUM) + multi-sensor evidence score** ⭐ | Adapts to any Twin's baseline. Produces a confidence value per incident. Corroboration gives some protection against spoofing | Needs a warm-up period. Slightly harder to explain |
| **B3. Zone adjacency graph (spatial correlation)** | Detects spreading floods and propagating jams. Allows predictive actions like pre-closing the next valve | Needs the Twin to expose its topology (or a config file describing it) |
| **B4. Auto-calibration from a Twin discovery endpoint (`/zones`, `/sensors` with ranges and units)** ⭐ | Zero hard-coding, which the jury explicitly checks | Depends on the triplet agreeing to expose it. Fall back to a config file |

## 3. How Brain uses Guardian (Security & Trust, Interop)

| Option | Pros | Cons |
|---|---|---|
| **C1. Synchronous pull per reading (current `get_trust_verdict`)** | Simple and exact | Brain's latency becomes Guardian's latency. If Guardian is down, Brain stalls |
| **C2. Guardian pushes verdicts; Brain keeps a local trust table (sensor → trust, TTL)** | Fast and decoupled. Survives short Guardian outages | Brief windows where the verdict is stale |
| **C3. Guardian as an inline proxy (Twin → Guardian → Brain)** | Brain never sees bad data | Guardian becomes a single point of failure. The demo goes dark if Guardian crashes. It also hides *why* data was dropped |
| **C4. Hybrid: subscribe to verdicts, plus a blocking pull only before high-impact actions** ⭐ | Best of C1 and C2. A natural story: "verify before irreversible actions" | Two code paths |
| **C5. Trust as a weight, not a yes/no gate** (evidence × trust) ⭐ | More nuanced. Several "suspect" sensors can still add up to a real incident | Must stay easy to explain |
| **C6. Policy by risk class when Guardian is unavailable** ⭐ | Answers the "layer goes down" scenario. Low-risk actions (traffic signals) go ahead flagged `UNVERIFIED`. High-risk actions (valve, grid, dispatch) need 2+ independent sensors or operator approval | Needs a small policy table |

## 4. Interop architecture (15 points)

| Option | Pros | Cons |
|---|---|---|
| **D1. Push the Phase 0 contract (REST + WebSocket + HMAC + MCP) onto the triplet** | Already designed | Partners may resist it. MCP is unfamiliar to them |
| **D2. MQTT + topic hierarchy (`city/{zone}/{sensor}`)** | Realistic IoT standard. Pub/sub fits three layers. Easy to plug into other teams | Needs a broker, though it's one Mosquitto container in docker-compose |
| **D3. Hexagonal design: core logic + swappable adapters (WS / MQTT / REST / MCP) chosen by config** ⭐ | Matches exactly what the jury lists ("separate logic from how it talks to partners"). Makes the Phase 2 reshuffle painless | Some upfront structure |
| **D4. AsyncAPI (streams) + OpenAPI (commands) + JSON Schema, optionally a CloudEvents envelope** ⭐ | Standard, machine-readable, and works as the backbone of `INTERFACE.md` | Spec writing takes time |
| **D5. A field/unit mapping file** (`partner_mapping.yaml`) | Connects to a foreign Twin without code changes. Strong evidence of interop | Small extra layer |
| **D6. Keep MCP as an optional adapter only** | Keeps the AI-native angle | Don't make it the main path |

## 5. Actuation and resource allocation (Prototype, report "how it picks an actuator")

| Option | Pros | Cons |
|---|---|---|
| **E1. Fixed one-to-one mapping (current)** | Simple | Nothing to show. Fails when several incidents compete |
| **E2. Resource pool + priority queue** (severity × exposure × age), nearest free unit, preemption ⭐ | Visible intelligence. Handles "fire and flood at once" well | Needs unit state from the Twin, or a model of it inside Brain |
| **E3. Optimal assignment (Hungarian / OR-Tools)** | Mathematically defensible | Overkill at this scale. Takes time |
| **E4. Closed-loop check: expect an effect within T seconds, else retry with an alternative actuator and report a suspected actuator failure to Guardian** ⭐ | Makes the lifecycle real. Creates a good Brain↔Guardian scenario | Needs a Twin whose physics responds to actions |
| **E5. Escalation ladder** (signal retime → reroute → dispatch police) | Proportional responses avoid overreacting on a calm day | Must be defined for each incident type |

## 6. Brain's own security (10 points)

| Option | Pros | Cons |
|---|---|---|
| **F1. Schema validation + authentication on every input (HMAC or mTLS/JWT)** ⭐ | Explicitly in the jury checklist | Low cost, so no real downside |
| **F2. Action guardrails: whitelist, per-zone cooldown, global dispatch budget, rate limit** ⭐ | Stops attackers from draining resources with fake incidents. Easy to demo | Needs tuning so real incidents aren't blocked |
| **F3. Refuse to command devices Guardian has quarantined** ⭐ | Matches the brief's example scenario directly | Needs a quarantine feed |
| **F4. Human-in-the-loop approval for high-impact actions** (button on the dashboard) | Strong safety story. Good on stage | Slows the demo. Needs a UI |
| **F5. Signed, append-only decision log (hash-chained)** | Tamper-evident audit trail. Nice extra for the security score | Extra work, low visibility |

## 7. Observability and demo (R2, R3, 5 demo points)

| Option | Pros | Cons |
|---|---|---|
| **G1. Structured JSONL events with `correlation_id` (reading → verdict → decision → action)** ⭐ | Feeds both the timeline and the R2 logs. Doubles as proof of "explainable" | Must be agreed with the triplet |
| **G2. Shared timeline UI (simple web page consuming all three event streams)** | Required by R3 anyway | Someone in the triplet must own it. Volunteer, since it gives us control of the demo |
| **G3. Grafana + Loki** | Polished with little code | Heavy. More setup risk on stage |
| **G4. A "why" card per decision** (rule hit, evidence, trust, alternatives rejected) ⭐ | Answers jury questions live | Small effort |

## 8. Mocks and testing (R1, Test Book)

| Option | Pros | Cons |
|---|---|---|
| **H1. Scripted mock Twin (replays scenario files)** ⭐ | Deterministic demo. Required by R1 | No physics |
| **H2. Mock Guardian with modes: trust-all / reject / slow / down / flip-flop** ⭐ | Lets us prove Brain behaves correctly when a partner fails. The spec says we keep our points if we show this with mocks | — |
| **H3. Contract tests (schemathesis / Pact) in CI** | Proves interop objectively | Setup time |
| **H4. KPIs per scenario** (time to detect, false dispatches, units used) | Hard numbers for the report | Needs a metrics script |

## 9. Scope extensions (choose 0–2)

- **Power overload → grid switching / load shedding.** Uses a sensor type we currently ignore.
- **Air quality → reroute traffic away from a polluted zone.** Shows actions that work across domains.
- **Predictive action** (flood trend → pre-open a valve upstream).
- **Calm-day scenario as an explicit test.** Zero dispatches is the success criterion.

---

## Recommended package

**A7 (revised from A3) + B2/B4 + C4/C5/C6 + D3/D4/D5 + E2/E4 + F1–F3 + G1/G4 + H1/H2**, and drop the decision cache.

The pitch becomes: *"An AI-driven Brain, behind a safety gate it cannot bypass, that weighs evidence by trust, allocates limited resources, verifies its own actions, stays safe when Guardian is down, and plugs into any Twin through config."* Each part of that sentence maps to a scoring line.

## Kick-off plan (submission 7 Nov, about 4.5 weeks)

| When | Work |
|---|---|
| **Week 1 (5–11 Oct)** | Agree protocol and envelope with the triplet (D4) and draft `INTERFACE.md`. Set up the hexagonal skeleton with mock Twin and mock Guardian (H1, H2). Define the JSONL event format (G1) and offer to own the timeline |
| **Week 2 (12–18 Oct)** | Detection (B2) + rule engine + trust weighting (C5) + guardrails (F2). First scenario script and log (R2) |
| **Week 3 (19–25 Oct)** | Allocator (E2) + closed-loop check (E4) + Guardian-down policy (C6). First joint run with real partners, with evidence saved for R4 |
| **Week 4 (26 Oct–1 Nov)** | LLM advisor (optional), why-cards, KPIs, Test Book, contract tests |
| **Last days (2–7 Nov)** | Report (the Brain part uses the six required subheadings), pitch deck, rehearse with a local hotspot |
