# Additional public datasets: candidates to fill our gaps

This follows on from [`datasets-utility-review.md`](datasets-utility-review.md). The five datasets reviewed there leave these gaps: **air-quality / smoke readings** (fire detection), **normal power load curves**, **labelled traffic incidents** (to measure detection recall), **labelled sensor faults**, **emergency call text**, a **calm baseline for water level**, and a **single city covering several domains** (for cross-domain scenarios).

Nothing below has been downloaded yet. Access was checked from the public pages only.

## 1. Priority list

| # | Dataset | Gap filled | Access | Size | Why it matters to us |
|---|---|---|---|---|---|
| 1 | **Kaggle "Smoke Detection Dataset"** | Fire sensor readings | Kaggle account | ~62,600 rows, 1 Hz | Labelled `Fire Alarm` 0/1 with temperature, humidity, TVOC, eCO2, PM1.0, PM2.5. The only labelled fire **sensor** data we found. Calibrates the `fire` rule's air-quality signal. (Drop the `CNT` counter column, which leaks the label.) |
| 2 | **NYC Motor Vehicle Collisions – Crashes** (NYC Open Data) | Accident labels, same city as FloodNet | Open, CSV / API | Since 2016, about 2 M crashes | Every police-reported crash with time and lat/lon. Combined with FloodNet it gives **real cross-domain cases** (see section 2) |
| 3 | **NYC 311 Service Requests** (filter: *Street Flooding*, *Catch Basin Clogged*, *Sewer Backup*, smoke / fire complaints) | Citizen "calls" with text | Open, Socrata API | Very large; filter by type and date | Real citizen reports with a free-text descriptor, timestamp and location. A realistic source for `brain/internal/call`, matched in time to FloodNet sensors |
| 4 | **Freeway Traffic Incident Detection Dataset** (IEEE DataPort, DOI 10.21227/hcxe-7k08, derived from PeMS / TraffiDent) | Labelled traffic incidents | IEEE login (we have one) | 16,972 detectors, 5-min | Incident windows matched to nearby sensors, with same-weekday normal traffic as negatives. Lets us measure **recall** of the accident / jam rules, which UTD19 can't (UTD19 has no labels) |
| 5 | **UCI ElectricityLoadDiagrams 2011–2014** | Normal power load | Open, CC BY 4.0 | 678 MB, 370 clients, 15-min, kW | Real daily and weekly load curves, the normal baseline for `power_load` that the smart-grid set lacks |
| 6 | **Intel Berkeley Lab sensor data** + the 2016 **labelled fault benchmark** built from it | Sensor faults | Open (MIT CSAIL page) | 2.3 M readings, 54 sensors, 31 s | Real temperature / humidity / light / voltage motes with typical faults (dying battery → drift, stuck values). The benchmark paper adds **labelled** random, malfunction, bias and drift faults. Tests the "frozen / drift / dropout" cases |
| 7 | **Numenta Anomaly Benchmark (NAB)** (GitHub `numenta/NAB`) | Labelled anomalies in streams | Open, MIT | 58 series, mostly 5-min | Includes NYC taxi demand, machine temperature and traffic speed / occupancy series with labelled anomaly windows, plus a scoring method that **rewards early detection**. Good for testing our EMA abnormality step |
| 8 | **USGS NWIS instantaneous values**, gage height (parameter 00065) | Calm water-level baseline + river floods | Open REST API, no key | 15-min, years per gauge | Continuous water-level series **including calm periods** (FloodNet has none). Pick one river or coastal gauge with a known flood. Gives both "normal variation" and "real rise" |
| 9 | **SF Fire Department Calls for Service** (DataSF) | Fire / EMS dispatch and response times | Open, CSV / API | Since 2000, millions of rows | Call type (structure fire, alarm, traffic collision, medical), unit dispatched, and every time step from call to on-scene. Better than FARS for **unit response time** and for the alarm-vs-real-fire ratio |
| 10 | **OpenStreetMap via OSMnx** (Python) | City graph | Open (ODbL) | Any city | One call (`graph_from_place`) gives the street network as a NetworkX graph. Useful to build realistic zone `NEXT_TO` zone links and road distances for our Graph DB, or to map the Twin city onto a real district |

**Lower priority / optional:**
- **OpenAQ** (open API v3, free key) gives real PM2.5 / NO2 / O3 time series from city stations worldwide, including Tunis if a station reports. It's a normal outdoor air-quality baseline and can catch real smoke events (wildfires). Hourly, so slower than our sensors.
- **Open Power System Data – time series** (open, 2015–2020, hourly national load) is an alternative to #5, aggregated at country level.
- **TrafficNet / TrafficNet-2024** (IEEE DataPort) is a larger PeMS incident set (about 584 k incident records) but heavily imbalanced. Only worth it if #4 isn't enough.
- **data.gov.tn** (Tunisian national portal, CKAN API) had no air-quality, traffic or flood time series in our search. It could still be worth a direct search for "inondation", "trafic" and "qualité de l'air" if the jury values local data.

## 2. Best opportunity: NYC as one consistent city

Several open NYC datasets share **the same city, clock and coordinates**:

| Domain | NYC dataset |
|---|---|
| Flood (sensor) | FloodNet (already downloaded) |
| Flood (calls) | 311 Street Flooding / Catch Basin complaints |
| Accidents | Motor Vehicle Collisions – Crashes |
| Traffic speed | NYC DOT traffic speed (E-ZPass segments, about 110 road segments; archive 2021–2024, check if still updated) |
| City map | OSMnx graph of a borough |

**Concrete cross-domain scenario:** pick a heavy-rain night (for example the **remnants of Hurricane Ida, 1–2 Sep 2021**, which FloodNet covers). Take the FloodNet depth curves in one neighbourhood, the 311 flooding complaints there, the collisions nearby in the same hours and the DOT speeds on adjacent segments. That's a real "flood that disrupts traffic" case, replayable through the mock, showing that the Brain links incidents across zones through the graph. It is also strong material for the report and the jury demo.

## 3. Suggested next steps

1. Download **#1 (smoke)**, **#5 (power load)** and **#8 (USGS gauge)**. They are small or quick and fill the three sensor types that have no real data yet (`air_quality`, `power_load`, calm `water_level`).
2. Build the **NYC Ida scenario** from FloodNet + #2 + #3 (all open, same API).
3. Use **#4** and **#7** only for evaluation (recall, early detection), not for tuning, so the test stays independent. This is the PDF's advice: evaluate on scenarios not used to build the reference library.
4. Use **#10** if the Graph DB needs a realistic map beyond the Twin's city description.
5. Keep a `datasets/SOURCES.md` with each source's licence and required citation (UTD19, NAB and UCI all ask for attribution).
