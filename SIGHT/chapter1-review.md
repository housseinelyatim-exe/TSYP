# Review: Chapter 1 (`chapter1.pdf`, 5 pages)

**Reviewed:** 2026-10-12, read alongside Chapter 2 (`report.pdf`)
**Verdict:** The story is right: flash floods, warnings that never reach people, and a gap between detecting and acting. As written, though, Chapter 1 is **the weak link of the proposal**. It has no numbers and no references. It still contains notes the authors wrote to themselves. Its figure is missing. Most importantly, **it doesn't define the R1–R6 requirements that Chapter 2 is built on**. Chapter 2 is strong, so the gap between the two chapters is very visible.

---

## 1. Critical: must fix

### 1.1 The R1–R6 requirements don't exist in Chapter 1
Chapter 2 opens with: *"Every choice traces back to the six requirements of Chapter 1: … (R1) … (R6)."* Its verification table (Table 2.5) also links every test to R1–R6. **Chapter 1 never lists them.** A judge reading in order will look for them and find nothing.
**Fix:** Add a section **1.6 Requirements** at the end of Chapter 1. Each requirement should come from a gap found in 1.2 or a need in 1.1.4:

| Req. | Requirement | Comes from |
|---|---|---|
| R1 | Work without grid, internet or mobile network | Floods knock out power and phones; limited connectivity (1.1.2) |
| R2 | Confirm receipt and act on silence | GSMA SMS system can't confirm receipt (1.2) |
| R3 | Give safe-action guidance, not just a level | 2018: warning existed, people still took wrong actions; roadmap gap (1.2) |
| R4 | Limit false alarms | Trust is lost after false alarms (cry-wolf effect) |
| R5 | Low-cost and locally repairable | Community need, municipal technicians (1.5) |
| R6 | Fit the institutional chain; never replace human decisions on public alerts | Regional committee and national SMS channel own public alerts |

### 1.2 No numbers and no references
The chapter cites **no sources at all**. It even says: *"Quantitative information on rainfall, damage, and human consequences **should be supported by reliable historical sources**."* That's a note to ourselves that was left in the final text.
**Fix:** Delete that sentence and replace it with real facts and citations:
- **Nabeul, September 2018:** rainfall, deaths, damage. Chapter 2 already cites the **IFRC DREF final report MDRTN008** ([24]), so use it here as well. It also supports the strongest human point: *a warning existed the day before, and people still made unsafe choices.*
- One or two other Tunisian events with dates and sources (2020 Sahel, Medjerda).
- One number on how fast small catchments react (Chapter 2 cites "under an hour" [23]).
- Ideally, one fact about **RR27 or Oued Souhil itself**: a past incident, traffic, or people exposed.

Rule of thumb: every factual sentence in 1.1 gets a citation.

### 1.3 Figure 1 is missing
On page 1 there is a caption, *"Figure 1. Proposed study area at Oued Souhil…"*, but **no image**.
**Fix:** Insert a map (OpenStreetMap, as in Chapter 2's [1]) that shows the wadi, the RR27 bridge, the planned N1/N2/N3 positions, and the gateway site. That last point is the same gateway fix Chapter 2 needs.

### 1.4 "Methodological note" weakens the site
*"Oued Souhil is a preliminary candidate site… remain subject to field assessment."* Being honest is good, but in this form it reads as "we haven't checked". Put it positively:
> "Oued Souhil is our illustrative site. We selected it because [reasons]. Exact node positions will be confirmed by a field survey in Phase 2."

---

## 2. Important: Section 1.2 "Existing solutions"

### 2.1 We criticise the GSMA system, then Chapter 2 depends on it
Chapter 1 says the GSMA "We Care" SMS system can't confirm receipt and so on. But Chapter 2 sends our CAP recommendation **to the committee that decides public alerts through the national channel** ([26] = the same GSMA system). It's our **partner**, not a competitor.
**Fix:** Frame it as *"good for mass alerts, but one-way: no confirmation, no local sensing at the crossing. We complement it by feeding it verified evidence through CAP."* Also remove *"prevent false alarms from reducing public trust"* from its gap list. That isn't a weakness of an SMS channel.

### 2.2 The gap given for the LoRaWAN/SMS paper backfires
Gap given: *"may not predict a flood early enough for evacuation."* But **our system doesn't predict either**. Chapter 2 says *"We promise no lead time."* A judge will notice that we criticise them for something we don't do either.
**Fix:** Use the real differences, which are already in Chapter 2's Table 2.1: no acknowledgement, no escalation, no local alarm without internet, no agreement between independent signals.

### 2.3 Flood Hub: the wrong gap
The real gap is that **Flood Hub is designed for large rivers**. It doesn't cover small, ungauged wadis where the flood arrives within an hour. That's exactly our case, and it's a much stronger argument than "updated daily".

### 2.4 The hydromet roadmap has no source and a "may not" gap
Which roadmap is it (World Bank, WMO, year)? *"May not adequately address"* is a guess. Cite it, quote what it says about the "last mile" (warnings reaching people), and state the gap clearly.

### 2.5 The closest competitor is missing
Chapter 2's closest work is **[5] Megawati et al.** (solar LoRa, works online and offline, two alert levels), plus **Everbridge [6]** for acknowledgement. Neither appears in Chapter 1.
**Fix:** Add them, and end 1.2 with a **summary table** (a simple version of Table 2.1) so the gap is obvious at a glance. Then 1.6 can say "these gaps give our requirements".

### 2.6 Inconsistent format
The solution headings use different styles, have spaces before colons ("Gap :"), and "Principle and workflow" appears for only one entry. Use the same three-line format for each: **What it is / What it does well / What it misses**.

---

## 3. Important: Section 1.3 "Measurable impact"

### 3.1 The targets contradict Chapter 2
| Metric | Chapter 1 | Chapter 2 | Problem |
|---|---|---|---|
| Delivery rate | ≥ 90 % | V2: ≥ 99 % with retries | Two different targets for the same thing |
| Time to acknowledge | Median < 1 min | Escalation after 3 min | Not a contradiction, but explain that 1 min is the goal and 3 min is the escalation limit |
| Households covered | 90 of 100 | Phase 2 = **tray wadi prototype**, synthetic numbers | You **can't cover 100 households in a tray demo**. Where does 100 come from? |

**Fix:** Make Chapter 1's table and Chapter 2's Table 2.5 use **the same numbers**. Move "households covered" to a **pilot (Phase 3 / after the competition) target**, or drop it.

### 3.2 The most important metric is missing
Our main promise is that the bridge warns people even when everything else fails. So add:
- **Detection-to-beacon time**: water reaches Danger → siren on (target ≤ 5 s, as in the fix discussed for Chapter 2).
- **Offline operation**: the alert chain still works with internet and mobile network off (Chapter 2 test V7).
- **Cost per node / total system cost**: Chapter 1 says "low-cost" but never gives a number. Add a target (e.g., "< X TND per node").

### 3.3 False-alarm rate: define how it's measured in Phase 2
"Below 5 %" of what? In a tray demo there are no real floods. Write: *"measured over N replayed rain and splash scenarios"* (same as V4).

### 3.4 Table font
The table uses a monospace (code) font, which looks unfinished. Use the document's normal font.

---

## 4. Minor: SDGs (1.4) and Inclusion (1.5)

- **SDGs:** name the **specific targets**. They're stronger than the goal names: **11.5** (reduce deaths and losses from disasters), **13.1** (resilience to climate hazards), **3.d** (early warning for health risks). **SDG 6** (drinking water) is a stretch. Drop it or justify it in one line. Consider mentioning the **UN "Early Warnings for All" initiative** (everyone covered by early warning by 2027), because it fits our project exactly.
- **Inclusion (1.5):** good content. Add: messages in **Arabic and French** (Chapter 2 already says this), the **optional assistance flag** for people who need help (Chapter 2 §2.10), and what happens for **people without a phone** (siren and volunteers).
- 1.5 repeats Chapter 2's escalation and CAP details. That's fine as long as both chapters say exactly the same thing: Municipality → Civil Protection → committee decides.

---

## 5. Polish

- There's no **chapter title** and no **"1.1" heading**. The text starts at 1.1.1. Add "Chapter 1: Problem and Context" and "1.1 Problem statement".
- Chapter 1 looks like a Google Doc and Chapter 2 is LaTeX. **Use one style** (fonts, heading numbers, captions) before merging.
- Remove the spaces before colons ("Gap :" → "Gap:") and the stray spaces ("maintainable , and").
- Too many hedges ("may", "should", "proposed", "aims to"). State things directly.
- Nice link to make: 1.1.3 mentions the **sandy channel bed**. That's exactly why Chapter 2's pressure sensor can get buried, so the two chapters support each other if Chapter 2 mentions it.

---

## 6. Priority list

| # | Fix | Effort |
|---|---|---|
| 1 | Add **1.6 Requirements R1–R6**, each linked to a gap | Small |
| 2 | Real numbers + citations in 1.1 (use IFRC [24]); delete the "should be supported" sentence | Medium |
| 3 | Insert the Figure 1 map | Small |
| 4 | Make the 1.3 targets match Chapter 2; move "100 households" to the pilot; add detection-to-beacon time and cost | Small |
| 5 | Rewrite the 1.2 gaps (GSMA as partner, Flood Hub = large rivers, no "prediction" criticism) + add [5] and a summary table | Medium |
| 6 | SDG targets, inclusion additions, unify formatting | Small |
