# Guardian Proposal vs City Brain Spec: Alignment

**Compared:** the Guardian layer proposal (13-slide deck) with our [`city-brain-interface-spec.pdf`](city-brain-interface-spec.pdf) v0.1 and [`city-brain-inputs-outputs.md`](city-brain-inputs-outputs.md).
**Note:** the deck refers to a full contract in `guardian/INTERFACE.md` v1.1, which we don't have yet. Some points below may already be answered there.

---

## 1. Summary

The two designs are **compatible in spirit**: MQTT for the event stream, HMAC-SHA256 on Twin readings, replay protection, three verdict levels, quarantine after repeated bad readings, a Brain that never acts on rejected data. Several of their choices are **stronger than ours** and worth adopting.

The differences to settle are:
1. **A second transport:** they add JSON-RPC 2.0 over HTTPS/WebSocket for Guardian's tools, with a JWT token per call.
2. **Security level:** they require **mTLS** (client certificates) and **sign verdicts with Ed25519**; our spec has TLS + passwords and HMAC everywhere.
3. **Topic and field names** differ (`twin/events/#`, `event_id`, `suspicious`, `triplet/timeline/guardian`).
4. **Verdict granularity:** per reading (`event_id`) in theirs, per sensor (retained) in ours.
5. **A new input for us:** a **rollback advisory** sent to the City Brain.

---

## 2. What already matches

| Topic | Guardian proposal | Our spec | Status |
|---|---|---|---|
| Event transport | MQTT | MQTT | ✅ |
| Twin signature | HMAC-SHA256 on every event | HMAC-SHA256 (SEC-8) | ✅ |
| Replay protection | `event_id` seen before, `seq` not increasing | `id` seen in last 60 s, 10 s timestamp window | ✅ (they add `seq`) |
| Verdict levels | trusted / suspicious / rejected | trusted / suspect / rejected | ✅ (name differs) |
| Fake flood | Rejected and isolated in < 10 s | Verdict ≤ 10 s after fake reading (GD-4) | ✅ |
| Stuck sensor | Suspicious, not blocked | Suspect counts less in scoring | ✅ |
| Quarantine | Signed, retained order to Twin; Twin refuses commands | Retained quarantine notice; Twin refuses (TW-17) | ✅ |
| Brain behaviour | "City Brain must not act on rejected" | Safety rule: never act only on rejected readings | ✅ |
| Shared timeline | MQTT push + `GET /timeline` | `brain/event` + shared timeline screen | ✅ (topic name differs) |
| Mocks | Runs standalone with mocks | R1 mocks | ✅ |

---

## 3. Differences and what we recommend

| # | Point | Guardian proposal | Our spec | Recommendation |
|---|---|---|---|---|
| 1 | **Verdict delivery** | Broadcast over MQTT **and** `get_trust_verdict` via JSON-RPC | MQTT only | **Use the MQTT broadcast as the main input.** Call `get_trust_verdict` only before a risky action (valve, grid, dispatch) if the latest verdict is missing or old. Keeps the Brain fast if the RPC server is slow. |
| 2 | **Verdict signature** | **Ed25519** on every verdict and order | HMAC (Guardian–Brain key) | **Adopt Ed25519.** It proves the verdict came from Guardian, not from anyone holding a shared key. We need Guardian's **public key**. Update SEC-9/10 for Guardian messages. |
| 3 | **Connection security** | **mTLS** between every layer; certificate must match the role | TLS + username/password (mTLS was MAY) | **Adopt mTLS** (make SEC-6 a MUST). We need a client certificate for `brain` from the triplet CA. |
| 4 | **Tool authentication** | JWT per tool call: one tool, one use, ≤ 120 s | Not in our spec | Accept for the RPC tools. **Ask who issues the tokens** and how the Brain gets one quickly. |
| 5 | **Trust score** | Score 0–1 (rejected < 0.4, suspicious 0.4–0.8, trusted ≥ 0.8) | Fixed weights (suspect 0.3, rejected 0) | **Use their `trust_score` directly** as the weight in our scoring. Better than our fixed values, and nothing to tune on our side. |
| 6 | **Verdict per reading vs per sensor** | Per reading (`event_id`) + `get_device_status` | Per sensor, retained (GD-1) | Accept per-reading verdicts on MQTT; the Brain keeps the latest one per sensor. **Ask for the device status (trusted / suspicious / quarantined) to be also published retained on MQTT**, so a Brain that restarts gets the current state at once. |
| 7 | **Rollback advisory** | Sent to City Brain on quarantine | Not in our spec | **New input for us.** Ask for the format. Proposed Brain behaviour: re-check every open incident and recent decision that used the quarantined device's readings; cancel or revert if no other trusted evidence remains; show it on the timeline. |
| 8 | **Guardian health** | `health` tool: ok / degraded | `guardian/status` with MQTT Last Will (GD-8) | **Ask for the Last Will status topic too.** It tells us instantly when Guardian disconnects; polling `health` is slower. Treat `degraded` as a reason to be more careful. |
| 9 | **Topic names** | `twin/events/#`, `triplet/timeline/guardian` | `city/{zone}/sensor/...`, `brain/event` | Agree on **one joint topic table** (see section 5). |
| 10 | **Field names** | `event_id`, `seq`, `trust_score`, `verdict`, `reason` | `id`, `timestamp`, `source`, `verdict`, `reason` | Align on `event_id` (or `id`) for all layers; add `seq` to Twin messages; use `suspicious` everywhere. |
| 11 | **Reason codes** | Not listed in the deck | Proposed list (Table 13) | Ask for their list; adopt one shared list. |
| 12 | **Quarantine threshold** | After **3 consecutive rejects** | Not specified | Accept. The Brain already ignores each rejected reading before quarantine happens, so there is no gap. |

---

## 4. Impact on our architecture

| Block | Change |
|---|---|
| **① Check incoming messages** | Verify **Ed25519** on Guardian messages (HMAC stays for Twin messages); check `seq` is increasing for Twin messages |
| **Connection** | Brain connects with a **client certificate** (mTLS) |
| **Scoring model** | Use Guardian's **`trust_score`** (0–1) as the reading weight instead of fixed weights |
| **New input** | **Rollback advisory** → re-check incidents and decisions that used the quarantined device |
| **Optional new output** | JSON-RPC client (with JWT) for `get_trust_verdict` before risky actions |
| **Safe mode** | Triggered by Guardian offline (Last Will) **or** `health = degraded` |

The diagram and spec need an update once these points are agreed.

---

## 5. Proposed joint topic table (to agree)

| Content | Publisher | Proposed topic |
|---|---|---|
| Twin readings, calls, events | Twin | `twin/events/{zone}/{type}/{device_id}` (keeps Guardian's `twin/events/#` subscription working) |
| City description | Twin | `twin/meta` (retained) |
| Actuator / unit state + acknowledgements | Twin | `twin/actuator/{id}`, `twin/unit/{id}` |
| Verdicts | Guardian | `guardian/verdict/{device_id}` |
| Device status (trusted / suspicious / quarantined) | Guardian | `guardian/device/{device_id}` (retained) |
| Quarantine order | Guardian | `guardian/quarantine/{device_id}` (retained) |
| Rollback advisory | Guardian | `guardian/rollback` |
| Commands | Brain | `brain/cmd/{actuator_or_unit_id}` |
| Timeline events | Each layer | `triplet/timeline/{twin, guardian, brain}` (Guardian's naming, extended to all) |
| Layer status (Last Will) | Each layer | `{twin, guardian, brain}/status` |

---

## 6. Questions for the Guardian team

1. Can you share `guardian/INTERFACE.md` v1.1 with the JSON examples?
2. On which **MQTT topic** are verdicts broadcast, and what is the exact payload (fields, signature format)?
3. Is a verdict published for **every reading**, or only when it changes?
4. Who **issues the JWT tokens** for the tools, and how does the City Brain get one?
5. Can you also publish **device status** (retained) and a **status topic with Last Will** on MQTT?
6. What is the format of the **rollback advisory**, and what do you expect the City Brain to do with it?
7. What are your **reason codes**?
8. How is `seq` defined: per device, starting at 0, reset on Twin restart?
9. Who generates the **triplet CA** and the client certificates for mTLS?
10. How will the **Guardian public key** (Ed25519) be distributed?
11. Do you want to receive the Brain's alerts (e.g. actuator not responding) as input for actuator-failure detection?

---

## 7. Next steps

1. Send the questions in section 6 to the Guardian team and get their `INTERFACE.md`.
2. Agree the joint topic table (section 5) and field names at the next triplet meeting.
3. Update our spec to v0.2: mTLS, Ed25519 for Guardian, `trust_score`, rollback advisory, joint topics.
4. Update the architecture diagram accordingly.
