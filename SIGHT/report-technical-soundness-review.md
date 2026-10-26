# Review: report.pdf, Chapter 2 "Technical Soundness" (Phase 1)

**Reviewed:** `report.pdf` (9 pages, Chapter 2 + bibliography), 2026-10-12
**Verdict:** Strong and honest. The architecture is sound, the numbers check out, and the "silence is never safe" / "human decides" principles show up in the design itself, not just in the wording. About a dozen technical gaps remain. A judge with field or RF experience would spot several of them. Four are significant: the link budget uses the wrong distance, N3 can react up to 10 min late in Normal mode, the pressure sensor physics needs work, and the float switch rule contradicts the Danger rule. Each one needs only a sentence or two, or one row in a table.

---

## 1. What I checked and confirmed

| Claim | Check | Result |
|---|---|---|
| 16 B payload → 29 B on air | LoRaWAN overhead MHDR+DevAddr+FCtrl+FCnt+FPort+MIC = 13 B | ✅ |
| Airtime 66.8 / 411.6 / 1646.6 ms (SF7/10/12) | Semtech formula, CR4/5, 8-symbol preamble, LDRO at SF12 | ✅ exact |
| Min interval at 1 % (6.7 / 41.2 / 164.7 s) | airtime × 100 | ✅ |
| Sensitivity −124.5 / −132 / −137 dBm | −174 + 10log(125k) + 6 NF + SNR limit (−7.5/−15/−20) | ✅ |
| Max path loss 143.5 dB at SF7 | 14 + 2 + 5 − 2 + 124.5 | ✅ |
| FSPL ≈ 95 dB at 1.6 km, 868 MHz | 32.44 + 20log(1.6) + 20log(868) = 95.3 | ✅ |
| Storm mode at SF8 every 30 s fits 1 % | SF8 airtime ≈ 123 ms → 12.3 s minimum | ✅ |
| Node energy: ~9 mAh/day normal, ~364 mAh/day storm | 144 vs 8640 wake-ups × 1.5 s × 100 mA + sleep + TX | ✅ |
| 6 Ah → ~13 storm days | 6000 / 364 ≈ 16.5, ≈13 at ~80 % DoD | ✅ |
| 5 W panel → ~4 Ah/day | 5 W × 4.5 h = 22.5 Wh / 3.2 V ≈ 7 Ah, ~4 Ah after losses | ✅ (state the efficiency used) |
| Fig 2.4a: 4–20 mA × 150 Ω = 0.6–3.0 V | | ✅ |
| Fig 2.4b: 1.65 V normal, 0.80 V closed, 3.3 V open, 0 V short | 10k/10k divider; 10k ∥ 4.7k ≈ 3.2k → 0.80 V | ✅ |
| Gateway 100 Ah at ~10 W ≈ 4 days | 1200 Wh / 240 Wh/day = 5 days, ~4 with DoD | ✅ |

The figures that can be checked are all right. That counts for a lot, so keep them. One improvement: the regulatory numbers should cite ERC/REC 70-03 directly rather than Wikipedia (see §4).

---

## 2. Significant issues (fix before submission)

### 2.1 The link budget uses the wrong distance
Table 2.3 and the "Link feasibility" paragraph use the **1.6 km spacing between nodes**. But in LoRaWAN, nodes do not talk to each other. Each node talks to the **gateway**, and the report never gives the gateway's position ("high ground or a public building"). N1 is 2.85 km upstream of N3. The gateway could easily be 3–5 km from N1. More importantly, the nodes sit **on the valley floor**, so the paths are probably not line-of-sight. Free-space margin says very little there. Most of the "48–61 dB margin" can go to a single diffraction edge plus vegetation.
**Fix:** Name a candidate gateway site. Give the node→gateway distances. Run a terrain profile (Radio Mobile, or the Splat/Longley-Rice model with SRTM data) for N1, N2 and N3, and replace "margin at 1.6 km" with "margin on the N_i→GW path". The second-gateway mitigation already exists, so make it the planned fallback for N1.

### 2.2 N3 can react up to 10 minutes late in Normal mode
In Normal, nodes sample **every 10 minutes**, and N3 "evaluates its own danger rule on every sample". Imagine a convective cell that drops its rain on the N2–N3 sub-catchment, below N1. Nothing upstream raises a Watch, so N3 stays in Normal. A flash-flood front can rise by a metre in a few minutes. In that case the "local first" beacon could fire **up to 10 minutes after the water reaches the road**. That breaks the main promise of the report.
**Fix (choose one, and say which):**
- Wire the Watch and Danger floats to an RTC-capable GPIO (or an ULP/comparator wake) so a closing float **wakes the MCU at once**. Keep the analogue supervision read for fault detection.
- Or have N3 sample every 1 min at all times. Its 30 W panel and 20 Ah battery can easily cover that.

Wake on rain-gauge tips at N1 for the same reason. Tips are already counted in deep sleep, so add "a rain-intensity threshold wakes the node and raises the sampling rate".

### 2.3 Pressure sensor physics is missing
- **Venting:** A 4–20 mA submersible gauge transmitter needs a **vented cable**, with a desiccant at the enclosure end. Otherwise barometric changes (±3 cm or more of water during a storm low) end up in the level reading. The other option is an absolute sensor plus a barometer in the enclosure. Say which one you use.
- **Sediment-laden water:** Wadi floods are often hyperconcentrated, with density around 1.1–1.3 or more. A pressure sensor calibrated for clear water then **over-reads depth by 10–30 %**. Together with ultrasonic interference from foam, the rule "disagreement beyond tolerance → degraded flag" will **trigger during real floods**, which is exactly when you need the data. **Fix:** Set the tolerance as a percentage of depth, not in cm. Never let a pressure > ultrasonic disagreement suppress escalation. Add a V1 sub-test using salt or bentonite water.
- **Burial and scour:** One flood can bury a sensor on the bed or tear it out. Mention the anchoring (pipe concreted into the bank, not the bed) and say that burial shows up as a flat-lined reading that the fault logic must catch.

### 2.4 The fusion rule contradicts the Danger rule
- §2.3 Fusion: "A closed Danger float is **accepted even if both continuous sensors fail**."
- §2.5 / Fig 2.6: Danger at N3 "needs **two of the three methods** above the danger height".

So if foam blinds the ultrasonic sensor and the pressure sensor is buried, does a closed Danger float fire the beacon? The report gives two different answers. **Fix:** Use one explicit rule, for example: "Danger = 2 of 3 methods; OR Danger float closed while the other two are flagged degraded (fail toward alarm)". Also, "the median of the continuous readings" is a median of only **two** values, which is just their mean. Say instead "median of the 5 ultrasonic echoes, then cross-check with pressure, bounded by the float steps".

---

## 3. Moderate issues (one sentence or one table row each)

1. **Meshtastic and LoRaWAN share 869.525 MHz.** Meshtastic EU_868 runs in the 869.4–869.65 MHz sub-band by default, and that is also the **LoRaWAN EU868 RX2 downlink** frequency. RX2 carries the gateway's ACKs for confirmed state-change uplinks and the "beacon on early" command to N3. The different sync words limit decoding errors, but the airtime collides and you get blocking. Move Meshtastic to a different frequency slot, or say that you checked coexistence. Also state that the default public channel key is **replaced with a private PSK**, because Meshtastic's default channel key is public.
2. **N3 "listens continuously" means LoRaWAN Class C.** Say so. Put the SX1262 RX current (~5 mA, about 120 mAh/day) in the N3 power budget. It fits easily, but a judge will look for it.
3. **ACKs are ambiguous when several alerts are open.** "Reply 1" does not say *which* alert is being acknowledged. Either say "one open alert per recipient; the reply applies to the latest" or put a short alert code in the SMS ("Reply 1 or 1A7").
4. **When the mobile network is down, officials are cut off.** "Officials are alerted when the network returns" means T3–T5 is cut off while the alert is happening. A cheap fix: give a Meshtastic node to the municipal duty office and the Civil Protection post as well, not only to volunteers.
5. **The gateway reboots mid-escalation.** The escalation state machine and its timers must be **persisted** (SQLite) and restored at boot. Add this to V5 or V6 ("power-cycle the gateway during T2 → T3, and escalation resumes").
6. **N3 brown-out and reset loop.** "Outputs off at reset" is correct. But if the siren (1–2 A) shares a battery with the MCU, a sagging battery can cause a reset → siren off → recovery → siren on → reset cycle. Say that the MCU has its own regulated supply and brown-out detection, and that after reboot it re-evaluates within one sample. Check that the MOSFET is fully on at **3.3 V** gate drive (for example AO3400 or IRLML6344, not IRLZ44N).
7. **The hash-chained log is only tamper-evident if the head is anchored outside the gateway.** Anyone with root on the gateway can rewrite the whole chain. Send the head hash out periodically (in the CAP update, a daily SMS to Civil Protection, or a signature with a key that is not on the gateway).
8. **Ultrasonic range and temperature.** The A02YYUW reaches 4.5 m at most, so the arm must be within 4.5 m of the dry bed **and** above the highest flood mark. Check this against the RR27 bridge height. The speed of sound changes by about 0.17 %/°C, which over a 20 °C swing at 4 m is about 14 cm. Add a temperature sensor and compensate if the module does not do it already. The V1 target of "2 cm over 0–1 m" is a tray test and should be labelled that way, separate from field accuracy.
9. **Fault detection takes 30 minutes in Normal.** Three missed heartbeats at 10 min each is a 30-min blind spot that can begin just before a storm. Shorten the heartbeat when M (forecast or rain) is active, or explain why 30 min is acceptable.
10. **Ground the lead time with numbers.** N1 → N3 is about 2.85 km. A wave celerity of 2–4 m/s gives roughly **12–24 min** of travel time. One sentence with this figure backs up the "no lead-time promise" and shows why the N3 local beacon matters.
11. **Arabic SMS is limited to 70 characters.** Place + action + reply instruction will barely fit in 70 UCS-2 characters. Show the actual Arabic text with its character count, or accept a 2-part SMS.
12. **CAP transport is unspecified.** The report never says how the CAP file reaches the regional committee: email, SFTP, or an HTTP POST? What happens when the internet is down? Give one line on the transport and the fallback.
13. **Voice calls with DTMF** over a cellular modem need a modem with voice support (and VoLTE if 2G/3G is switched off). Name the modem class.

---

## 4. Presentation and editorial

- **"[Project Name]" placeholders** appear in §2.1, §2.6 and Table 2.1. Replace them before submission.
- **Weak sources for technical claims:** [14] Wikipedia is cited for duty-cycle limits (cite ERC/REC 70-03 Annex 1 directly). [8] is a vendor blog (cite a datasheet or paper). [3] is a Zenodo record with no authors. Reviewers notice these in a "technical soundness" chapter.
- **Table 2.1:** The disclaimer "absence of evidence ≠ evidence of absence" is good. Keep "Independent-signal agreement before alarm" modest, because operational hydromet networks (ALERT/ALERT2) do multi-gauge confirmation. Your claim rests on the *combination*, and the report already says so.
- **Table 2.5 V2:** Change "at planned spacing" to "node → gateway on the real paths" (see §2.1).
- **Verification gaps** to add as table rows: sediment-laden water (§2.3), gateway power cycle during escalation (§3.5), Meshtastic and LoRaWAN coexistence (§3.1), and a localised-downstream-rain scenario where N3 responds without N1 (§2.2).
- Figure 2.4 is fine, but its labels overlap in the PDF ("REOL", "at the sensor"). Check the rendering.

---

## 5. Priority list

| # | Change | Effort |
|---|---|---|
| 1 | Node → gateway link budget with a named gateway site and terrain profile | Medium |
| 2 | Float/rain interrupt wake, or 1-min sampling at N3 | Small (text + one GPIO choice) |
| 3 | Make the Danger rule consistent (2-of-3 vs float override) | Small |
| 4 | Pressure: vented cable or barometer; tolerance as % of depth; sediment test | Small |
| 5 | Move Meshtastic off the RX2 frequency; private PSK; Class C stated | Small |
| 6 | Persist escalation state; anchor the log hash | Small |
| 7 | Remove "[Project Name]"; replace the Wikipedia and blog citations | Small |
| 8 | Lead-time estimate, Arabic SMS sample, CAP transport line | Small |

With items 1–4 fixed, the chapter has no obvious technical hole left. The rest is polish.
