# Triplet Meeting: Twin · City Brain · Guardian

**Goal:** leave the meeting with the shared decisions every team needs to start building against the others.
**Rule of thumb:** agree on **what crosses the boundary between layers**. Each team stays free inside its own layer.

---

## What to bring

- Our fixed choices: **MQTT for input and output**, and **mocks of the other layers** (required by R1 anyway).
- A **draft topic list and one example message** for each direction (below), as a starting point to edit together, not a final contract.
- The Phase 1 requirements R1–R4 and the deadlines (7 Nov submission, 14 Nov CSTAM).

**Don't spend meeting time on** our internal design (local LLM, scoring model). The other teams only need to know what the Brain **receives** and **sends**.

---

## 1. Transport: MQTT (10 min)

| To decide | Our proposal |
|---|---|
| Use MQTT for all layers? | Yes: one broker, pub/sub, every team can listen to what it needs |
| Who runs the broker, on which machine? | One machine on **our own router/hotspot** (venue Wi-Fi is not allowed to be relied on) |
| MQTT version | MQTT 5 if all libraries support it, otherwise 3.1.1 |
| Security level | At least one login per team; TLS if time allows (counts for the security score of every layer). Full proposal in **Annex B** |

## 2. Topics and message format (20 min, the most important part)

| To decide | Draft to discuss |
|---|---|
| Topic naming | `city/{zone}/sensor/{type}/{id}` · `city/{zone}/call` · `guardian/verdict/{sensor_id}` · `brain/cmd/{actuator_id}` · `twin/ack/{actuator_id}` |
| Message format | JSON, same base fields everywhere: `id`, `timestamp`, `source`, `zone_id` |
| Units and IDs | One unit per sensor type (e.g. water level in m); one naming style for zones, sensors and actuators |
| Error handling | What a layer does when it receives a malformed message (ignore + log with a clear error) |

**Output of this item:** a shared `INTEGRATION.md` with the topic list and **one example message per topic**. Each team's `INTERFACE.md` points to it.

## 3. What each pair of layers expects from the other (20 min)

*Our side of this is summarised in **Annex A** (City Brain inputs and outputs).*

**Twin → Brain and Guardian**
- List of zones, sensors and actuators (who publishes it, and how).
- Reading frequency.
- Are emergency calls plain text or structured?

**Guardian → Brain**
- Verdict values (e.g. `trusted` / `suspect` / `rejected`) and the reason field.
- Verdict per reading or per sensor?
- How Guardian signals that it quarantined a device.
- How the others know Guardian is down.

**Brain → Twin**
- Command format.
- Does the Twin send an acknowledgement?
- Does the action change later readings (e.g. valve opened → water level falls)?

## 4. Mocks (5 min)

- Each team builds mocks of the other two layers (R1).
- **Agree to build all mocks from the same example messages** in `INTEGRATION.md`, so that when the real layers connect, they already match.
- Optionally share mocks between teams to save time.

## 5. Timeline screen and logs (10 min): required by R2 and R3

| To decide | Proposal |
|---|---|
| Who builds the live timeline screen? | One team, fed by an MQTT topic that every layer publishes events to |
| Common event fields | `timestamp`, `layer`, `type`, short description, and an ID linking reading → verdict → decision → action |
| Log files | One log file per scenario run in `logs/`, same format for all layers |

## 6. Test Book scenarios (10 min)

- The Test Book must cover **all three layers and every interaction**: Twin→Brain, Twin→Guardian, Guardian→Brain, all three together.
- Draft a first list together (e.g. calm day, real flood, fake reading, stuck sensor, layer goes down, real incident + attack at the same time).
- Decide who writes which scenario and how a scenario is triggered (one command or button).

## 7. Repository and way of working (10 min): R4

| To decide | Proposal |
|---|---|
| Repo | `triplet-XX`, one folder per team, CODEOWNERS, root `docker-compose.yml` starting everything with one command |
| Root files | Who owns `README.md`, `INTEGRATION.md`, `TESTBOOK.md` |
| Communication | One shared channel, one contact person per team |
| Sync | One weekly triplet meeting (fixed day and time) + short notes, which are R4 evidence |
| Changing the interface | No silent changes: announce in the channel, update `INTEGRATION.md`, version it |

## 8. Shared dates (5 min)

| Date | Milestone |
|---|---|
| **~15 Oct** | Topics and message format v1 frozen in `INTEGRATION.md` |
| **~22 Oct** | First joint run: one scenario across all three real layers (save the evidence) |
| **~29 Oct** | All Test Book scenarios running together |
| **~1–5 Nov** | Full dry run on our own router; report and pitch drafts |
| **7 Nov** | Submission |
| **14 Nov** | CSTAM: 2-min pitch + 8-min live demo |

Also agree on **demo hardware**: who brings the router or hotspot, which machines run which layer, and where the broker runs. Our edge device must be on the same network.

---

## Decisions checklist: tick before leaving the meeting

- [ ] MQTT confirmed; broker host and machine chosen
- [ ] Topic list agreed (v1)
- [ ] Common message fields and units agreed
- [ ] Verdict format and "Guardian down" signal agreed
- [ ] Command + acknowledgement format agreed
- [ ] Owner of `INTEGRATION.md` named
- [ ] Owner of the timeline screen named
- [ ] First scenario list drafted, owners assigned
- [ ] Repo created, CODEOWNERS set
- [ ] Weekly sync slot + contact person per team
- [ ] Interface freeze date and first joint run date fixed
- [ ] Security rules agreed: one account per layer, topic ACLs, required fields (`id`, `timestamp`, signature), replay window (Annex B)

---

## Annex A: City Brain inputs and outputs

Everything goes over MQTT; exact formats to be agreed at this meeting.

**In one line:** Twin readings + Guardian verdicts → **City Brain** → commands to the Twin actuators + events to the timeline.

### Inputs (what the Brain receives)

**From the Twin**

| Input | What it is | Example |
|---|---|---|
| Sensor readings | Live values per zone: traffic, water level, power load, air quality | `water-level-04, zone port, 2.4 m, 10:22:03` |
| Emergency calls | Reports of incidents (fire, accident, flood…), possibly free text | `zone 3: "smoke from the substation"` |
| City description | List of zones, sensors and actuators (sent once at start) | `zone port: sensors [...], actuators [valve-port-up, ...]` |
| Actuator / unit status | State of valves, signals, units (free/busy), and acknowledgements of our commands | `valve-port-up: opened` · `ambulance-2: on scene` |

**From Guardian**

| Input | What it is | Example |
|---|---|---|
| Trust verdicts | Whether a reading or sensor can be trusted, with a reason | `water-level-04: rejected, out of range` |
| Quarantine / isolation notices | Devices the Brain must not use | `valve-port-main: quarantined` |
| Guardian status | Whether Guardian is up or down, so the Brain switches to a safe mode | `guardian: offline` |

### Outputs (what the Brain sends)

| Output | To | What it is | Example |
|---|---|---|---|
| Actuator commands | Twin | The decided response: dispatch units, change traffic signals, open/close valves, switch the grid | `open valve-port-up 80 %` · `dispatch ambulance-2 to zone 3` |
| Events | Timeline + logs (R2/R3) | Each Brain step with a timestamp: incident detected, decision, action sent, action confirmed, action refused because of an untrusted reading | `10:22:04 flood detected at port → valve opened` |
| *Optional:* alerts | Guardian | e.g. "valve-port-up didn't respond", which helps Guardian detect actuator failures | `actuator_suspect: valve-port-up` |
| *Optional:* Brain status | Everyone | Whether the Brain is up or down | `brain: online` |

Our mocks copy exactly this: mock Twin + mock Guardian on the input side, mock actuators + timeline on the output side.

---

## Annex B: Security of communication between layers

### 1. Network: keep outsiders off
| Measure | Why |
|---|---|
| Our own router / hotspot, WPA2 password, no venue Wi-Fi | Strangers can't even reach the broker |
| Broker exposes only its port (8883 for TLS), firewall on the rest | Smaller attack surface |
| No anonymous access on the broker (`allow_anonymous false`) | By default Mosquitto may accept anyone |

### 2. Encryption: no eavesdropping or tampering in transit
| Measure | Why |
|---|---|
| **TLS** on MQTT (port 8883), one certificate authority shared by the triplet | Messages can't be read or changed on the network (see Annex C) |

### 3. Authentication: know who is talking
| Measure | Why |
|---|---|
| One account per layer (twin, brain, guardian, timeline, edge device) | Every message is tied to a layer |
| Stronger option: client certificates instead of passwords | No password to steal or share |

### 4. Authorization: each layer only does its own job (topic ACLs)
| Account | Can publish | Can subscribe |
|---|---|---|
| Twin | `city/#`, `twin/#` | `brain/cmd/#`, `guardian/quarantine/#` |
| Guardian | `guardian/#` | `city/#`, `twin/#`, `brain/#` |
| Brain | `brain/#` | `city/#`, `twin/#`, `guardian/#` |
| Timeline | nothing | everything (read only) |

A compromised Twin can't fake Guardian verdicts, and nobody but the Brain can send actuator commands.

### 5. Message integrity: prove who sent each message
| Measure | Why |
|---|---|
| Signature on every message: **HMAC** with one secret per pair of layers, or better **Ed25519** signatures with one key per layer | Protects even if the broker or another account is compromised. A signature also proves *which* layer sent it; with an HMAC, either holder of the shared secret could have written it (see Annex C) |

### 6. Replay and freshness: old messages can't be reused
| Measure | Why |
|---|---|
| Timestamp + unique ID (nonce) in every message; reject if older than ~10 s or ID already seen | Stops an attacker replaying an old "open the valve" command |
| `command_id` on every command; the Twin ignores duplicates | MQTT QoS 1 can deliver twice; a duplicate must not act twice |
| MQTT 5 message expiry | Late messages dropped automatically |

### 7. Validation: never trust the content blindly
| Measure | Why |
|---|---|
| Schema check on every message (required fields, types) | Malformed messages never reach decision logic |
| Range and ID checks: known sensor/actuator IDs, physically possible values | Rejects nonsense and invented devices |
| Clear error codes + logging of rejected messages | Asked for by the jury; also shows attacks on the timeline |

### 8. Availability: the system keeps running
| Measure | Why |
|---|---|
| Rate limits and maximum message size (broker + each layer) | A device flooding the network can't take the system down |
| Last Will / heartbeat per layer | Everyone knows instantly when a layer is down and switches to safe mode |
| Broker in Docker with auto-restart; spare machine ready | The broker is a single point of failure |

### 9. Secrets handling
- Passwords, keys and certificates in `.env` / secrets folder, **never committed to Git** (`.gitignore`).
- Each layer only gets the secrets it needs.
- Generate new keys before CSTAM if any were shared in chat.

### What this does *not* cover
These measures stop **outsiders and tampering between layers**. They don't catch a sensor sending false data with a valid signature: the Twin legitimately signs its own readings. That is Guardian's job (trust verdicts), plus the Brain's own checks (no action on rejected readings, corroboration from more than one sensor).

### Priority for 4 weeks
| Must have | Should have | Nice to have |
|---|---|---|
| Own router, no anonymous access, one account per layer, topic ACLs, schema + range validation, timestamp + ID anti-replay, secrets out of Git | TLS, Last Will, rate limits, `command_id` deduplication | Client certificates, Ed25519 signatures, automatic attack alerts on the timeline |

**To agree with all three teams:** account per layer, ACL table, required fields (`id`, `timestamp`, signature), replay window. These only work if every layer applies them.

---

## Annex C: TLS and HMAC in plain words

### TLS (Transport Layer Security)
**What it is:** the protocol that puts the "S" in HTTPS. It creates an **encrypted tunnel** between a client (e.g. the Brain) and a server (the MQTT broker).

**What it protects:**
- **Confidentiality:** someone listening on the Wi-Fi sees only scrambled bytes.
- **Integrity in transit:** if someone changes bytes on the way, the connection detects it.
- **Server identity:** the broker shows a **certificate**. Clients check it was issued by our triplet's certificate authority (CA), so they know they talk to the real broker, not an impostor.
- (Optional) **client identity:** with client certificates, the broker also checks who each layer is.

**How it works, simply:**
1. The Brain connects to the broker and receives its certificate.
2. The Brain checks the certificate against the CA file we all share.
3. Both sides agree on a temporary secret key (key exchange).
4. Everything after that is encrypted with that key.

**Limit:** TLS protects the **pipe**, hop by hop: Twin → broker, then broker → Brain. Inside the broker, the message is readable again. If the broker or an account is compromised, TLS alone doesn't prove where a message came from. That is what HMAC or signatures add.

**In practice for us:** generate a CA + broker certificate once (`openssl`), configure Mosquitto on port 8883, give every team the CA file. Clients add about 2 lines of config.

### HMAC (Hash-based Message Authentication Code)
**What it is:** a short "seal" computed from **the message + a secret key**, attached to the message.

```
seal = HMAC-SHA256(secret_key, message)
```

**How it works:**
1. The **sender** computes the seal with the shared secret and sends `message + seal`.
2. The **receiver** recomputes the seal from the received message with the same secret.
3. If both seals match, the message **was not modified** and **was sent by someone who knows the secret**. If one character changed, the seal is completely different.

**Example:**
```json
{ "id": "twin-000182", "timestamp": "10:22:03", "sensor_id": "water-level-04", "value": 2.4,
  "hmac": "9f2c...e81a" }
```
The Brain recomputes HMAC over everything except the `hmac` field with the Twin↔Brain secret. If it matches, it accepts the message; if not, it rejects it with `E_AUTH`.

**What it protects:**
- **Integrity end to end:** even through the broker, any change is detected.
- **Authenticity:** only a holder of the secret could have produced the seal.

**Limits:**
- Both sides share the **same secret**, so either of them could have produced the message. HMAC can't prove *which* of the two sent it. **Signatures (Ed25519)** fix this: each layer signs with its own private key, and others verify with its public key.
- HMAC alone doesn't stop **replays**: an old message keeps a valid seal. That's why we add a timestamp + unique ID inside the sealed message.
- HMAC does **not** hide the content (no encryption). TLS does that.

### TLS vs HMAC at a glance
| | TLS | HMAC |
|---|---|---|
| Protects | The connection (each hop) | Each message (end to end) |
| Hides content | ✅ Yes | ❌ No |
| Detects modification | ✅ In transit | ✅ Anywhere, even inside the broker |
| Proves sender | The server (and the client with client certificates) | "Someone holding the shared secret" |
| Stops replay | ❌ No (needs timestamp + ID) | ❌ No (needs timestamp + ID) |
| Effort | Certificates + broker config | A few lines of code per message + shared secrets |

**They complement each other:** TLS keeps outsiders from reading or changing traffic, HMAC (or signatures) proves each message is genuine and unchanged, and timestamp + ID stops replays.
