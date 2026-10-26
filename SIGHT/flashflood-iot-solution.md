# SAYL — Flash-Flood Early Warning for Tunisian Wadis
### NEXUS (TSYP14 · IEEE SIGHT) — Solution concept & Phase 1 report blueprint

> **SAYL** (سيل) is Arabic for a torrent or flash flood. The working name can be changed.
>
> ⚠️ **Phase 1 is due on 12 Oct 2026, 7 days from now, and missing it means elimination.** Section 12 has a day-by-day plan for writing the report.

---

## 1. The problem in one paragraph

Flash floods are Tunisia's costliest hazard. Floods caused about **60% of disaster-related economic losses between 1957 and 2018**, and more than 560,000 people were affected. The deaths are rarely caused by a lack of rain data. They happen because the warning does not reach the person at the wadi crossing in time:

- **Cap Bon / Nabeul, 22 Sep 2018.** About 200 mm of rain fell on Nabeul and 225 mm on Beni Khaled, the most since records began in 1995. Water rose 1.7 m and **5 people died**. Two sisters were swept away as they left a factory in Bou Argoub, and a man drowned near Takilsa. A national warning had gone out the day before. Residents also said the wadis had been **left unmaintained for decades and were clogged with trees, rubbish and rubble**.
- **Sep 2020 (Monastir, Sousse, Mahdia, Tunis, Kairouan):** 6 or more deaths and more than 40,000 people affected.
- **18–20 Jan 2026:** the heaviest rain in parts of the country since 1950. **5 deaths (4 in Moknine, 1 in Nabeul)**, 15 governorates and about 25,000 people affected, 105 roads affected in Monastir, about 350 rescues, and schools closed.

**The gap:** a weather warning covers a whole governorate. Nobody tells the person at *this* crossing that the water is arriving in *25 minutes*. SAYL fills that last kilometre.

---

## 2. The solution

SAYL is a low-cost network of solar-powered sensor nodes that **watches a whole wadi catchment, not only the river**. It covers three things:

1. **Upstream catchment nodes.** These measure *how much rain is falling* and *how much more water the soil can absorb*. Saturated soil means almost all of the rain becomes runoff, and this is the earliest sign of a flash flood.
2. **River nodes at bridges and crossings.** A non-contact radar measures **water level and surface velocity**. From these the node computes **discharge (m³/s)** and detects the flood front as it arrives.
3. **Gateway and alerts.** A gateway at the municipality or Civil Protection fuses the data, predicts *when* the water will reach the town, and alerts people through SMS, voice calls in Tunisian Darija, a dashboard, and **sirens and flashing beacons at the crossings themselves**. The beacons still work when the internet and the power grid are down.

```
 RAIN + SOIL (upstream)         RIVER (bridges, crossings)        PEOPLE
 ┌──────────────────┐   LoRa    ┌───────────────────────┐   LoRa   ┌───────────────────┐
 │ Catchment node   │ ───────▶  │ River node            │ ──────▶  │ Gateway (mairie / │
 │ rain gauge       │           │ 60 GHz radar:         │          │ Civil Protection) │
 │ soil moisture ×3 │           │  level + velocity     │          │ fusion, ETA, log  │
 │ pressure/temp/RH │           │ discharge, dh/dt      │          └───┬─────┬─────┬───┘
 │ solar + battery  │           │ siren + beacon        │◀─ LoRa ──────┘     │     │
 └──────────────────┘           └───────────────────────┘  (offline loop)    │     │
                                                                  SMS / voice│     │4G/Internet
                                                          households, factories,   ▼
                                                          farmers, schools    Dashboard, INM
                                                                              forecast, open data
```

**The pipeline the challenge asks for:** Detect (soil and rain, then river) → Communicate (LoRa, then SMS/4G) → Coordinate (gateway dashboard for municipality and Civil Protection) → Enable response (local siren, Darija voice alert, evacuation of the crossing).

---

## 3. What we measure and why

| Parameter | Sensor (low-cost) | Why it matters for flash floods |
|---|---|---|
| **Soil moisture** at 10, 30 and 60 cm | Waterproof capacitive probes (e.g. DFRobot SEN0308), calibrated on site against oven-dried samples | Gives a **Soil Saturation Index**. On saturated soil a moderate storm causes a big flood; on dry soil the same storm may not. This is the main factor the weather forecast misses. |
| **Rainfall intensity** (mm per 5, 15 and 60 min) and accumulated rain | Tipping-bucket rain gauge (0.2–0.3 mm per tip) | Flash floods follow *intensity*, not daily totals. Cumulative rain is compared with what the soil can still absorb. |
| **Water level h** and **rate of rise dh/dt** | Acconeer **XM125 (A121, 60 GHz pulsed radar)**, about 21 USD, pointing down from a bridge. Ultrasonic JSN-SR04T as a cheap fallback. | The classic flood indicator. dh/dt gives the earliest warning at the river. |
| **Surface water velocity v** | The **same XM125**, tilted 35–45°, using Acconeer's *surface velocity* example application | Velocity, not depth, is what knocks people over and sweeps cars away. Hazard to people ≈ h × v. |
| **Discharge Q** | Computed: Q = k · v_surface · A(h), with k ≈ 0.85 and A(h) from a one-off survey of the cross-section | Lets us compare with design flows and historical floods. Agencies understand m³/s. |
| **Blockage signature** | Derived: level rising while velocity falls | Shows debris or a clogged culvert backing water up, which made the 2018 floods worse. Triggers a **maintenance alert** to the municipality, so the system also helps between floods. |
| **Air pressure, temperature, humidity** | BME280 | A sharp pressure drop or sudden cooling marks a convective storm. Also used to compensate the sensors. |
| *(optional)* **Turbidity** | DFRobot SEN0189 in a protected side pipe | A surge of sediment often arrives just before the flood peak. Optional because sensors in the water get destroyed. |
| **External data** (gateway) | Open-Meteo / INM rain forecast, GPM-IMERG satellite rain, Copernicus GloFAS | Adds hours of lead time on top of minutes. Ground sensors confirm or rule out the forecast. |

**Why radar and not ultrasonic or float sensors:** nothing touches the water, so the flood cannot destroy the sensor. It is not affected by wind or temperature the way ultrasonic is. **One 21 USD chip measures both level and velocity**, where a commercial radar flow station costs thousands. This is our strongest technical-innovation argument.

---

## 4. Detection logic (edge + gateway)

### 4.1 On the catchment node
- **Soil Saturation Index:** SSI = (θ − θ_wilting) / (θ_saturation − θ_wilting), a weighted average over the three depths, from 0 (dry) to 1 (saturated).
- **Continuous antecedent moisture.** The standard SCS Curve-Number runoff method uses only 3 discrete moisture classes (AMC I/II/III). We **adjust CN continuously using the SSI we measure**, then compute the expected runoff from the measured rain:
  `S = 25400/CN − 254`, `Q_runoff = (P − 0.2S)² / (P + 0.8S)` when P > 0.2S.
- **Adaptive sampling:** one reading every 15 min in normal weather, every 1 min when it rains more than a set threshold or the pressure falls sharply. This saves battery and still captures events.

### 4.2 On the river node
- Level h, dh/dt, velocity v, discharge Q and the h × v hazard index.
- **Flood-front detection:** dh/dt above a threshold *and* a jump in v. When this happens the node sends an immediate priority message instead of waiting for its schedule.

### 4.3 On the gateway (fusion)
- **Lead time (ETA):** when the flood front is detected upstream, the gateway estimates arrival at the town. ETA = channel distance / wave speed, and the wave speed is calibrated from each event the system records.
- **Risk state machine with hysteresis**, so alerts do not flicker on and off:

| Level | Example trigger (calibrated per site) | Action |
|---|---|---|
| 🟢 Normal | — | Routine logging; irrigation and drought advice for farmers |
| 🟡 Watch | INM/Open-Meteo forecast of heavy rain **and** SSI > 0.6 | Dashboard notice; municipality checks the wadi for blockages |
| 🟠 Warning | Rain intensity > X mm/h on soil with SSI > 0.8, **or** water rising upstream | SMS and voice alert to subscribers; Civil Protection on standby |
| 🔴 Danger | Flood front detected, or h × v at a crossing above the safe limit | **Sirens and beacons at crossings**, mass SMS and calls, factories and schools hold people inside |

- **AI layer (honest scope):** at first the thresholds are rules, because no local training data exists yet. Each event SAYL records becomes labelled data. We then train a small model (gradient boosting or a tiny LSTM) on the gateway, and use historical DGRE/INM series where we can get access. We will not claim "AI" that we cannot train.

---

## 5. Communication and resilience

- **LoRa 868 MHz** (EU863-870 plan, licence-exempt in Tunisia): ranges of several km, milliwatt power. Alert messages are **confirmed (acknowledged) and retried**. Nodes can relay for nodes that have no direct line of sight.
- **Offline-first loop:** if 4G or the internet fails, the gateway still turns on the sirens and beacons at the crossings over LoRa. If the gateway fails, **each river node triggers its own siren** from its own readings. Every layer can work without the layers above it.
- **Gateway:** Raspberry Pi with a RAK LoRa concentrator, a 4G modem with SMS fallback, and a battery backup lasting 24 h or more. It is hosted at the municipality or the Civil Protection post.
- **Alert channels for inclusion:** SMS in Arabic and French, **pre-recorded voice calls in Darija** (for elderly people and people who cannot read), Telegram or WhatsApp for those who want them, and **visual beacons plus sirens** (for deaf people and passers-by without phones). Mosque loudspeakers or the municipal PA system can be added if the community agrees.

---

## 5b. From alert to action

The brief asks for **Detects → Communicates → Coordinates → Enables Response**. An alert alone covers only the first two steps. SAYL acts on three levels:

**1. Automatic local actions (fast, low-risk, reversible, no human needed)**
| Trigger | Automatic action |
|---|---|
| 🔴 at a crossing (h × v above the safe limit) | Siren and flashing **"DO NOT CROSS / ممنوع العبور"** sign at the ford or low bridge; optional **motorised road barrier** (like a railway crossing) |
| 🟠 or 🔴 | Factory and school sirens or relays: **"stay inside, do not leave"** (the 2018 victims were leaving a factory) |
| 🔴 in an underpass or at a stormwater pump | Turn on drainage pumps; switch the underpass light to red |
| Blockage signature (between floods) | Ticket sent to the municipality: "clear the culvert at bridge X" |

**2. Coordinated human actions (the system helps people decide)**
- Civil Protection dashboard shows *which* crossing, *how many minutes* until the water arrives, and *how much water* (m³/s), with a suggested response playbook: close road X, send a team to Y, open shelter Z.
- Dam and hydraulic-works operators (DGBGTH) get upstream flow data to decide on releases. **We never control gates automatically.** High-stakes decisions stay with humans.
- One-tap "confirm / cancel" for the duty officer, which reduces false alarms and keeps a record.

**3. Telling people what to do, not only that there is danger**
Every message carries an instruction: *"Flood reaching Oued Souhil bridge in ~20 min. Do not cross. Move away from the wadi bed. Shelter: Ecole X."* The same message is sent as SMS, as a Darija voice call, and shown on the beacon.

**Design rule:** automate only what is fast, safe and reversible (sirens, signs, barriers, pumps). Keep a human in the loop for everything else (evacuations, dam releases). The report should state this rule explicitly; it scores on *Ethics & technology*.

---

## 6. Hardware and power

| Item | Prototype | Field version |
|---|---|---|
| MCU + LoRa | Heltec WiFi LoRa 32 (ESP32), quick to develop on | RAK3172 (STM32WL), sleeps at µA |
| Radar | XM125 eval board | XM125 module on our own PCB |
| Power | 6 W solar panel + 1 LiFePO4 cell (3.2 V, 6 Ah) + MPPT charger | Same, sized for **5 days without sun** |
| Enclosure | IP65 junction box | IP67, UV-resistant, bolted under the bridge deck (hard to steal or vandalise) |
| Firmware | Arduino/PlatformIO | Zephyr or STM32Cube, watchdog, over-the-air config through LoRa downlink |

**Power budget (river node, rough estimate):** sleeping at about 20 µA, plus one radar burst and one LoRa uplink every 15 min, gives an average of a few mA in normal mode. That is several weeks of autonomy on the battery alone, so the solar panel has plenty of margin. *Measure this on the prototype and put the measured numbers in the Phase 2 report. Judges like real numbers.*

---

## 7. Target site (pick one and write about it concretely)

**Recommended: the Cap Bon / Nabeul wadi system** (for example Oued Souhil through Nabeul city, and the Beni Khaled / Bou Argoub catchments). It had record rain and deaths in 2018, a factory-worker tragedy, documented wadi clogging, and was hit again in 2026. The case study is strong and easy to document.
**Alternative: Moknine (Monastir)**, which had 4 of the 5 deaths in Jan 2026 and is very recent and dramatic. It is a flatter, more urban flood-runoff case, though, so the river-velocity part fits less well.

Pilot layout: **4 catchment nodes** upstream (spread across soil and land-use types), **3 river nodes** (upstream bridge, mid-reach, and the town crossing or the factory-zone road), and **1 gateway** at the municipality.

---

## 8. Managerial section (10 pts)

### 8.1 Mission / Vision / Values
- **Mission:** Give every community along a Tunisian wadi the minutes it needs to get out of the water's way.
- **Vision:** No Tunisian is killed by a flood they could have been warned about.
- **Values:** *Open* (open hardware, firmware and data) · *Local* (built, installed and maintained by local people) · *Inclusive* (alerts for people who cannot read, deaf people, people without a phone) · *Frugal* (affordable for municipalities) · *Honest* (transparent thresholds and a public record of false alarms).

### 8.2 Team roles (3–5 people, including the required SIGHT, Systems Council and CEDA members)
| Role | Owns | Society fit |
|---|---|---|
| Systems lead / PM | Architecture, requirements, risk register, timeline | **Systems Council** |
| Embedded & PCB engineer | Node firmware, low-power design, PCB, radar integration | **CEDA** |
| Comms & backend engineer | LoRa network, gateway, alert engine, dashboard | — |
| Hydrology & data lead | Thresholds, SCS-CN model, sensor calibration, data analysis | — |
| Community & business lead | Municipality partnership, surveys, market and finance, video | **SIGHT** |

### 8.3 Market analysis
- **Customers (who pays):** municipalities (budgets for risk and wadi maintenance), the **Civil Protection office (ONPC)**, the Ministry of Agriculture (CRDA, DGBGTH dams and hydraulic works), industrial zones and factories (duty of care for workers, as at Bou Argoub), insurers (fewer claims), and agricultural cooperatives (GDA).
- **Data partners:** INM (forecasts), DGRE (hydrometric history), universities (INAT, ENIT hydrology labs).
- **Funders:** GIZ, UNDP, World Bank resilience programmes, Green Climate Fund and adaptation-fund projects in Tunisia, and EU programmes. All of these finance early-warning systems in the region.
- **Competition:** national hydrometric stations (accurate, but sparse and expensive, so they do not reach the last kilometre), commercial IoT flood sensors from Europe and the US (import costs, no local maintenance, single sensor), and weather apps (forecast only, no ground truth). **SAYL's niche** is dense coverage, low cost, the whole catchment (soil + river), offline operation, and local maintenance.
- **Year-round value:** flash floods happen a few days a year. In the dry season the same soil-moisture and rain data **feeds irrigation and drought advice to farmers**. The network therefore earns its keep all year, which answers "why pay for something used 3 days a year?"

### 8.4 Budget (estimates at about 3 TND/USD; check against local suppliers)
| Unit | Approx. cost (TND) |
|---|---|
| Catchment node (rain gauge, 3 soil probes, BME280, MCU+LoRa, solar, battery, enclosure, pole) | ~450 |
| River node (XM125 radar, MCU+LoRa, solar, battery, IP67 box, bridge mount, siren + beacon) | ~500 |
| Gateway (Pi + LoRa concentrator + 4G modem + UPS battery) | ~900 |
| **Pilot: 4 catchment + 3 river nodes + 1 gateway + installation and contingency (~25%)** | **~5,500** |
| **Phase 2 prototype** (1 catchment node, 1 river node, gateway, test flume) | **~1,200** |

### 8.5 Business model and ROI
- **Model:** hardware sold close to cost, plus an **annual "early warning as a service" subscription** per municipality (for example 3,000–6,000 TND/year covering maintenance, SMS/voice credits, hosting, recalibration and training of local volunteers). **Alerts are always free for households.**
- **Extra revenue:** premium agronomic data for cooperatives, risk reports for insurers and factories, and grant-funded deployments.
- **ROI argument:** compare a pilot at about 5–6k TND against **one** avoided death, the damage to a factory or a flooded road, and the cost of emergency rescues. The World Bank / WMO rule of thumb is that early-warning systems return several times their cost. *Cite the exact source in the report.* Build a simple 3-year table: number of municipalities, revenue, costs, and break-even year.

### 8.6 Risk register (main risks)
| Risk | Mitigation |
|---|---|
| A node is destroyed by the flood | Non-contact radar mounted above the highest recorded flood level; the electronics never touch the water |
| Theft or vandalism of solar panels | Mount under the bridge deck or on municipal buildings; small panels; community ownership ("the neighbourhood's node") |
| False alarms → people stop trusting alerts | Several conditions must agree, hysteresis, public log of false alarms, thresholds reviewed after each season |
| No historical data for calibration | Start with rules and published thresholds, then learn from each recorded event; ask DGRE and INM for data |
| Cheap soil probes drift | Calibrate on site against gravimetric samples, recalibrate each season, cross-check with neighbouring nodes |
| Coverage holes (hills block LoRa) | Site survey, relaying between nodes, a second gateway |
| Permissions to mount on bridges | Municipal partnership and an agreement with the Ministry of Equipment |
| Personal data (subscriber phone numbers) | Opt-in only, minimal data, stored locally, never sold |

---

## 9. Humanitarian impact and SDGs (10 pts + bonus)

- **Real need:** Section 1 (deaths in 2018, 2020 and 2026). **Run a short survey** of residents and factory workers in the pilot area before the deadline, even 20–30 answers. Ask how they heard about past floods and what channel they would use. This is powerful evidence.
- **Inclusion:** voice alerts in Darija, visual beacons, sirens, no smartphone required, women factory workers (2018 victims) as a priority group, and farmers.
- **Empowering local actors:** **"wadi wardens"**, volunteers trained to clean the sensors, replace batteries and report blockages. Open designs so a local technician can repair a node with parts available in Tunisia.
- **SDGs (aim for 2 or more to get the bonus):**
  - **SDG 11.5:** reduce deaths and losses from disasters.
  - **SDG 13.1 / 13.3:** resilience and adaptation to climate hazards; awareness.
  - **SDG 6.4 / 2.4:** soil moisture data for efficient irrigation and resilient farming.
  - **SDG 9.1:** resilient, affordable infrastructure.
  - **SDG 17.17:** partnerships between municipality, Civil Protection, university and community.
- **Bonus (+3):** get a **written letter or signed MoU from a municipality** (Nabeul, Beni Khaled, Moknine…) or a local association. Even a letter of interest counts as documented collaboration. **Start this today.**

---

## 10. Ethics and values (10 pts)

- **Equity:** alerts are free for everyone. Placement of nodes favours the most exposed and poorest neighbourhoods, not only the city centre.
- **Transparency:** open-source firmware and hardware, published alert thresholds, an open-data portal (anonymised), and a public log of every alert and false alarm.
- **Sustainability:** solar power, long-life LiFePO4 batteries, repairable modular design, and a recovery and recycling plan for old nodes.
- **Wellbeing:** fewer deaths, less anxiety ("trusted, specific alerts instead of vague red warnings"), and safer commutes for workers.
- **Community ownership:** wadi wardens, municipal ownership of the network, co-designing alert messages with residents.

---

## 11. Phase 2 prototype and demo plan (to keep in mind)

- **Tabletop flume:** a PVC gutter or half-pipe with an aquarium pump and an adjustable valve. The XM125 above it shows level and velocity live, and the flow can be increased to trigger 🔴.
- **Soil box:** a tray of soil with the moisture probes. A watering can acts as "rain" and the SSI rises on screen.
- **End-to-end demo in 2 min:** rain on wet soil, then 🟠 SMS to a judge's phone, then the flume surges, then 🔴 siren and beacon go off. Then **unplug the internet** to show the local siren still works offline.
- **GitHub:** firmware, gateway code, KiCad schematics and PCB, calibration notebooks, and the power-budget measurements.

---

## 12. Phase 1 report: 7-day plan (deadline 12 Oct)

**Report outline (≤ 30 pages), with page budget matched to the points:**
1. Executive summary + Mission/Vision/Values (1.5 p)
2. Problem and context: Tunisian floods, target site, survey results (3 p)
3. Solution overview + system architecture diagram (3 p)
4. Technical design: sensors, detection logic, comms, power, edge/AI (6 p) → **15 pts**
5. Methodology and tools: systems engineering (V-model, requirements table, SysML/block diagrams), KiCad, PlatformIO, ChirpStack (2 p)
6. Humanitarian impact and SDGs (3 p) → **10 pts**
7. Ethics and values (2 p) → **10 pts**
8. Market analysis, business model, partners (3 p)
9. Budget, financial analysis and ROI (2 p)
10. Team roles, timeline (Gantt chart to Dec 2026 and a pilot in 2027), risk register (2.5 p) → **10 pts**
11. Conclusion + references (1 p)

| Day | Task |
|---|---|
| **Mon 6 Oct** | Lock the name and target site. Split the sections between team members. Email the municipality and Civil Protection for a letter. Launch the survey (Google Form in Arabic). |
| **Tue 7** | Write sections 2–4. Draw the architecture and node block diagrams (draw.io / FigJam). |
| **Wed 8** | Write sections 5–7. Get prices for the BOM from Tunisian suppliers. |
| **Thu 9** | Write sections 8–10: market, finance, Gantt chart, risks. |
| **Fri 10** | Add the survey results. Full read-through for flow and concise language. Check anonymity (no names, no school, no SB). |
| **Sat 11** | Final layout to PDF. Record the 2-min video (voiceover, no faces) if time allows. |
| **Sun 12** | **Submit early in the day.** Do not wait until midnight. |

---

## Sources
- [ReliefWeb: Tunisia flash floods, Sep 2018](https://reliefweb.int/disaster/ff-2018-000158-tun)
- [FloodList: Nabeul floods, Sep 2018](https://floodlist.com/africa/tunisia-floods-nabeul-september-2018)
- [France24: record rains, Cap Bon 2018](https://www.france24.com/en/20180924-tunisia-weather-cap-bon-record-rains-set-off-deadly-flash-floods-nabeul)
- [Middle East Online: five killed (wadi clogging)](https://middle-east-online.com/en/five-killed-tunisia-flash-floods)
- [Wikipedia: Floods in Tunisia (60% of losses, 2020 event)](https://en.wikipedia.org/wiki/Floods_in_Tunisia)
- [Africanews: Jan 2026 floods, heaviest rain in 70+ years](https://www.africanews.com/2026/01/21/at-least-four-dead-in-tunisia-floods-after-heaviest-rainfall-in-over-70-years/)
- [The New Arab: 2026 death toll rises to five](https://www.newarab.com/news/tunisia-flood-death-toll-rises-five-four-missing)
- [ACAPS: Tunisia](https://www.acaps.org/en/countries/tunisia)
- [Acconeer docs: A121 surface velocity example](https://docs.acconeer.com/en/latest/example_apps/a121/surface_velocity.html)
- [Acconeer: surface velocity measurement](https://acconeer.com/innovation_lab/surface-velocity-measurement/)
- [DigiKey: XM125 module](https://www.digikey.com/en/product-highlight/a/acconeer-ab/entry-module-xm125)
- [Early warning of impending flash flood based on AIoT (EURASIP JWCN)](https://jwcn-eurasipjournals.springeropen.com/articles/10.1186/s13638-022-02096-5)
- [LoRa-based IoT sensor node for real-time flood EWS](https://www.researchgate.net/publication/358678804_Lora-based_IoT_sensor_node_for_Real-time_Flood_Early_Warning_System)
- [Calibration of low-cost capacitive moisture sensors (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11679601/)
- [OmniPreSense OPS243 Doppler radar (commercial reference)](https://omnipresense.com/product/ops243-doppler-radar-sensor/)
