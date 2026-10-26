# Datasets we have: recap and utility

This lists the **17 datasets downloaded and analysed** (23 Oct 2026); candidates we never downloaded are left out. Files are in `~/Desktop/city-brain-datasets/`. Full numbers are in `city-brain-datasets.pdf` (v1.2) and `datasets-*-analysis.md`.

Uses, in the order of the table columns:

- **Detect**: thresholds and rules for `brain/src/detection/` (person A).
- **Graph**: zones, links and chains for `brain/src/graph/` (person B).
- **Mock**: realistic replay data for the mock sensors.
- **Scen.**: test and demo scenarios (normal situations, real incidents, faults, ambiguous cases, cross-domain chains).
- **Eval**: measuring the Brain on data not used to tune it.
- **Score**: realistic numbers for scoring (response times, rates).

## 1. At a glance

| # | Dataset | Domain | Utility | Detect | Graph | Mock | Scen. | Eval | Score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | UTD19 loop detectors (Torino) | Traffic | Very high | ✓ | ✓ | ✓ | ✓ | | |
| 2 | NYC FloodNet | Flood | High | ✓ | ✓ | ✓ | ✓ | | |
| 3 | USGS Raritan River gauge | Flood | High | ✓ | | ✓ | ✓ | | |
| 4 | UCI ElectricityLoadDiagrams | Power | High | ✓ | | ✓ | ✓ | | |
| 5 | NYC 311 calls (Ida night) | Calls | Very high | ✓ | ✓ | ✓ | ✓ | | |
| 6 | NYC Motor Vehicle Collisions | Accident | High | | ✓ | ✓ | ✓ | | |
| 7 | NYC DOT Traffic Speeds | Traffic | High | ✓ | ✓ | ✓ | ✓ | | |
| 8 | DOE Eagle-I power outages | Power | High | ✓ | ✓ | ✓ | ✓ | | |
| 9 | EPA AirNow PM2.5 (smoke) | Air quality | High | ✓ | | ✓ | ✓ | | |
| 10 | NIST smoke alarm tests | Fire sensors | Very high | ✓ | | ✓ | ✓ | ✓ | |
| 11 | Fire & Smoke Digital Twin calls | Fire calls | Medium | ✓ | | ✓ | ✓ | | ✓ |
| 12 | FARS 2024 fatal crashes | Accident | Medium | | | ✓ | | | ✓ |
| 13 | SmartGrid Cyber-Physical Attack | Power / security | Medium | ✓ | | | ✓ | | |
| 14 | Intel Berkeley Lab sensors | Sensor faults | High | ✓ | | ✓ | ✓ | | |
| 15 | Numenta Anomaly Benchmark | Generic | Medium | | | | | ✓ | |
| 16 | PeMS Freeway Incidents (IEEE) | Traffic | Low | ✓ | | | | ✓ | |
| 17 | Smoke Detection IoT (Kaggle) | Fire sensors | Low | | | ✓ | | | |

**Incident types covered:**

| Incident type | Datasets |
|---|---|
| `flood` | 2, 3, 5 |
| `fire` | 9, 10, 11, 17 |
| `accident` | 6, 12, 16 |
| `traffic_jam` | 1, 7, 16 |
| `power_problem` | 4, 8, 13 |
| Faults and fake readings | 13, 14 |

## 2. Each dataset: what it is and how it helps

### Traffic

**1. UTD19: urban loop detectors (ETH Zurich). Very high**
- *What:* 5-min flow, occupancy and speed from 23,626 detectors in 39 cities, plus detector positions, road class and road polylines. Torino analysed in depth: 339 detectors over 21 days.
- *How it helps:*
  - **Detect:** it proved which jam rules give false alarms. "Speed < 20 km/h" gives 1.63 false alarms per detector per day. Our final rule gives **0.065**: speed < 50 % of the same-hour baseline, occupancy ≥ 25 % for 30 min, ≥ 2 neighbours, ignore speed when flow ≈ 0.
  - **Graph:** a real detector → road → neighbour structure to model `NEXT_TO` links.
  - **Mock:** replay real weekdays (rush hour 8h and 17–18h). Test case: "rush hour, no false jam".

**7. NYC DOT Traffic Speeds: Ida night vs a normal Wednesday. High**
- *What:* speeds on 137 NYC links every ~5 min, 1–2 Sep 2021 against 25 Aug 2021.
- *How it helps:*
  - **Scen.:** the real effect of a flood on traffic. At 22h, median speed is 0.33 of normal and 81 links are below half speed.
  - **Detect:** speed 0 is ambiguous (the Lincoln Tunnel closed and read 0). Silent links during the storm show that silence isn't an incident.
  - **Graph:** flood → traffic jam chain for `/chain`.

**16. PeMS Freeway Traffic Incident Detection (IEEE DataPort). Low**
- *What:* 25-reading windows of occupancy, speed and flow at freeway detectors, for incident times and for the same detectors on normal days.
- *How it helps:*
  - **Detect:** confirms that one traffic sensor is not evidence of an accident. Incident and normal windows look the same.
  - **Eval:** the jam rule without neighbours fires on 1.6 % of normal windows (a false-alarm ceiling).
  - **Limit:** it can't measure recall (60 % duplicates, broken timestamps).

### Flood

**2. NYC FloodNet: street flood sensors. High**
- *What:* 3,526 flood events from 319 sensors, each with its full depth curve (1-min steps), plus sensor positions.
- *How it helps:*
  - **Detect:** real rise rates (median 0.10 in/min, fast 0.41), time to peak (37 min) and drain time (54 min), which sets when to close an incident.
  - **Mock:** replay real depth curves.
  - **Graph:** 3 neighbouring Gowanus sensors flooding within 75 min is a test of "one incident spreading to neighbouring zones, not three duplicates".

**3. USGS gauge 01403060: Raritan River. High**
- *What:* water level every 15 min for all of 2021, calm months and Hurricane Ida included.
- *How it helps:*
  - **Detect:** the calm baseline FloodNet lacks (noise std 0.017 ft). Ida's +1.58 ft in 15 min is about 90× normal, so the 3σ rule fires within 1–2 readings.
  - **Scen.:** 6 smaller rises give moderate incidents (severity levels), and a calm month gives the "no incident" test.

**5. NYC 311 service requests: Ida night. Very high**
- *What:* 6,275 flood and signal-failure calls with free text, time and location (31 Aug – 3 Sep 2021), plus August 2021 as a reference.
- *How it helps:*
  - **Mock:** real citizen calls for `brain/internal/call` (sewer backup 27× normal, street flooding 24×; peak 582 calls/h at 22h).
  - **Detect:** "water abnormal + flood call". The first call near Gowanus came 3 min before the sensor.
  - **Graph:** traffic signal failures 4× normal give a flood → power/traffic link.

### Accidents

**6. NYC Motor Vehicle Collisions. High**
- *What:* every police-reported crash with time, position, injuries and causes. Extract: the Ida night and August 2021.
- *How it helps:*
  - **Scen. and Graph:** the last link of the chain flood → signal failure → collisions (+29 % on Ida night; "pavement slippery").
  - **Mock:** accident calls at real positions.

**12. FARS 2024: US fatal crashes (NHTSA). Medium**
- *What:* 36,297 fatal crashes with time, road, weather, light and EMS times.
- *How it helps:*
  - **Score:** unit ETA prior. EMS notification → arrival takes a median of **7 min** (p90 18 min).
  - **Mock:** accident priors by hour, weather and light (peak 17–21h).
  - **Limit:** no sensor data.

### Power

**4. UCI ElectricityLoadDiagrams (Portugal). High**
- *What:* load of 370 clients every 15 min, 2011–2014.
- *How it helps:*
  - **Mock:** a real normal `power_load` curve (peak 18h, night ≈ 45 %).
  - **Detect:** a normal 15-min step is up to 16 % at substation level. Holidays and heat waves look abnormal, so `power_problem` needs a same-time baseline and a second signal.

**8. DOE Eagle-I: power outages, NY + NJ 2021. High**
- *What:* customers without power per county every 15 min.
- *How it helps:*
  - **Detect:** a real `power_problem` is ≥ 10× normal customers out, sustained ≥ 30 min (Ida peak: 92,651 out in NJ). Recovery is slow, more than a day.
  - **Scen. and Graph:** Somerset County had the river flood and 10,000 customers out on the same night (flood → power chain). Other 2021 outages give "power problem without flood".

**13. SmartGrid Cyber-Physical Attack (IEEE DataPort). Medium**
- *What:* 9 PLCs (frequency, voltage, current, power) plus network traffic in 6 scenarios: benign, false data injection and 4 cyber attacks.
- *How it helps:*
  - **Scen.:** the shape of a fake reading (a sudden −40 % / +13 % step on 2–3 devices while the network looks normal), for the "Guardian rejects the sensor → no incident" test.
  - **Detect:** benign variance is almost zero, so the 3σ rule needs a minimum-variation floor.

### Fire and air quality

**10. NIST smoke alarm tests (TN 1947). Very high**
- *What:* 90 room tests at 1 Hz: 2 real fires (flaming and smouldering) and 4 cooking nuisances, with CO, CO2, temperatures and smoke. Plus 547 alarm tests.
- *How it helps:*
  - **Detect:** gives the second signal for `fire`. **CO + 10 ppm flags 30/30 fires and 0/60 cooking tests**, while smoke alone sets off alarms on cooking in 35–100 % of tests. Rule: smoke abnormal **and** (CO rise **or** fire call); wait up to 4 min for CO.
  - **Mock and Scen.:** three real curves: fire confirmed fast, fire confirmed slow, smoke but no fire.
  - **Eval:** an independent fire vs nuisance test.

**9. EPA AirNow: hourly PM2.5 during the June 2023 wildfire smoke. High**
- *What:* hourly PM2.5 at 1,356 US sites; 8 NYC sites used.
- *How it helps:*
  - **Detect:** a normal 1-h change is ≤ 7.4 µg/m³; smoke rose +132 in 1 h, peaking at 336.
  - **Scen.:** the ambiguous case. A city-wide rise with no fire call is regional smoke, not a fire.

**11. Fire & Smoke Digital Twin: fire incident calls. Medium**
- *What:* 331,616 fire calls in 13 US cities (type, position, time). There are no sensor readings.
- *How it helps:*
  - **Mock:** real fire call categories and hourly rates.
  - **Detect:** about 28,000 calls are alarms, not fires, which supports "fire call **and** sensor signal".
  - **Score:** realistic call rates.

**17. Smoke Detection IoT (Kaggle). Low**
- *What:* 62,630 readings at 1 Hz from an air-quality sensor (TVOC, eCO2, PM, temperature) with a fire label.
- *How it helps:*
  - **Mock:** value ranges only (TVOC ≈ 100 ppb with spikes).
  - **Limit:** the labels are unreliable, so never train or set thresholds on it.

### Sensor faults and evaluation

**14. Intel Berkeley Lab sensor data. High**
- *What:* 2.3 M readings from 54 motes (temperature, humidity, light, battery voltage) every 31 s.
- *How it helps:*
  - **Detect:** real fault shapes. Dying batteries (< 2.4 V) give readings up to **385 °C**, a "fire" with no fire. There are also 333 stuck runs and frequent gaps.
  - **Mock:** fault injection.
  - **Rule:** check device health; never open an incident on one sensor.

**15. Numenta Anomaly Benchmark (NAB). Medium**
- *What:* 58 time series with labelled anomaly windows.
- *How it helps:*
  - **Eval:** an independent test of our spec rule (EMA α = 0.05, 3σ, 3 readings). It gives recall 0.71 on traffic, but **1.2 false alarms per day** on a clean daily cycle. That is why daily signals need a per-hour baseline.
  - **Limit:** use it only to evaluate, never to tune.

## 3. The cross-domain combination: the Storm-night scenario

Datasets 2, 3, 5, 6, 7 and 8 all describe **Hurricane Ida (1–2 Sep 2021)**:

| Time | What happened | Source |
|---|---|---|
| 22h | Flood calls peak at 582/h | 311 |
| 22h | Median road speed 0.33 of normal | DOT |
| 22h | Raritan River rising | USGS |
| Overnight | Power outages peak at 92,651 customers (NJ) | Eagle-I |
| 12 h window | Collisions +29 % | Collisions |

Together they form a real, timestamped chain flood → traffic jam → accidents → power problem. It's the basis of our demo, compressed from 12 h to about 10 min, and it tests detection, `/chain`, `/context` and neighbouring-zone links all at once.

## 4. What the data taught us (one line each)

1. Daily-rhythm signals need a per-sensor, per-hour, weekday/weekend baseline, not a plain EMA (from NAB, UTD19, UCI).
2. No incident is ever opened on one sensor (from Intel, PeMS, NIST, smoke).
3. Every incident type needs a second signal: a call, neighbours or another sensor. For fire, that's **CO** (from NIST).
4. Silence and speed 0 are ambiguous, not incidents (from NYC DOT, Intel).
5. Fake readings look like sudden steps on a few devices while the network looks normal (from the smart-grid set).
