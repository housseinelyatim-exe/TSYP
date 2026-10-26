# City Brain: Team Plan (7 people)

**Based on:** [`city-brain-phase1-proposal.md`](city-brain-phase1-proposal.md)
**Deadline:** submission 7 Nov 2026 · CSTAM 14 Nov 2026

---

## 1. Roles

Each person **owns** one module (they write it and are responsible for it) and has a **buddy** who reviews their PRs and can take over if they're absent.

| # | Role | Owns | Buddy | Profile |
|---|---|---|---|---|
| **P1** | **Tech lead & integrator** | Repo skeleton, shared data models, ports/adapters, specs (AsyncAPI/OpenAPI/JSON Schema), `INTERFACE.md`, CI, merges, **triplet coordination** (R4) | P6 | Strongest overall dev, good communicator |
| **P2** | **Detection & fusion** | Discovery/config loading, per-sensor EWMA/CUSUM, evidence fusion with trust weights, incident lifecycle | P3 | Comfortable with maths and stats |
| **P3** | **Reflex & resources** | `rules.yaml` + escalation ladder, utility score, resource allocator (priority queue, preemption), closed-loop action checks | P2 | Algorithms, careful with edge cases |
| **P4** | **LLM reasoning** | Agent loop (5 s + event triggers), city summary builder, prompts, local model setup (Ollama), plans and overrides | P5 | Has used LLM APIs or agents before |
| **P5** | **LLM tools & safety** | MCP tools (read + action), structured JSON output, prompt-injection defence, operator chat, rule learning from logs | P4 | Python + security mindset |
| **P6** | **Policy gate & security** | Policy gate (every action), risk classes, HMAC/nonce/validation, error codes, guardrails, Guardian integration (trust table, fresh checks, down policy, quarantine) | P1 | Rigorous, likes security |
| **P7** | **Mocks, scenarios & demo** | Mock Twin (+ foreign-format mode), mock Guardian (modes), scenario runner + logs (R2), timeline UI (R3), KPIs, Test Book | P1 | Frontend + scripting. **Good entry role for a less experienced member** |

**Assigning people:** the two LLM roles (P4, P5) and the gate (P6) are the most critical for the score. Put your strongest people there and on P1.

### How the modules connect

```
   P7 mocks ──▶ P1 adapters ──▶ P6 validation ──▶ P2 detection ──▶ P3 reflex ─┐
                                                       │                     ▼
                                                       └──▶ P4/P5 LLM ──▶ P6 GATE ──▶ P1 adapters ──▶ Twin
                                                                               │
                                         P7 timeline ◀── events from everyone ◀┘
```

**Contracts that must be frozen early** (otherwise people block each other):

| Contract | Owner | Needed by | Deadline |
|---|---|---|---|
| Shared data models (`Reading`, `Verdict`, `Incident`, `Action`, `Event`) | P1 | Everyone | **Wed 8 Oct** |
| Port interfaces (`SensorSource`, `VerdictSource`, `ActuatorSink`, `EventSink`) | P1 | P2, P6, P7 | **Wed 8 Oct** |
| Gate API: `gate.check(action) → approved / rejected(reason)` | P6 | P3, P4, P5 | **Thu 9 Oct** (stub that approves everything is fine at first) |
| Event format (JSONL + `correlation_id`) | P1 + P7 | Everyone | **Thu 9 Oct** |
| City summary format given to the LLM | P4 | P2, P3 (they provide the data) | **Mon 13 Oct** |

---

## 2. Week-by-week tasks

### Week 1 · 5–11 Oct: Foundations

| Who | Tasks | Done when |
|---|---|---|
| P1 | Repo skeleton in `brain/`, data models, ports, `brain.yaml`, Docker; meet the triplet to agree protocol + message format | Brain starts with mocks via one command |
| P2 | Discovery client + `city.yaml` fallback; EWMA baseline per sensor | Prints a per-sensor anomaly score from mock data |
| P3 | Draft `rules.yaml` for 4 incident types × 3 severities; utility score function + unit tests | Rules load and return candidate actions |
| P4 | Install Ollama, test 2–3 local 7–8B models for JSON/tool calling and latency on the demo laptop | Short comparison table, model chosen |
| P5 | Draft action/read tool schemas; first prompt-injection test cases (10 malicious call texts) | Tool schemas reviewed by P4 and P6 |
| P6 | Gate stub + HMAC/timestamp/nonce validation + error codes | Bad messages rejected with the right code in tests |
| P7 | Mock Twin replaying a scenario file; mock Guardian with `trust_all` and `down` modes; events written to `logs/` | Scenario B1 file plays end to end |

### Week 2 · 12–18 Oct: Reflex, gate, first LLM call

| Who | Tasks | Done when |
|---|---|---|
| P1 | WebSocket adapter for real partners; AsyncAPI/OpenAPI draft; `INTERFACE.md` v1; CI (lint + tests) | CI green on every PR |
| P2 | CUSUM, evidence fusion with trust weights, hysteresis, incident lifecycle | Flood detected in B2; nothing in B1 |
| P3 | Reflex decisions wired to the gate; per-zone cooldown handled with P6 | B2 reflex opens the valve |
| P4 | City summary builder; agent loop calling one tool through the gate | LLM proposes an action that appears in the log |
| P5 | Read tools (`get_zone_history`, `ask_guardian`); structured-output validation | Malformed LLM output rejected cleanly |
| P6 | Real gate: risk classes, whitelist, ID checks, independence rule; Guardian trust table | B3 fake flood suppressed with Guardian's reason |
| P7 | Mock Guardian `reject`/`slow`/`flip_flop`; scenario runner `./scenarios/run <id>`; timeline v1 (reads events) | B1–B3 run with one command each and show on the timeline |

### Week 3 · 19–25 Oct: Full intelligence + first joint run

| Who | Tasks | Done when |
|---|---|---|
| P1 | **Joint run with real Twin and Guardian partners**; collect R4 evidence (screenshots, logs, notes) | One scenario runs across all three real layers |
| P2 | Zone adjacency (spreading floods); support P4 with trend data in the summary | Summary includes trends and neighbours |
| P3 | Allocator with priority queue + preemption; closed-loop checks + alternative actuator | B5 and B6 pass |
| P4 | Plans with conditions, reflex overrides with justification, event-triggered cycles | B11 passes (3 signals → 1 incident) |
| P5 | Action tools (`propose_plan`, `cancel_action`, `reprioritise`); gate rejection fed back to the LLM; call-text parsing | LLM adapts after a gate rejection |
| P6 | Fresh verdict before risky actions; Guardian-down policy; quarantine; incident-storm guardrail | B4, B7, B8 pass |
| P7 | Why card display on the timeline; mock Twin foreign-format mode | Click on an action → why card |

### Week 4 · 26 Oct–1 Nov: Hardening + polish

| Who | Tasks | Done when |
|---|---|---|
| P1 | Final specs; contract tests (schemathesis); B9 with the mapping file; code review sweep | B9 passes with config only |
| P2 | Tune thresholds on the real partner Twin; KPIs: detection time, false alarms | KPI table filled |
| P3 | Edge cases: no unit available, all valves quarantined; KPIs: units used | No crash in any scenario |
| P4 | Prompt tuning on all scenarios; `REASONING: OFFLINE` handling | B12 passes |
| P5 | Prompt-injection hardening; operator chat; rule learning (proposals only) | B10 passes on all 10 malicious texts |
| P6 | Security review of the whole Brain; pen-test the gate with P5 | Security checklist done |
| P7 | Test Book (all scenarios in the required format); timeline polish; record backup video of the demo | Test Book complete; video saved |

### 2–7 Nov: Deliver

| Who | Tasks |
|---|---|
| P1 | Final merge, tag the release, triplet README / INTEGRATION.md with partners |
| Everyone | Write their report section (see section 3), review someone else's |
| P1 + P4 + P7 | Pitch deck (~5 slides) |
| Everyone | **Two full rehearsals** on our own hotspot, including one with the LLM forced offline |

---

## 3. Report ownership (Brain part: 5 pages, 6 required subheadings)

| Subheading | Writer | Reviewer |
|---|---|---|
| Role and goals | P1 | P3 |
| Architecture | P1 + P4 | P2 |
| Tech stack and why | P4 | P6 |
| Interfaces in/out | P7 | P1 |
| Security measures | P6 + P5 | P4 |
| Known limitations | P2 + P3 | P1 |

Shared triplet parts: **Part 0 (integration)** → P1 with the partner leads · **Part 4 (Test Book)** → P7 · **Part 5 (collaboration)** → P1.

---

## 4. Demo day roles (14 Nov)

| Role | Who |
|---|---|
| Pitch (2 min) | P1, or the best speaker |
| Demo driver (runs scenarios) | P7 |
| Narrator (explains the timeline live) | P4 |
| Network + backup (hotspot, local fallback, video) | P6 |
| Q&A experts | P2 (detection), P3 (decisions), P5 (LLM safety) |

---

## 5. How we work together

| Practice | Rule |
|---|---|
| **Daily stand-up** | 10 min, or async in the group chat: done yesterday / doing today / blocked by |
| **Team sync** | Twice a week (e.g. Mon + Thu, 45 min): demo progress, unblock, re-plan |
| **Triplet sync** | Once a week with the Twin and Guardian teams, led by P1. Keep notes (R4 evidence) |
| **Git** | One branch per task, PR into `main`, **buddy reviews before merge**, CI must be green. Only commit inside `brain/` (CODEOWNERS) |
| **Task board** | GitHub Projects: one card per row of section 2, with owner and due date |
| **Definition of done** | Code + tests + runs in a scenario + event visible on the timeline |
| **Stuck > half a day?** | Tell the buddy, then P1. Don't stay blocked silently |

---

## 6. If the team is smaller or someone drops out

| If we lose… | Then… |
|---|---|
| P5 | P4 takes the LLM tools; operator chat and rule learning are cut |
| P7 | P1 takes mocks; the timeline becomes a simple log viewer |
| P2 or P3 | The buddy merges both roles; zone adjacency and preemption are cut first |
| P6 | **Don't cut**. P1 takes the gate; the gate is what makes the LLM safe |
