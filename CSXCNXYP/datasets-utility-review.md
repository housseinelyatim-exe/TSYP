# Datasets: what they are useful for (Graph team view)

`Dataset (1).pdf` suggests four public sources, one per incident domain. This file covers all of them, plus the FARS crash data already downloaded. Numbers below were measured on the downloaded data (18 Oct 2026).

| Domain | Dataset | Access | Status | Utility for us |
|---|---|---|---|---|
| Accidents | **FARS 2024** (NHTSA) | Open | Downloaded, analysed | Medium: priors, mock calls, EMS times |
| Traffic / jams | **UTD19** (ETH Zurich) | Free, but **registration form → link by email**; academic / non-commercial use | Downloaded, Torino analysed | **High**: real 5-min flow / occupancy / speed; rush-hour and false-jam evidence |
| Fire | **Fire and Smoke Digital Twin** (`UrbanInfoLab/FireIncidentData`, GitHub) | Open | Downloaded, analysed | Medium: fire call text and rates; **no sensor data** |
| Flood | **NYC FloodNet** (NYC Open Data) | Open | Downloaded, analysed | **High**: real 1-min depth curves |
| Power grid | **SmartGrid-CyberPhysical-Attack-Dataset** (IEEE DataPort) | **Login + subscription** | Downloaded (via a member's account), analysed | Medium for Guardian; **low for detection** (4-min simulated steady state) |

---

## 1. NYC FloodNet: the most useful one we can get today

**Files:** `events.csv` (dataset `aq7i-eu5q`, 3,526 flood events, 6 MB) and `sensors.csv` (dataset `kb2e-tjy3`, 491 sensors).
**Coverage:** Nov 2020 to Oct 2026, 319 sensors with at least one event. Sensors are ultrasonic, mounted on street sign posts, and sample every **60 s** (median step 61 s).

Each event has a start and end time, max depth, time to peak, time to drain, durations above 4 / 12 / 24 in, and the **full depth time series** (median 76 points per event). Each sensor has lat/lon, borough, a tidally-influenced flag and its height above the local low point.

| Measure | 10 % | 50 % | 90 % |
|---|---|---|---|
| Max depth (in) | 0.9 | 3.5 | 11.1 (99 %: 25.4) |
| Time to peak (min) | 6 | 37 | 119 |
| Rise rate to peak (in/min) | 0.03 | 0.10 | 0.41 (99 %: 1.34) |
| Time to drain (min) | 12 | 54 | 196 |
| Total duration (min) | 20 | 111 | 285 |

- 12 % of events never pass 1 in, 45 % reach 4 in, 8 % reach 12 in.
- **67 % of events (2,377) are at the 67 tidally-influenced sensors.** Tidal flooding is a regular, predictable pattern, so it's a good "normal situation" for the reference library.

**What it gives us:**
- **Detection (A):** realistic values for "abnormal **and rising**". A rise of more than about 0.1 in/min is typical of a real flood, and 0.4 in/min is fast. Short events under 1 in, which peak and drain in minutes, are good examples of "high water that doesn't persist" (ambiguous). It also gives realistic close timing: drain takes about an hour.
- **Mock:** replay real curves as `water_level` readings. Inches convert to metres or cm, and 60 s steps can be sped up for the demo. This gives realistic noise and shape instead of hand-made ramps.
- **Graph (B):** severity bands from the 4 / 12 / 24 in thresholds; 4 in is roughly where streets become hard for vehicles.
- **Limits:** these are street-level depths in NYC, not river or port levels. Before the event starts, depth is zero, so there's **no normal (no-flood) baseline**; the mock must generate calm periods itself.

## 2. Fire and Smoke Digital Twin (`FireIncidentData`)

**Files:** a 143 MB repo with 13,047 daily `FireMap.json` files across 13 US cities, 2022–2026. Files are RSS-style, one item per call: `title` (call type), lat/lon, `description` (street | agency | time), `pubDate`, `active_status`.
**Content:** 331,616 unique fire calls. The most active cities are Seattle (median 78 per day) and Houston (65). 3,493 files are empty because of collection gaps.

- Top call types: "LEVEL 2 FIRE", "FIRE EVENT", "LEVEL 1 FIRE", "MVC-FIRE ONLY" (a motor vehicle crash with fire), "AUTOMATIC FIRE ALARM", "FIRE ALARM", "APARTMENT FIRE", "CAR FIRE", "TRASH FIRE", "BUILDING FIRE".
- By hour: the low is at 3h–6h (about 7,400), there's a broad plateau from 11h to 21h (about 16,000), and a peak at midnight (17,400, probably partly a midnight-rollover artefact).
- **Many calls are alarms, not fires** ("AUTOMATIC FIRE ALARM", "FIRE ALARM": about 28,000). That is a real source of **ambiguous cases**: a fire call without a confirmed fire.

**What it gives us:**
- **Mock:** realistic fire call categories, wording and rates per hour, for `brain/internal/call` messages.
- **Detection (A):** a prior on how often a "fire call" is just an alarm. That supports the "fire call **and** air quality abnormal" rule rather than trusting a call alone.
- **Cross-domain:** "MVC-FIRE ONLY" calls (about 15,000) are accident + fire combinations.
- **Limits:** despite the project's name, the repo has **no smoke or air-quality readings**. Those come from the backend's smoke model, which we didn't fetch. It has no outcome or severity beyond "level 1 / 2". It can't tune the air-quality threshold.

## 3. FARS 2024 (accidents)

`accident.csv`: 36,297 fatal crashes and 39,254 deaths in the US. Fatal crashes peak 17h–21h, 75 % in clear weather and 7 % in rain. EMS notification → arrival: **median 7 min, 90th percentile 18 min**.
**Utility:** accident priors (hour × weather × light), mock accident calls, unit response times. **Limits:** no traffic sensor streams, fatal crashes only, US roads only. Only `accident.csv` (23 MB) is worth keeping out of the 33 files.

## 4. UTD19 (traffic)

**Files:**
- `utd19_u.csv` (7 GB): `day, interval (s from midnight), detid, flow (veh/h), occ (%), error, city, speed (km/h)`. Lines end in CRLF.
- `detectors_public.csv` (23,626 detectors): road class, road name, speed limit, lanes, link id, lat/lon.
- `links.csv`: road polylines.

**Coverage:** 39 cities (London is the largest, at 34 M rows and 5,719 detectors). Each city covers only a window of days to months, mostly between 2015 and 2017. **Speed is present in only 9 cities**: Torino, Rotterdam, Manchester, Constance, Groningen, Bolton, Essen, Innsbruck and Birmingham. The `error` field is `1` on 0–79 % of rows depending on the city, so filter it out.

**City analysed: Torino.** 399 detectors (339 with speed), 21 days (26 Sep – 16 Oct 2016), 5-min intervals, 2.08 M rows, 13 % error-flagged. Data coverage is 99 % for the median detector; 10 % of detectors have less than 66 %, so **silent sensors are real**.

| Measure | 10 % | 50 % | 90 % |
|---|---|---|---|
| Speed (km/h) | 21 | 43 | 64 |
| Flow (veh/h) | 36 | 336 | 972 |
| Occupancy (%) | 0.8 | 8 | 27 |

**Rush hour (weekday medians):** flow peaks at **8h (732 veh/h)** and **17–18h (about 700)**, against 24 at night. Speed drops only modestly, from 46–50 at night to **39 km/h at rush hour**. Weekends have no morning peak; flow is flat from 10h to 19h.

**Testing jam rules on 21 days of real traffic.** These are episodes per detector-day. Torino had no known major incident, so almost every episode is a **false alarm**:

| Rule (3 × 5 min in a row unless stated) | Episodes / detector-day | Comment |
|---|---|---|
| Speed < 20 km/h | 1.63 | Useless. Peaks at **3h**, when speed is low because **no cars pass** (median flow 0) |
| Speed < 50 % of the detector's overall median | 1.21 | Same night problem |
| Speed < 50 % of the **same-hour, same-day-type** baseline | 0.63 | Night false alarms drop by 3× |
| + occupancy ≥ 25 % | 0.29 | Removes empty-road cases; what remains is mostly real rush-hour queues |
| + occupancy ≥ 25 %, **6 × 5 min (30 min)** | **0.065** | 82 of 339 detectors ever fire; still about 150 in the 16–19h peak |
| Spec EMA rule (α 0.05, 3σ, 3 in a row) on speed | 0.023 | Rare, but it can't tell a jam from a sensor fault and drifts with rush hour |

- **Sudden speed drop:** a ≥ 50 % fall in one 5-min step (from > 30 km/h) happens in **3.7 % of all intervals**. On its own it's noise. The accident rule needs an accident call, persistence, or several detectors on the same link agreeing.

**What it gives us:**
- **Detection (A):**
  - `traffic_jam` must use a **per-detector, per-hour, weekday/weekend baseline** plus **occupancy** and a **persistence of 15–30 min**, not raw speed.
  - **Ignore speed when flow ≈ 0.**
  - Requiring 2+ neighbouring detectors (from the graph's `NEXT_TO` / link) should cut the remaining false alarms further. That's our "combine signals per zone" step.
- **Mock:** replay real Torino detectors as `traffic_speed` / `traffic_flow` readings. That gives a realistic rush hour for the "rush hour: no false jam" test. Real detector gaps also test the "silent sensor" handling.
- **Graph (B):** `detectors_public.csv` + `links.csv` give real **detector → road link → neighbour** structure, a realistic model for sensor `IN` zone / zone `NEXT_TO` zone.
- **Limits:** 2016 data, a European city, no incident labels (so a precision test is possible but not recall), and speed is only available in 9 cities.
- **Licence:** academic and non-commercial use only. Cite Loder et al. 2019 (*Scientific Reports*) and acknowledge utd19.ethz.ch in the report.

## 5. SmartGrid-CyberPhysical-Attack-Dataset (IEEE DataPort, DOI 10.21227/symr-bz19)

**Files:** a 4.6 MB zip (151 MB unzipped) with 6 folders: `benign`, `FDI` (false data injection), `backdoor`, `Bruteforce`, `ransomware`, `reverseshell`. Each folder holds a `Physical.csv` and a `Cyber.csv`, and each file has about **100,000 rows covering about 4 minutes** (it looks like a row-capped export). The testbed is simulated (Docker network 192.168.x.x, Modbus/TCP on port 502). There is **no label column**: the folder name is the label, and nothing marks when the attack starts.

**Physical.csv:** `@timestamp, PLCID (1–9), Freq, Theta, V_A/B/C, I_A/B/C, ActivePower, ReactivePower, BreakerStatus`. There are 9 PLCs, sampled several times per second. Numbers use thousands separators (`"85,717,736"`), and the units look scaled (V about 8.6e7, P about 1e14), so we need to normalise them.

- **Benign is a flat steady state.** Frequency is a constant 59.992 Hz and V, I and P barely move (relative deviation < 0.01 %). The breaker is always closed. There are no load changes, faults or daily pattern.
- **FDI: the injection shows only in the last ~10 s** (t ≥ 240 s). PLC7 current drops 39 % (254.7k → 155.9k), PLC6 current rises 13 % (401k → 453k), PLC9 current drops 2 % and PLC7 active power rises 2.4×. Everything before that is identical to benign. So it's a **sudden step injection** on 2–3 devices.
- **The other four attacks don't change the physical values** (only noise on near-zero reactive power). They're purely cyber.

**Cyber.csv:** packet headers only (`node, frame.time_epoch, eth/ip src/dst, protocol, ip.len, tcp/udp ports`), with no payload and no flags. The `FDI/Cyber.csv` header has one more column than its rows, so the columns are shifted by one.

| Scenario | Visible signature vs benign (≈400 pkt/s, 30 source IPs) |
|---|---|
| Bruteforce | 466 pkt/s; host 192.168.200.11 sends about 9,600 HTTP packets to port 9090 (benign: about 2,500 in total) |
| Backdoor | **SSH (port 22) appears**, 147 packets; absent in benign |
| FDI | Traffic looks normal; the attack is visible only in the physical values |
| Ransomware, Reverse shell | Nothing visible in these coarse statistics; it would need per-flow features |

**What it gives us:**
- **Guardian layer (main user):** a ready benchmark for "cyber anomaly + physical anomaly" fusion. The useful lesson: FDI is invisible on the network and the other attacks are invisible physically, so you need both views.
- **Mock:** a realistic *pattern* for our fake power reading. Steady values, then a **step of −40 % / +13 % on a few devices**. That's a better fake than a random spike. It's the input for the "Guardian rejects the sensor → no incident" test.
- **Detection (A), warning:** benign variance is nearly zero, so a rule like "3 × usual variation" would flag any tiny change. **Add a minimum variation floor** (for example 1–2 % of the mean) in `config/detection.yaml`.
- **Limits:** only 4 minutes per scenario, no labels or attack times, simulated rather than real, odd units, 60 Hz US grid. It can't give normal daily load curves for `power_load`. Those must be synthetic, or come from an open load dataset such as a national grid operator's public load data.

---

## 6. Verdict and next steps

1. **Use FloodNet now.** Convert 10–20 real event curves into mock `water_level` scenarios, and set the detection "rising" and close thresholds from the table in section 1. This is the best real data for our flood test ("opened within 3 readings, updated, closed").
2. **Use UTD19 Torino** for traffic: write the jam rule as "speed < 50 % of the same-hour baseline **and** occupancy ≥ 25 % for 30 min **and** ≥ 2 neighbouring detectors", ignore readings with zero flow, and replay a weekday rush hour for the false-jam test.
3. **Fire data:** use it for call text and categories plus the alarm-vs-fire ambiguity. Air-quality behaviour must still be simulated.
4. **Smart grid:** pass it to the Guardian team (fusion benchmark). For us, copy its FDI step pattern into the mock "fake power reading" scenario, and add a minimum-variation floor to detection. Normal power load curves stay synthetic.
5. Every source has a different schema and units, so the mock team needs one small converter per source to our `reading` / `call` formats (section 3 of the contracts).
6. **Nothing covers our city's geography.** Real data gives shapes, rates and statistics. Zones and sensor IDs still come from our Twin's city description.
