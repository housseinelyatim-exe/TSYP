# Datasets batch 4: download and analysis results

This follows [`datasets-batch3-analysis.md`](datasets-batch3-analysis.md). Downloaded by the team on 23 Oct 2026 and analysed the same day:

| Dataset | Size | Verdict |
|---|---|---|
| IEEE DataPort *Freeway Traffic Incident Detection* (PeMS): `incident_data.parquet`, `non_incident_data.parquet` | 146 MB + 293 MB; 3.3 M + 6.5 M rows | **Low for recall.** Incident and normal windows are statistically the same at the detector level. Useful only as a freeway false-alarm test |
| NIST smoke alarm tests (TN 1947 compilation): `roomdata.zip`, `smokeboxdata.zip`, `summary_nistsmokebox_roomresults.xlsx` | 4 MB | **Very high.** Real fires vs cooking nuisances, 1 s readings. Gives the second signal for `fire` |

---

## 1. Freeway Traffic Incident Detection (IEEE DataPort, PeMS)

**Format, worked out from the data because the file has no documentation:**

- Columns: `Time`, `Data1`–`Data25`, `tag`, `Week`, `Percentage`, `Median`, `Hour`, `Month`, `Day`, `Y`.
- Each row is a window of **25 consecutive readings** from one detector.
- Rows come in groups of three for the same detector and window: **occupancy** (0–1), **speed** (mph) and **flow** (vehicles per interval).
- `Median` is the detector's usual value for that variable at that time. It is the same-time baseline.
- `Y` = 1 in the incident file. The normal file holds the **same detectors on the day before and the day after**.
- All data is from 2023.

**Data quality problems:**

| Problem | Effect |
|---|---|
| About **60 % of rows are exact duplicates** (both files) | Incident set falls from 926,672 to 343,656 unique detector windows; normal set from 1,835,669 to 719,436 |
| **17 % of incident rows also appear in the normal file** | Removed before comparing |
| `Time` saved as a 32-bit float | Precision lost (about 1.6-day buckets); cannot be used as a timestamp |
| `tag` (0–3) and `Percentage` are undocumented | `tag` has the same distribution and the same speed trends in both files, so it describes the traffic trend in the window, not the incident type |

**Our jam rule on both sets** (deduplicated; "3 in a row" = 3 consecutive readings):

| Rule | Incident windows | Normal windows | Ratio |
|---|---|---|---|
| speed < 50 % of `Median` | 2.57 % | 2.73 % | 0.94 |
| speed < 50 % of `Median` **and** occupancy ≥ 25 % | 1.48 % | 1.63 % | 0.91 |
| speed < 60 % **and** occupancy ≥ 15 % | 3.69 % | 3.97 % | 0.93 |
| speed < 70 % | 6.57 % | 6.54 % | 1.00 |
| speed < 20 mph at any point | 3.56 % | 2.74 % | 1.30 |
| speed falls ≥ 20 mph within the window | 4.38 % | 4.01 % | 1.09 |

**What this shows:**

1. **Most incident windows show no visible effect at the detector.** Median speed is about 62 mph in both sets, with the same profile across the window. Most logged incidents (minor crashes, debris, stalled cars on the shoulder) don't slow traffic at a given detector, or the detector is not the one next to the incident.
2. **So this file can't measure the recall of our rules.** A rule that "misses" 97 % of these windows is not necessarily wrong. Only the "speed < 20 mph" signal is slightly more frequent in incident windows (1.3×).
3. **It confirms the Brain's design choice:** an accident can't be detected from one traffic sensor alone. `accident` needs a call, or several neighbouring sensors plus persistence (same conclusion as UTD19 and NYC).
4. **Useful as a freeway false-alarm test:** on normal days, the full jam rule (speed < 50 % of the same-time median, occupancy ≥ 25 %, 3 readings in a row) fires on **1.6 % of 25-reading windows**. That's a ceiling before the "≥ 2 neighbours" condition is added.

**To measure recall**, we'd need incidents with their **exact location and start time** matched to the nearest detector. That's the TraffiDent version on Kaggle (`gpxlcj/xtraffic`), which keeps the incident table separately. Otherwise use our own labelled scenario (Storm night).

## 2. NIST smoke alarm performance data (TN 1947 compilation)

**Content:**

- **Room tests** (`roomdata.zip`): 90 tests, 6 sources × 5 groups × 3 trials, one reading per second from 60 s before ignition.
  - Sources: two real fires (**flaming polyurethane foam**, **smouldering polyurethane foam**) and four cooking nuisances (**broiled hamburger**, **fried hamburger**, **stir-fried vegetables**, **toast**).
  - Readings: CO2, **CO**, temperature, humidity, HCN, 4 ceiling thermocouples, ionisation chamber current (MIC), light transmission and **smoke obscuration** (%/ft).
- **Smoke box tests** (`smokeboxdata.zip`): 547 tests, one alarm unit per test in a controlled smoke flow, with alarm signal, obscuration, MIC and CO.
- **Summary workbook:** alarm times by alarm type: ionisation (I), photoelectric (P), dual (PI), with a CO sensor (ICO, PCO), and PT.

**Room tests: time to cross each threshold** (medians over 15 tests per source):

| Source | Smoke ≥ 1 %/ft | CO + 10 ppm | Ceiling temperature + 5 °C | CO2 + 0.05 % | Peak CO rise |
|---|---|---|---|---|---|
| **Flaming fire** | 15/15, 185 s | **15/15, 270 s** | 15/15, 262 s | 15/15, 218 s | 13–17 ppm |
| **Smouldering fire** | 15/15, 1,341 s | **15/15, 1,550 s** | 1/15 | 2/15 | 16–521 ppm |
| Broiled burger | 15/15, 1,225 s | **0/15** | **15/15**, 923 s | 0/15 | 0–5 ppm |
| Fried burger | 15/15, 270 s | **0/15** | 0/15 | 0/15 | 0–2 ppm |
| Stir-fry | 15/15, 290 s | **0/15** | 0/15 | 0/15 | 0–2 ppm |
| Toast | weak in room files | **0/15** | 0/15 | 0/15 | 0–1 ppm |

**Commercial alarms sound on cooking** (room tests, alarms sounded / units tested):

| Alarm type | Flaming | Smouldering | Broil | Fry | Stir-fry | Toast |
|---|---|---|---|---|---|---|
| Ionisation (I) | 42/42 | 31/42 | 36/42 | 15/42 | 20/42 | 15/42 |
| Photoelectric (P) | 39/42 | 39/42 | 31/42 | 38/42 | 36/42 | – |
| Dual (PI) | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 3/12 |
| Photo + CO (PCO) | 21/21 | 21/21 | 19/21 | 20/21 | 21/21 | – |

**What this shows:**

1. **Smoke alone can't separate fire from cooking.** All five measured sources cross 1 %/ft. Commercial alarms sound on cooking in 35–100 % of tests, often **faster** than on a smouldering fire (fry burger about 220 s vs smouldering about 800 s). This matches the fire-call data, where about 1 call in 10 is an alarm only.
2. **A CO rise is the best second signal:** CO + 10 ppm over baseline flagged **30/30 real fires and 0/60 cooking tests**. CO confirms about **1.5 min after smoke** for flaming fires and about **3.5 min** for smouldering fires.
3. **Temperature is a weak confirmation.** A broiled burger heats the ceiling by 5 °C (15/15), and smouldering fires mostly don't (1/15).
4. **CO2 + 0.05 % is a fast confirmation for flaming fires only** (218 s, about 30 s after smoke).

**Use for us:**

- **Detection (A):** the `fire` rule becomes: smoke/air-quality abnormal **and** (CO rise ≥ 10 ppm **or** fire call). A smoke rise with no CO and no call is an *ambiguous / nuisance* case (low confidence, not dispatched). Keep the rule open for at least 4 min after the smoke rise, waiting for CO.
- **Mock:** replay real curves at 1 Hz for the `air_quality` sensor: a flaming fire, a smouldering fire, and a fry-burger nuisance. That gives the three test cases "fire confirmed fast", "fire confirmed slow" and "smoke but no fire".
- **Twin hardware:** if the Twin's air-quality sensor has a CO channel (MQ-7 type, or the CO of an MQ-2/MQ-9), use it. If not, the fire call becomes the only second signal.
- **Limits:** indoor single-room tests, not open or outdoor fires. CO is measured with lab analysers, while a cheap Twin sensor has more noise and drift. Toast obscuration in the room files is unreliable (the summary sheet values differ).

---

## 3. Settings to add to `config/detection.yaml`

| Signal | Based on | Setting |
|---|---|---|
| `fire` | NIST room tests | Smoke abnormal **and** (CO ≥ baseline + 10 ppm **or** fire call). Wait up to 4 min after smoke for CO; smoke alone means ambiguous/nuisance |
| `fire` (fast path) | NIST flaming | CO2 rise ≥ 0.05 % within 1 min of smoke also confirms (flaming only) |
| `accident` (freeway) | IEEE PeMS | Single detector speed is not evidence; most incidents leave no trace at the detector. Require a call or ≥ 2 neighbours + persistence |
| `traffic_jam` false-alarm budget | IEEE PeMS normal days | Jam rule without neighbours fires on 1.6 % of 2-h windows; the neighbour condition is mandatory |

## 4. Licences

- **IEEE DataPort Freeway Traffic Incident Detection:** IEEE DataPort terms. Cite DOI 10.21227/hcxe-7k08. Data from Caltrans PeMS.
- **NIST smoke alarm data:** US government work (public domain). Cite NIST TN 1947 and DOI 10.18434/T4530X.

## 5. Files

- Desktop folder:
  - `traffic/ieee-freeway-incidents/`: the two parquet files.
  - `fire/nist-smoke-alarms/`: the original zips, the unzipped `Room Data/` and `Smoke Box Data/`, and the summary workbook.
- Scripts (`scripts/`):
  - `ieee_triplets.py` and `ieee_compare.py`. These need `pandas` and `pyarrow`.
  - `nist_room.py`, `nist_lag.py` and `nist_summary.py`. The summary script needs `openpyxl`; the other two use the standard library only.
