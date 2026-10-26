# Datasets batch 2: download and analysis results

This follows [`datasets-additional-candidates.md`](datasets-additional-candidates.md). Downloaded and analysed on 19 Oct 2026: the **smoke sensor** set, **UCI power load**, a **USGS river gauge**, and the **NYC Hurricane Ida night** (311 + collisions + FloodNet).

| Dataset | Size | Verdict |
|---|---|---|
| Smoke Detection IoT (Kaggle, GitHub mirror) | 5.8 MB, 62,630 rows | **Low–medium.** Gives value ranges only; labels unreliable for training |
| UCI ElectricityLoadDiagrams 2011–2014 | 711 MB, 370 clients × 140,256 slots | **High.** Real daily load curves and noise levels for `power_load` |
| USGS 01403060, Raritan River at Bound Brook NJ, 2021 | 35,000 points, 15-min | **High.** Calm baseline + a record flood (Ida) in one series |
| NYC Ida night (1–2 Sep 2021) | 6,275 calls + 3,727 crashes + 5 FloodNet events | **Very high.** A real cross-domain scenario for the demo |

---

## 1. Smoke Detection IoT dataset

**Content:** 1 Hz readings: temperature, humidity, TVOC (ppb), eCO2 (ppm), raw H2, raw ethanol, pressure, PM1.0, PM2.5, particle counts (NC0.5/1.0/2.5), `Fire Alarm` 0/1.

**Problems found:**
- **71.5 % of rows are "fire"**, which is the reverse of real life.
- There are only **5 recording sessions** and the label changes just **10 times** in 62,630 rows. Labels mark long blocks (whole sessions of several hours), not individual fire events.
- "Fire" sessions include readings at **−14 °C** (recorded outdoors or in varied conditions), so the label is mixed up with the environment.
- The best single-feature rule is **pressure > 937.6 hPa (88 % accuracy)**. Pressure can't detect fire, so this proves the labels **leak through the session**. Any model trained on it learns "which session", not "is there a fire".

**Useful value ranges** (medians, no fire → fire):

| Feature | No fire (median / p90) | Fire (median) | Comment |
|---|---|---|---|
| TVOC (ppb) | 86 / 9,014 | 1,103 | Strongest real signal, but no-fire also spikes |
| PM2.5 (µg/m³) | 1.5 / 2.3 | 1.9 | Barely changes: indoor smouldering, not open fire |
| eCO2 (ppm) | 400 / 454 | 404 | Not discriminative |
| Humidity (%) | 46 / 54 | 51 | Weak |

**Use for us:**
- **Mock:** ranges for an `air_quality` sensor in a realistic noisy state (TVOC baseline about 100 ppb, spikes to thousands even without fire).
- **Detection (A):** confirms that **one air-quality reading alone is not enough for `fire`**. Keep the rule "air quality abnormal **and** fire call / second signal".
- **Don't** use it to train or set thresholds; say so in the report if we cite it.

## 2. UCI ElectricityLoadDiagrams 2011–2014 (Portugal, CC BY 4.0)

**Content:** 370 clients, kW averaged per 15 min, 2011–2014 (Portuguese local time). 210 clients only start after June 2011 (zeros before they were connected).

**Aggregate daily profile** (weekday, % of peak):

```
00h 55 · 03h 44 · 06h 50 · 08h 60 · 10h 88 · 12h 94 · 15h 96 · 18h 100 · 21h 93 · 23h 70
```

Night is about 45 % of peak, the rise is between 8h and 10h, and the peak is at about 18–19h. Weekends are almost identical in the aggregate. Individual clients differ a lot: one office-like client drops to 9 % at night and peaks at 13h; another (MT_010) has a clear evening peak at 19h.

**Noise and variability:**

| Level | Deviation from same-slot median (p5 / p95) | 15-min step change (median / p99) |
|---|---|---|
| Aggregate (370 clients) | −14 % / +44 % | 2 % / 16 % |
| Single large client (MT_200, MT_300) | −20 % / +25 % | 3 % / 30 % |
| Single small client (MT_100, MT_362) | −40 % / +100 % | 5 % / 75 % |

- **Seasonality and growth:** 282 days are more than 20 % off the typical daily total. They are mostly **summer heat (July 2013: +52 %)** and **holidays (25 Dec: −40 %, 1 Jan: −38 %)**.
- **Use for us:**
  - **Mock:** replay one large client or the aggregate scaled to our substation as `power_load`. That's a real normal curve with real noise.
  - **Detection (A):** a substation-level load moves up to **~16 % in 15 min normally** (p99). So `power_problem` needs a larger or sustained deviation from the **same-time-of-day** baseline, and holidays and heat waves will look abnormal: detect a power problem only with a second signal (fire, outage, Guardian).
  - It complements the smart-grid set: that one gave the *attack* pattern, this one gives the *normal* pattern.
- **Limits:** no outages or faults labelled. Values are kW per 15 min (divide by 4 for kWh).

## 3. USGS 01403060: Raritan River at Bound Brook, NJ (2021)

**Content:** gage height (ft) every 15 min, all of 2021, with data quality codes.

| Measure | Value |
|---|---|
| Calm stage (deciles) | 17.1–19.7 ft (median about 17.7) |
| Normal 15-min change | p1 −0.06 / p50 0.00 / p99 +0.08 ft; **February std 0.017 ft** |
| Ida | rise starts 1 Sep 19:45 (from 17.9 ft) → **peak 42.13 ft on 2 Sep 12:00** (+24 ft in 16 h) |
| Fastest rise | **+1.58 ft in 15 min** (1 Sep 20:30), about 90× the normal p99 |
| Time above 35 / 40 ft | 14 h / 3.8 h |
| Other "high water" episodes (> +5 ft) | 6 smaller ones in 2021 (Jan, Mar ×2, Jul, Aug [Henri], Oct). Good **"rise that's not a disaster"** cases |

**Use for us:**
- **Detection (A):** the clearest real example of "abnormal **and rising**". The noise is tiny (std 0.017 ft), so the EMA 3σ rule fires on Ida within 1–2 readings. The 6 smaller rises give **moderate** incidents (test severity levels), and a calm month gives the "calm day: no incident" test.
- **Mock:** scale ft → m and speed up time to get the `water_level` port sensor. This is the calm baseline FloodNet lacks.
- **Limits:** a river gauge, not a street sensor. US units. Flood-stage thresholds come from the US weather service, not from this file.

## 4. NYC Hurricane Ida night (1–2 Sep 2021): a real cross-domain case

Sources: NYC 311 Service Requests (flood-related + traffic-signal types), NYPD Motor Vehicle Collisions, FloodNet (already downloaded). Window: 1 Sep 18:00 → 2 Sep 06:00 local time.

**311 calls: normal day vs Ida night (12 h):**

| Call type | August average per day | Ida 12 h | × |
|---|---|---|---|
| Sewer backup | 57 | **1,524** | 27× |
| Street flooding | 19.5 | **471** | 24× |
| Catch basin clogged / flooding | 30 | 153 | 5× |
| Water in basement | 2.8 | 119 | 42× |
| **Traffic signal controller failure** | 61 | **231** | 4× in half a day |

Flood calls by hour: 19h 29 → 20h 47 → **21h 221 → 22h 582** → 23h 452 → 0h 338 → 1h 165 → 3h 30, then a second wave in the morning (9h 262) as people discover damage.

**Collisions:** 160 in the 12 h window against a typical 124 (+29 %). There are spikes at 19h (30 vs 14.5) and midnight (26 vs 12.7). "Pavement slippery" is among the top factors. The effect is moderate: many people stayed off the roads.

**FloodNet sensors** (9 deployed at the time; 5 recorded an event):

| Sensor | Flood start | Max depth | Time to peak | 311 flood calls within 1 km |
|---|---|---|---|---|
| BK – 9th St / Smith St | 20:11 | 27.8 in | 135 min | 14 (first at 20:08) |
| BK – Hoyt St / 5th St | 21:24 | 10.4 in | 17 min | 17 |
| BK – Carroll St / 4th Av | 21:27 | **35.6 in** | 21 min | 27 |
| Q – Russell St 2 | 21:51 | 2.9 in | 20 min | 0 |
| Q – Russell St 1 | 22:03 | 1.5 in | 36 min | 0 |

**What this shows (useful for the report and the demo):**
1. **Sensor and calls agree in time.** The first flood calls near Gowanus (20:08) arrived 3 minutes before the first sensor event (20:11). Combining both raises confidence fast, which is exactly our "water abnormal + flood call" rule.
2. **Neighbouring zones.** The three Gowanus sensors are within 1 km of each other and flood within 1 h 15. That's a natural test for the graph's `NEXT_TO` links: one incident spreading to neighbours, **not three duplicates** if they're in the same zone.
3. **Sensor without calls.** The Russell St sensors saw shallow water (< 3 in) with no nearby calls. That's a realistic **low-severity / ambiguous** case.
4. **Cross-domain chain.** Flooding → **traffic signal failures (4×)** → more collisions (+29 %). That's flood → power/traffic → accident, the kind of linked chain the graph's `/chain` and `/context` endpoints should show.

**Use for us:** build a **"Storm night" scenario** for the mock:
- Replay the 3 Gowanus depth curves as 3 `water_level` sensors in neighbouring zones.
- Turn a sample of the 311 flood calls in the same hours (with their text) into `call` messages.
- Add a "signal controller offline" event and a few collisions.
- Compress 12 h into about 10 min.

All of it is real, timestamped and geolocated.

---

## 5. Recommendations

| For | Use | Settings to put in `config/detection.yaml` |
|---|---|---|
| `water_level` | USGS Raritan (calm + moderate + Ida), FloodNet curves | Noise std ~0.02 ft / 15 min; "rising" = > 5× normal p99 step for 3 readings |
| `power_load` | UCI aggregate or a large client | Same-time-of-day baseline; normal step ≤ 16 % per 15 min; require a second signal |
| `air_quality` | Smoke set ranges only | TVOC baseline ~100 ppb with spikes; never open `fire` on air quality alone |
| `traffic_*` | UTD19 Torino (batch 1) | See `datasets-utility-review.md` §4 |
| Demo scenario | NYC Ida night | Storm night: flood + calls + signals + collisions, 3 neighbouring zones |

**Licences / citations:**
- UCI (CC BY 4.0, cite the dataset)
- USGS and NYC Open Data (public domain / open; acknowledge the source)
- Smoke set (Kaggle, CC0 per the original page; check before citing)

**Files:** all extracts are in the session scratchpad (temporary):
`/tmp/claude-1000/-home-houssein-Desktop-TSYP-CSXCNXYP/872a9597-1f52-4fbd-af79-8fd54cb1c216/scratchpad/{smoke,uci,usgs,nyc}/`.
Before it's cleared, copy the small ones into the repo (`brain/scenarios/data/`): USGS 1.5 MB, NYC about 3 MB, FloodNet 6 MB.
