# Datasets batch 3: closing the gaps

This follows [`datasets-batch2-analysis.md`](datasets-batch2-analysis.md). Downloaded and analysed on 19 Oct 2026.

| Gap | Dataset | Result |
|---|---|---|
| Labelled anomalies (evaluate our detector) | **Numenta Anomaly Benchmark (NAB)** | Our spec EMA rule: 71 % recall on traffic, but about 1.2 false alarms/day on clean periodic signals |
| Labelled sensor faults | **Intel Berkeley Lab** (54 motes, 2.2 M readings) | Dying batteries produce **fake temperatures up to 385 °C**, a fault that looks like fire |
| Real fire / smoke air quality | **EPA AirNow hourly PM2.5, June 2023** (Canadian wildfire smoke over NYC) | PM2.5 11.5 → **336 µg/m³**; +132 µg/m³ in one hour |
| Real power failure | **DOE Eagle-I outages 2021**, NY + NJ, 15-min by county | Ida: **92,651 customers out in NJ**, 50,995 in NY |
| Cross-domain: flood → traffic | **NYC DOT Traffic Speeds**, Ida night vs a normal Wednesday | At 22h, **81 of 137 road links below half their normal speed** |
| Labelled traffic incidents (PeMS) | TraffiDent / Freeway Incident Detection | **Not downloaded**: needs a Kaggle account or a browser download from IEEE DataPort |

---

## 1. Numenta Anomaly Benchmark (NAB): testing our detection rule

**Source:** GitHub `numenta/NAB` (MIT). 58 series with labelled anomaly windows. Used here: `realTraffic` (7 series: speed, occupancy, travel time from Minnesota detectors), `realKnownCause` (7: machine temperature, NYC taxi demand, ambient temperature…), `artificialWithAnomaly` (6), `artificialNoAnomaly` (5).

We ran the **exact rule from our spec** (EMA α = 0.05, |x − mean| > 3σ, 3 readings in a row), with no learning from anomalous points:

| Category | Anomaly windows | Recall | False alarms / day |
|---|---|---|---|
| Real traffic | 14 | **0.71** | 0.25 |
| Real known cause | 19 | 0.53 | 1.16 |
| Artificial with anomaly | 6 | 0.83 | 1.41 |
| **Artificial, no anomaly at all** | 0 | — | **1.21** |

- On traffic it's decent: 10 of 14 incidents caught, about 1 false alarm every 4 days per sensor.
- **On clean periodic series (a daily sine, no anomaly) it still fires about 1.2 times a day.** The EMA lags behind a daily cycle and sees the cycle itself as abnormal. This is the same lesson as UTD19 and UCI: **for any signal with a daily rhythm (traffic, power, air quality), the "normal" must be a time-of-day baseline, not a plain moving average.**
- A minimum-variation floor (5 %) barely changes the result here (it matters for flat signals, as the smart-grid set showed).

**Use:** an independent test bench for detection. Keep it for **evaluation only**, not tuning.

## 2. Intel Berkeley Research Lab: real sensor faults

**Source:** MIT CSAIL `labdata` (open). 54 Mica2Dot motes, temperature, humidity, light and battery voltage every 31 s, 28 Feb – 5 Apr 2004. 2.31 M lines, of which 94 k (4 %) are malformed or truncated.

| Fault | Measured |
|---|---|
| **Impossible temperatures** | **17.7 % of readings > 50 °C, max 385 °C**. **51 of 52 motes** develop it |
| Cause | Battery: 65 % of readings with voltage < 2.4 V are > 50 °C, and **0 %** above 2.4 V. Onset at a median 2.3 V |
| Stuck values | 333 runs of ≥ 20 identical temperature readings |
| Gaps | Median step 33 s, p99 322 s; 1.1 % of gaps > 5 min |
| Normal behaviour | Temperature 16–32 °C (p1–p99); a normal step changes by ≤ 0.22 °C (p99) |

**Why it matters:**
- A dying sensor produces a **"fire-like" reading** (temperature shoots up) with **no fire**. The Guardian layer should flag it, and our detection must not open a `fire` incident on one sensor. The device's **health (battery voltage)** is a better clue than the value.
- Gaps and stuck runs are realistic "silent" and "frozen" faults for the mock and for the rule "a silent sensor must not keep an incident open".

**Use:**
- **Mock:** inject these real fault shapes (slow climb to absurd values as voltage drops, stuck runs, gaps) into our simulated sensors.
- **Guardian team:** a labelled benchmark (fault ⇔ voltage < 2.4 V).
- **Detection (A):** a range check from the city description's `alert` / max values, plus at least two sensors agreeing.

## 3. EPA AirNow: real smoke event (June 2023 wildfire smoke, NYC)

**Source:** `files.airnowtech.org` hourly files (open, US EPA). 1–14 June 2023, PM2.5 only: 433 k rows, 1,356 sites. NYC sites used: Bronx IS52 and IS74, Manhattan IS143, CCNY, Maspeth, Queens, Queens near-road, Fresh Kills.

| Measure | Value (median of NYC sites) |
|---|---|
| Baseline (1–4 June) | **11.5 µg/m³** |
| Normal 1-h change | p99 **7.4 µg/m³** |
| First hour > 3 × baseline | 6 June 02:00 UTC |
| Peak | **336 µg/m³** on 7 June 18:00 UTC (14:00 local); a single site reached 412 |
| Fastest rise | **+132 µg/m³ in 1 h** (about 18 × the normal p99) |
| Hours above 35.5 / 150.5 / 250.5 | 72 / 14 / 3 |
| Daily max | 6 Jun 162 → 7 Jun 336 → 8 Jun 226 → 9 Jun 39 |

**Use:**
- **The real air-quality signal for `fire`** that the Kaggle smoke set couldn't give. It's a city-wide smoke event, so it shows the shape (fast rise, plateau over hours, slow decay) and the scale (×30 the baseline).
- **Ambiguous case:** very high air-quality readings **everywhere at once, with no fire calls**. That's regional smoke, not a local fire. Our `fire` rule (air quality **and** a call or a local signal) handles it correctly; the test scenario proves it.
- **Limits:** hourly (our sensors will be faster); outdoor stations, not a building fire.

## 4. DOE Eagle-I: real power outages (2021, New York + New Jersey)

**Source:** figshare DOI 10.6084/m9.figshare.24237376 (US DOE / ORNL, open). Customers without power, per county, every 15 min. The 2021 file (1.1 GB) was streamed and filtered to NY + NJ. Times are as provided in the file (likely UTC).

| | New York | New Jersey |
|---|---|---|
| August baseline (customers out) | about 1,030 | about 320 |
| **Ida peak** | **50,995** (2 Sep 07:15) | **92,651** (2 Sep 04:15) |
| Rise | 1,400 → 8,000 → 30,500 in 6 h | 4,400 → 32,000 → 83,000 in 4 h |
| Recovery | still 10,000 out 30 h later | still 13,700 out 30 h later |
| Worst counties at peak | Westchester 17 k, Suffolk 9 k | Essex 16 k, Morris 12 k, Sussex 12 k, **Somerset 10 k** |
| Other big 2021 events | 26 Mar (88 k), 2 Mar (62 k), 6 Jul (48 k) | 6 Jul (94 k), 14 Sep (69 k) |

- **Somerset County, NJ is where the Raritan gauge (batch 2) is.** The record river flood and 10,000 customers out happen in the same county on the same night.
- NYC's five boroughs peaked at only about 6,600 out (underground grid): the flooding there hit traffic and signals more than power.

**Use:**
- The first **real `power_problem` incidents**: shape (fast rise in 2–4 h, slow recovery over a day or more), scale (×100–300 the baseline), and several non-Ida events for "power problem without flood".
- **Mock:** a substation-level "customers out" or load-drop signal for the Storm-night scenario.
- **Limits:** county level, not a substation; customers, not kW.

## 5. NYC DOT Traffic Speeds: the Ida night vs a normal Wednesday

**Source:** NYC Open Data `i4gi-tjb9` (open). Speeds on 137 monitored links (highways, bridges, tunnels, major arterials), about every 5 min. Compared: 1 Sep 12:00 → 2 Sep 12:00 (Ida) against 25 Aug at the same hours (the previous Wednesday).

| Hour (local) | Median speed vs normal | Links < 50 % of normal |
|---|---|---|
| 18h | 0.87 | 12 |
| 20h | 0.79 | 16 |
| 21h | 0.66 | 40 |
| **22h** | **0.33** | **81 of 137** |
| 23h | 0.58 | 66 |
| 01h | 0.68 | 64 |
| 03h | 0.84 | 45 |
| 09h next day | 0.83 | 51 |

- **22h is also the peak hour of 311 flood calls (582).** Sensors, calls and traffic all peak together.
- Lincoln Tunnel tubes read **0 km/h from 21h to 00h**. That's a closure, not a jam. A speed of exactly 0 is ambiguous (closed, or a sensor fault), so the context and the graph should resolve it.
- From 01h, fewer readings arrive (1,258 vs 1,644 per hour), so **some links went silent** during the storm.
- Traffic hadn't recovered by 09h the next day (51 links still slow).

## 6. The complete Storm-night chain (NYC / NJ, 1–2 Sep 2021)

Everything below is real, timestamped data from public sources:

| Local time | Flood sensors | Calls (311) | Traffic | Power |
|---|---|---|---|---|
| 19–20h | First FloodNet event 20:11 (Gowanus) | 29 → 47 flood calls/h; first nearby call 20:08 | Speed 0.79 of normal | Normal |
| 21h | 2 more Gowanus sensors flood (up to 35.6 in) | 221/h; signal-controller failures rising | 40 links < 50 % | NJ 4,400 out |
| **22h** | Raritan River rising +1.6 ft / 15 min | **582/h** | **0.33 of normal, 81 links < 50 %** | Rising |
| 00h | — | 338/h | 60 links < 50 % | **NJ peak about 92,000** (04:15 UTC) |
| Morning | Raritan peak 42.1 ft at 12:00 | Second wave (damage reports) | Still 51 links slow | NY peak about 51,000 |

This is the **"Storm night" demo scenario**: one event that crosses the five incident types we handle (flood, traffic jam, accidents +29 %, power problem, plus ambiguous and silent sensors), ideal for showing the graph's links and the `/chain` endpoint.

## 7. What is still missing

| Gap | Status |
|---|---|
| Labelled traffic incidents (TraffiDent / PeMS) | Needs **your** download: Kaggle `gpxlcj/xtraffic` (account) or IEEE DataPort "Freeway Traffic Incident Detection" (browser, logged in). Licence CC BY-NC 4.0 |
| A real *building* fire with sensors | None public found. Use AirNow for shape and scale, and simulate a local fire |
| Local (Tunisian) time series | None found |

## 8. New settings for `config/detection.yaml`

| Setting | Value | Evidence |
|---|---|---|
| Baseline type for daily-cycle signals (traffic, power, air quality) | **Per sensor, per hour, weekday/weekend**, not a plain EMA | NAB: about 1.2 false alarms/day on a clean sine; UTD19; UCI |
| Device health | Ignore or flag readings when battery or voltage is low; range-check against the city description | Intel: 100 % of > 50 °C readings at < 2.4 V |
| `air_quality` rise | Normal 1-h change ≤ about 7 µg/m³; smoke event rises of 100+ µg/m³/h | AirNow |
| City-wide air-quality rise with no call | Regional smoke, **not** a `fire` incident | AirNow (June 2023) |
| `power_problem` | ×10+ customers out (or load drop) vs baseline, sustained ≥ 30 min | Eagle-I |
| `traffic_speed` = 0 | Treat as "closed or faulty" and check context; not an automatic jam | DOT (Lincoln Tunnel) |
| Silent sensors during an incident | Expected; don't close or keep open on silence alone | DOT, Intel |

**Licences:**
- NAB (MIT; cite Ahmad et al. 2017)
- Intel Lab (open; acknowledge MIT CSAIL / Intel Research Berkeley)
- AirNow (US EPA, public; data are preliminary)
- Eagle-I (open, figshare DOI above; cite the dataset)
- NYC Open Data (open)

All files are in the scratchpad: `/tmp/claude-1000/-home-houssein-Desktop-TSYP-CSXCNXYP/872a9597-1f52-4fbd-af79-8fd54cb1c216/scratchpad/{nab,intel,airnow,eaglei,nyc}/`.
