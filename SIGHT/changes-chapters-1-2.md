# What changed: Chapters 1 and 2, old vs new

- **Old Chapter 1:** `chapter1.pdf` (the Google Doc version, 5 pages)
- **New Chapter 1:** `~/Desktop/report/report/chapter1.tex`, LaTeX, 4 pages. PDF: `chapter1-new.pdf`
- **Old Chapter 2:** `report.pdf` / `chapter2.backup-2026-10-12.tex`, 8 pages
- **New Chapter 2:** `~/Desktop/report/report/chapter2.tex`, 8 pages. PDF: `chapter2-new.pdf`

---

## Chapter 1: rewritten from scratch

### Format
| Old | New |
|---|---|
| Google Doc style, different fonts, monospace (code-style) table | LaTeX, same style as Chapter 2 |
| No chapter title, started at "1.1.1" | "Chapter 1: Problem, Context and Requirements" with sections 1.1–1.8 |
| No references at all | 20 references, shared bibliography with Chapter 2 |
| Figure 1 caption with **no image** | Real map of Oued Souhil drawn from OpenStreetMap data |
| 5 pages | 4 pages |

### Section by section

**1.1 The problem** (old 1.1.1 + 1.1.2)
- **Old:** No numbers. "Severe rainfall", "earlier flooding affecting Greater Tunis" with no dates. Contained a note to ourselves: *"Quantitative information… should be supported by reliable historical sources."*
- **New:** Real, cited facts:
  - Floods = 70% of disaster casualties, 60% of losses, about US$40M a year (World Bank).
  - Nabeul, 22 Sep 2018: about 200 mm (up to 225 mm at Beni Khaled), the most since 1995; **6 deaths**, more than 6,000 families affected; US$100M in recovery needs (IFRC, World Bank).
  - January 2026: heaviest rain since 1950, 5 deaths (AFP), Nabeul among the hardest hit.
- **New argument, "The warning existed; acting on it failed":** a warning was issued the day before the 2018 flood, yet people died and some stayed on rooftops. So the weak point is the **last mile**, not the forecast. The World Bank confirms this: Tunisia ranks 13th of 19 MENA countries and has "inefficient procedures for alert dissemination".
- **"Why flash floods need a local approach":** now with evidence. Water can rise in under 1 hour in small basins. In the US, nearly half of flash-flood deaths are vehicle-related; this is labelled as US data. SMS can be delayed by hours, and cell broadcast has no back channel.
- **New "Why now":** the national strategy's Action 8a asks for "simple, low-cost equipment"; national funding goes to INM; the first pilot sites don't include Cap Bon; UN Early Warnings for All targets 2027.
- **Removed:** the Sahel 2020 and Medjerda mentions. There was no verified source for them.

**1.2 Study site** (old 1.1.3)
- **Old:** "proposed as an illustrative site… described setting…" with no reason given, plus a "Methodological note" saying it was not yet checked. Missing figure.
- **New:** four concrete reasons:
  - it's in the governorate hardest hit in 2018 and 2026
  - the RR27 primary road crosses it on a bridge
  - it has a sandy bed with industrial buildings beside it
  - there's an experimental station on the wadi that could be a data partner
- **New map**, with N1, N2 and N3 placed at 3.3, 4.9 and 6.15 km. N3 lands exactly on the RR27 bridge.
- **Removed** at your request: the "no record of past flooding" sentence.

**1.3 Existing solutions** (old 1.2)
- **Old:** four separate blocks with inconsistent headings, no sources, and hedged gaps ("may not"). Two gaps backfired:
  - the LoRaWAN paper was criticised for not predicting floods, but our system doesn't predict either
  - the GSMA SMS system was criticised, but Chapter 2 relies on it
- **New:** one table, **"What it does well / What it leaves open"**, with five rows:
  - the national SMS system (GSMA)
  - the national early-warning programme (INM)
  - Google Flood Hub (real gap: flash floods covered only where there is flood history)
  - low-cost LoRa monitors, now including the closest competitor (Megawati et al.)
  - commercial mass notification (Everbridge)
- **New "The gap" paragraph:** the five things no existing low-cost system combines, with a pointer to Chapter 2's Table 2.1.
- **Removed** at your request: "status not public / we feed it", and the Nepal/India row with its references.

**1.4 Community need** (old 1.1.4)
- **Old:** two paragraphs saying the same thing; vague ("environmental monitoring").
- **New:** one clear sentence stating the need, plus who is affected (drivers, residents and workers, volunteers and the duty officer, Civil Protection and the committee).
- **Removed** at your request: the "will validate with the municipality" sentence.

**1.5 Measurable impact** (old 1.3)
| Old | New |
|---|---|
| Delivery ≥ 90% | Radio delivery ≥ 99% (**now matches Chapter 2, V2**) |
| Ack median < 1 min | Kept, labelled "in drills" |
| False alarms < 5% (of what?) | "No Warning from a single signal group" in replayed scenarios (matches V4) |
| Node uptime ≥ 95% | Replaced by "fault reported within 3 heartbeats" (matches V6) |
| 90 of 100 households (impossible in a table-top demo) | Moved to a separate **"Pilot after the competition"** block |
| — | **New:** detection to beacon ≤ 5 s (matches new V9) |
| — | **New:** escalation within 3 min, offline operation, local repair (match V5, V7, V8) |

**1.6 SDGs** (old 1.4)
- **Old:** SDG 3, 6, 11 and 13 by name only. SDG 6 (drinking water) was a stretch.
- **New:** specific **targets**: **11.5** (disaster deaths), **13.1** (climate resilience) and **1.5** (exposure of vulnerable people), plus Early Warnings for All and the national Action 8a. SDG 3 and 6 were dropped because the verified sources cover only Goals 1, 11 and 13.

**1.7 Inclusion and local actors** (old 1.5)
- **Kept** the strongest parts: multiple channels, volunteers relaying to the elderly, municipal technicians.
- **Added:**
  - beacon for people who cannot hear, siren for people who cannot see
  - Arabic/French SMS
  - an optional assistance flag
  - consent and data protection (Law 2004-63)
  - the evidence that volunteers raise risk awareness better than officials
- **Named actors:** Nabeul municipality; ONPC (24 regional directorates, 196 brigades); the governor's regional committee (Law 91-39); INM; the experimental station.
- **Removed:** jargon a first-time reader wouldn't know (CAP 1.2, gateway details).

**1.8 Requirements (new)**
- **Old:** did not exist, although Chapter 2 opens with "every choice traces back to the six requirements of Chapter 1".
- **New:** table of **R1–R6**, each with its evidence. Chapter 2 now points to something real.

---

## Chapter 2: targeted fixes (same structure, same 8 pages)

### 1. Distance between stations and the central box (§2.1, §2.4, Table 2.3, V2)
- **Old:** radio margin calculated over **1.6 km**, the distance *between stations*. But stations talk to the gateway, whose location was never given.
- **New:**
  - Gateway placed on **a public building near the RR27 bridge** (site to be agreed with the municipality).
  - Real distances from the map: **N1 ≈ 2.5 km, N2 ≈ 1.2 km, N3 < 0.5 km**.
  - Budget computed for **3 km**: free-space loss ≈ 101 dB, margin **43 / 50 / 55 dB** (was 48 / 56 / 61).
  - Added: the stations sit in a valley, so each path gets a **terrain profile** (Radio Mobile) and a walk test. A blocked path gets a taller mast, a slower and longer-range radio setting (SF10), or the second gateway on high ground.
  - Test **V2** now covers each station → gateway path.

### 2. N3 checks every minute (§2.3 Firmware)
- **Old:** all stations checked every **10 min** in Normal and sped up only after the gateway raised the risk level. If the storm hit only near the bridge, or the gateway was down, N3 could react up to 10 min late.
- **New:**
  - **N3 checks every minute, always**, and every 10 s from Warning.
  - A float switch closing **wakes any station instantly** (the low-power co-processor watches the floats every second). Heavy rain wakes N1 the same way.
  - **N3 sends a heartbeat every minute**, so a dead N3 is noticed within **3 min** (was 30 min).
  - **Hardware watchdog** on every station: frozen software restarts by itself.
  - N3 listens continuously (LoRaWAN Class C), now stated explicitly.

### 3. Danger rule fixed (§2.3 Fusion, §2.5, Figure 2.6)
- **Old:** contradiction. §2.3 said "a closed Danger float is accepted even if both other sensors fail", while §2.5 said "Danger needs 2 of 3 methods". "Median" of only two readings didn't mean anything.
- **New, one rule:** **Danger = 2 of 3 *working* sensors.**
  - If the other two are broken, the Danger float **alone** triggers Danger (when in doubt, alarm).
  - If the float says Danger but both working sensors clearly read low, the result is **Warning + "float fault"**, so a float jammed by debris can't wake the town.
  - When the sensors disagree, the **higher** reading counts for alarms. The allowed disagreement grows with depth (30% or 10 cm), so muddy water doesn't cause false "degraded" flags.
  - The ultrasonic reading = median of 5 echoes.

### 4. Restart in the middle of an event (new paragraph, §2.7)
- **Old:** not covered.
- **New:**
  - The gateway **saves every alert's state** (tier, who was contacted, who answered, next deadline) *before* acting.
  - After a restart, alerts **resume where they stopped**, not from the start. Expired deadlines fire at once. People who hadn't answered get one copy marked "resent after system restart". People who answered are not contacted again.
  - The risk level **can never go down because of a restart**.
  - The restart is logged and reported to the duty officer.
  - **N3** remembers Danger across a reset and switches the siren back on within about 1 s.
  - N3's processor has its own power supply, so the siren's current can't make it restart.

### 5. Gateway failure and low battery: maintenance alerts (new paragraph, §2.7; §2.4)
- **Old:** "if the gateway fails, N3 still fires". Nobody was told about the failure.
- **New:** a separate recipient, the **municipal maintenance technician**, for equipment problems only. They're alerted when:
  - a station's battery drops below 30%
  - a station goes silent or a sensor fails
  - the gateway loses mains power (with hours left)
  - the gateway's battery drops below 50% and 25%
- At 25%, the duty officer and Civil Protection are also told that only N3 will protect the crossing.
- Before its battery runs out, the gateway saves everything and shuts down cleanly.
- A dead gateway can't report itself, so it sends a **daily status message**. If it doesn't arrive, someone checks the same day. N3 also shows a **"gateway lost" light**.

### 6. Verification table (Table 2.5): 4 new tests
| Test | What it proves |
|---|---|
| **V9** | Storm at the bridge only, gateway off → beacon on within **5 s** |
| **V10** | Danger rule: float alone with broken sensors → Danger; jammed float → Warning + fault |
| **V11** | Gateway restart mid-escalation → alert resumes; N3 reset → beacon back within 2 s |
| **V12** | Mains off, low battery, gateway off → technician alerted within 5 min; missing daily status detected |

### Not changed yet in Chapter 2 (from the earlier review)
- Pressure sensor setup (barometer vs vented cable)
- Volunteers' radios (Meshtastic) sharing 869.525 MHz with the gateway's downlinks to the stations
- "Reply 1" being ambiguous when two alerts are open
- Sending the log's fingerprint outside the gateway, so edits made on the gateway itself can be detected
- "[Project Name]" placeholder (set once in the preamble)
