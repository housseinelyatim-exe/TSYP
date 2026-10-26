# Team 5, Person A: Safety + commands

**People:** 1 · **Code:** `brain/src/output/` · **Read first:** [`00-overview-and-contracts.md`](00-overview-and-contracts.md), [`../city-brain-interface-spec.pdf`](../city-brain-interface-spec.pdf) sections 4, 8, 9 · **Partner:** Person B, timeline + logs ([`05b-output-timeline-logs.md`](05b-output-timeline-logs.md))

## 1. Mission

You are the **last gate of the City Brain**. You apply the **safety rules** no score can override, sign and send commands to the Twin, and check they were acknowledged.

## 2. You own / you don't own

| You own | You don't own |
|---|---|
| Safety rules, ② signing, publishing `brain/cmd/…`, tracking acknowledgements, retries, alerts | Choosing the action (Math) |
| The `brain/event` messages for your steps | The timeline screen and log files (Person B) |
| | Checking incoming messages (Input) |

## 3. Your inputs and outputs

| Direction | Topic | Content |
|---|---|---|
| In | `brain/internal/decision` | Chosen actions to execute |
| In | `brain/internal/quarantine/#`, `trust/#`, `layer-status/#` | For the safety rules |
| In | `brain/internal/meta` | City description (allowed actions per device, S5) |
| In | `brain/internal/ack` | Twin acknowledgements |
| Out | `brain/cmd/{actuator_or_unit_id}` | **Signed** commands (external, spec BR-1) |
| Out | `brain/internal/outcome` | sent / refused / acknowledged / failed |
| Out | `brain/event` | `action_refused`, `command_sent`, `command_acknowledged`, `command_failed` |
| Out | `brain/alert` (optional, if agreed with Guardian) | e.g. actuator not responding |

## 4. Safety rules

Applied to **every action** of a decision, in this order. If one fails, the action is **refused** (never silently): publish `outcome: refused` with the rule in `detail`, and a `brain/event` `action_refused`.

| # | Rule | Refused when | Example |
|---|---|---|---|
| S1 | Quarantine | Target device is quarantined | `valve-port-main` quarantined → refused |
| S2 | Rejected evidence | All evidence of the incident comes from rejected readings | Fake flood → refused |
| S3 | Two sensors for risky actions | Valve, grid or dispatch with fewer than **2 different sensors** agreeing | One water sensor only → refused (waits) |
| S4 | Cooldown | Same action on the same device within **60 s** | Signal switched again after 10 s → refused |
| S5 | Allowed action | Action not in the device's allowed actions (city description) | `open` on a traffic signal → refused |
| S6 | Guardian offline | Risky action while Guardian is offline, unless S3 is met with **2 different sensor types** | — |

Rules and values in `config/safety.yaml`. Each rule has its own unit test.

## 5. Commands and acknowledgements

1. Build the command body (spec BR-1) with a new `id` (e.g. `brain-000042`) and the `correlation_id`.
2. **Sign:** envelope `{"v":1,"body":"<text>","hmac":"<HMAC-SHA256 with the Brain–Twin key>"}`.
3. Publish on `brain/cmd/{target_id}`, QoS 1. Outcome `sent`.
4. Wait for the acknowledgement (`brain/internal/ack` with `correlation_id` = command id):
   - `done` within **2 s** (configurable; real hardware may need more) → outcome `acknowledged`
   - `rejected` / `failed` → outcome `failed` with the reason
   - nothing after 2 s → **retry once with the same id**, then outcome `failed` + `brain/alert` `actuator_not_responding`
5. Optional (week 3): check the **effect** (valve opened → water stops rising within 30 s); if not, outcome `failed` so Math picks another action.

Outcome format: see `00-overview-and-contracts.md` section 3.

## 6. Tasks

### Week 1 (15–19 Oct)
- [ ] Signer (envelope + HMAC), verified with the spec's test vector; publish a test command to the mock actuators
- [ ] `config/safety.yaml` and outcome format (with Person B)

### Week 2 (20–26 Oct)
- [ ] Safety rules S1–S6, acknowledgement tracking, retry, outcomes
- [ ] **Sun 26 Oct:** end-to-end run on mocks, visible on the timeline

### Week 3 (27 Oct – 2 Nov)
- [ ] Effect check (optional), `brain/alert`
- [ ] Joint run with the real Twin: commands verified by their actuators

### Week 4 (3–7 Nov)
- [ ] Report section: safety rules, signing, acknowledgements

## 7. Done when

- [ ] Each safety rule refuses its case and lets the valid case through (unit tests)
- [ ] Scenarios B3 (fake flood), B4 (Guardian offline), B8 (quarantined valve): the right action refused, with the reason published as an event
- [ ] Commands accepted by the mock actuators (valid HMAC); duplicate not executed
- [ ] Missing ack → retry → `command_failed` + alert

## 8. Who you work with

| Who | About |
|---|---|
| **Person B (timeline)** | Event names and content for your steps; refused / failed display |
| **Math** | Decision format; refused / failed outcomes so they can re-decide |
| **Input** | Shared MQTT client; acks, quarantine, layer status |
| **Mock** | Mock actuators that verify the HMAC and send acks |
| **Team lead** | Brain–Twin key, `brain/alert` agreement with Guardian |

## 9. Risks and tips

- Never block a command forever waiting for an ack: always time out.
- Test the signer against the Twin team's verifier **early**, not at the joint run.
- A refused action must always be visible (outcome + event), never dropped.
