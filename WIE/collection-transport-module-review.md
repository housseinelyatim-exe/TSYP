# Review: Smart Collection and Transport Optimization Module

**Reviewed:** the build plan for the RuralDirect collection and transport module (pipeline, code layout, build order, resources, risks, feature tables for the location and schedule models)
**Status:** design-stage plan, not a final report
**Reviewed against:** the RuralDirect proposal and the earlier reviews in this folder (`ruraldirect-proposal-review.md`, `ruraldirect-ai-ideas.md`)

---

## 1. Overall assessment

The plan is solid and realistic for a student team. Its strongest points:

- It uses **established operations-research models** (p-median, capacitated VRP with time windows) and standard solvers instead of inventing anything. This is easy to defend.
- It **compares against a baseline in every stage**, with a fixed seed and a config file, so the results can be reproduced.
- The build order is right: assumptions first, then the baseline, then a toy instance you can check by hand.
- It is **honest about the risks**: synthetic data, OSRM, thin OSM data, and "results show the method, not real savings".

The main problems to fix before coding:

1. **Some parts contradict each other**: "four models" against five stages, no school buildings against school hours as a hard rule, and fixed weekly days against a threshold-based dispatch rule (§2).
2. **The baseline is too weak.** "Every producer travels alone to the market" makes the savings look larger than they are (§3).
3. **The p-median setup has three modelling problems**: what it weights by, where point capacity comes from, and what happens when the walking limit makes it infeasible (§4).
4. **Routing over 3–5 points is almost trivial**, so two routing solvers are more effort than the problem needs (§6).
5. **The KPIs are never defined**, even though `evaluate.py` and the whole comparison depend on them (§8).
6. The reliability factor needs **shrinkage and a fairness rule**, otherwise it is noisy and could be used against women whose harvest failed (§7).

---

## 2. Inconsistencies to fix

| Where | Problem | Fix |
|---|---|---|
| Intro vs pipeline table | "Four models that feed each other", but the table has five stages, and stage 1 (data) is not a model | Say "a pipeline of five stages: data preparation and four models" |
| Code layout vs "four people work in parallel" | The stages depend on each other in sequence, so people can only work in parallel if the **file formats between stages are fixed first** | Write the interface (columns and units of `producers.csv`, `sites.csv`, `matrix.npy`, `assignments.csv`, `schedule.csv`) in week 1, and give each person a small fixture file so they don't wait for the previous stage |
| Candidate sites vs schedule model | Sites exclude school buildings, but "class hours and school holidays" is a **hard rule** in the schedule | Explain why. If it is about producer availability (mothers on the school run) or traffic near schools, move it under "producer availability". Otherwise remove it |
| Schedule objective vs dispatch rule | "Keep the same day every week" conflicts with "run when a volume threshold is reached or the deadline passes" | Make the fixed days **the plan**, and the threshold rule an **operational adjustment**: skip a visit below a minimum volume, add one above truck capacity. Say which of the two wins |
| "Nothing needs training" vs the tool list | scikit-learn is listed for k-means and the reliability factor, but the factor is a ratio and k-means isn't used in any stage | Drop scikit-learn, or say what k-means is for (generating candidate sites, or a warm start for p-median) |
| Weather and covered-space flags in the location model | p-median picks **fixed** weekly points, while weather changes per round. A per-round flag can't change a strategic decision | Move the weather flag to the round level: on rain days, producers at an uncovered point are sent to their backup point. Keep "covered space" only as a site attribute |
| Code layout | No `config.py`/`config.yaml`, no `baseline.py`, no map output, although the text needs all three | Add them to the module list |
| Formatting | The heading "Collection point model (p-median)Schedule model" is merged; "travel times.." | Clean up before sharing |

---

## 3. Make the baseline realistic

"Each producer travels alone to the market" is a **straw man**. Many rural women don't make that trip at all today. They sell at the farm gate to an intermediary (collector), share a louage or a relative's vehicle, or don't sell outside the village. Beating a baseline that nobody uses doesn't prove anything to a jury.

**Use two or three baselines:**

| Baseline | What it represents | Main cost |
|---|---|---|
| B1. Travel alone (keep it) | Upper bound of today's cost | Fare or fuel, time, one trip per producer per market day |
| B2. Intermediary at the farm gate | The most common real situation | The intermediary's margin (price gap), little travel |
| B3. Shared informal transport (louage) | What organised women already do | Fare per person and per crate, waiting time |

The real argument for RuralDirect is then **"better price than B2 at a cost close to B3"**. The only number you need from the field contact is a rough farm-gate price against the market price for one or two products.

**Count the same costs on both sides.** The optimised plan must include the producer's **walking time to the point and waiting time there**, not only the truck kilometres. Otherwise the comparison isn't like for like, although the plan says it is.

---

## 4. Collection point model (p-median)

### 4.1 Weight by people, not by volume

A p-median weighted by declared volume pulls points towards the **largest producers**. The walking burden is per **person** and per **trip**, not per kg. Volume weighting therefore works against the smallest producers, who are often the women this project targets.

- Weight walking time by **number of producers × visits per week**.
- Count volume in the **routing cost** (stage 4), where it belongs.
- Report an equity KPI: **the longest walk** and the share of producers above 2 km, not only the total.

### 4.2 Point capacity doesn't come from truck capacity

"Capacity per point: set from truck capacity" mixes two constraints. One truck can visit several points, and one point can be visited by several trips. What limits a point is **its space, its handling staff and the service time on site**. Set point capacity from those (for example crates the site can hold, or producers served in a 2-hour window), and leave truck capacity to stage 4.

### 4.3 Handle infeasibility

With a hard 3 km walking limit and a fixed p, p = 3 may have **no feasible solution**, because some producers are out of range of any three sites. Decide in advance:

- First solve a **set-covering model** to find the minimum p that covers everyone within 3 km. That gives the lower bound for the 3/4/5 comparison.
- Or allow uncovered producers with a large penalty, and report them. In the real system they would get a **farm-gate pickup** (see §6).

### 4.4 The 3 km walking limit

3 km is a long way **carrying produce**: a 20 L can of olive oil weighs about 18 kg, a crate of tomatoes 15–20 kg. Express the limit in **minutes** and make it depend on the load or the means of transport (on foot, donkey cart, a relative's car). Run the sensitivity test at 1.5 / 3 / 5 km. Safety and social acceptability matter as much as distance: the walk and the site should be ones women are comfortable using (not a café, not an isolated road at dusk). Add **"acceptable to women" (yes/no from the survey)** as a hard rule next to permission to host.

### 4.5 Smaller points

- **"Unknown" permission:** run two scenarios, with unknown sites allowed and with them excluded, and report the difference. That shows the field team which permissions are worth chasing.
- **Minimum producers per point:** derive it from the economics. A stop is worth making when the volume collected justifies the service time plus the detour. Compute it once from the config values instead of leaving it "to decide".
- **Backup point:** good idea. Either add it as a constraint (every producer has a second open point within range) or report it as a KPI.

### 4.6 Say that the stages are solved one after another

Choosing points first and routing afterwards is a known simplification of the **location-routing problem**. The p-median doesn't see the truck cost. That's acceptable at this scale, but say it, and **choose p by running the whole pipeline** for p = 3, 4, 5 and comparing total cost (walking + truck + producer time), not by the p-median objective alone.

---

## 5. Schedule model

### 5.1 Give it a formulation

"Assignment of fixed weekly days" describes the goal but not the model. A simple version that fits:

- Each point gets a **visit pattern** from an allowed list: perishables "Mon+Thu" or "Tue+Fri", olive oil and other shelf-stable products "once a week".
- A point's pattern follows its **most frequent product**. Shelf-stable products ride along on the perishables visits.
- Constraints: the market must be open on the arrival day, producers must be available, and each day's load must fit the fleet and the driver's hours.
- Objective: balance the load across days, and keep each point on the same days every week.

This is a small integer program (PuLP or OR-Tools CP-SAT) and needs no new tool.

### 5.2 Schedule and routing depend on each other

A day's assignment is only valid if the routes for that day fit in the truck and in daylight. Add a **simple feedback loop**: if routing fails for a day, move the point with the most slack to its second-best pattern and re-run. Mention it in the build order.

### 5.3 Constraints that are missing

- **Heat and time in transit for fresh produce.** In summer, tomatoes or herbs left at a point at noon spoil quickly. Add a **maximum time between collection and market arrival** for perishables.
- **Seasons.** The olive harvest (November to January) has the shortest days, so daylight is tightest exactly when oil volumes peak. Test a winter week and a summer week.
- **Ramadan and Fridays** change working hours and market activity. Add them as calendar exceptions in the config.
- **Artisanal products.** The module is still designed for agriculture only. Crafts and textiles are not perishable and can ride along on any visit, or go to a locker. Adding a **product profile** (fresh / shelf-stable / artisanal) in the config costs almost nothing and covers the second target group (see the proposal review, §2).

---

## 6. Routing model

### 6.1 The routing instance is very small

With 3–5 collection points and one market, the VRP is almost trivial: there are at most 120 orders of visiting five points. **Running OR-Tools, PyVRP and pyvroom on it is more effort than it gains.**

- Keep **OR-Tools** as the main solver (it handles capacity, time windows, service times, and different start and end locations).
- Use a **brute-force check** on the toy instance instead of a second solver. That is a stronger test than comparing two heuristics.
- Keep PyVRP as optional, or drop it.

To make routing matter, test a **larger instance**: several villages or a whole delegation with 10–20 points, or a **mixed instance** where large or out-of-range producers get farm-gate pickups next to the points. That is also more realistic.

### 6.2 Details to specify

- **Start and end:** where does the truck start (garage, the operator's home, the market)? This is an open VRP or one with a different end point. OR-Tools supports it.
- **Units:** tomatoes in kg or crates, olive oil in litres, crafts in pieces. Use **two capacity dimensions** (weight and volume or crate slots). OR-Tools supports several.
- **Who operates the truck:** the proposal review recommended paid third-party transporters. If so, cost per round (a fixed fee plus per km) matters more than vehicle-km, and **fill rate** decides whether a transporter accepts the round.
- **Service time:** the 20 minutes for a tent is an assumption. Make service time depend on the number of producers and crates at the stop (fixed + per crate), because that is where loading time dominates in small rural rounds.

---

## 7. Reliability and re-planning

### 7.1 The ratio is noisy at the start

A delivered-to-declared ratio from one or two rounds is unreliable. Use **shrinkage towards the group average**: for example corrected ratio = (n × own ratio + k × group ratio) / (n + k), with k around 3–5 rounds. New producers start at the group value and move towards their own value as rounds accumulate. This is still "no training", and it is easy to explain.

### 7.2 Plan for overflow, not only for the average

If you plan with the average corrected volume, about half of the rounds will be over plan. Plan truck capacity at a **higher percentile** (for example the 80th) of the corrected volume, or keep a safety margin in the config.

### 7.3 Fairness rule

A ratio below 1 often means a **bad harvest, sickness or a family emergency**, not cheating. Write it into the design:

- The factor is used **only to correct volumes for planning**. It is never shown as a score and never used to rank, exclude or penalise a producer.
- Producers keep the same point and day whatever their factor.

This fits the gender-inclusive goal and avoids an obvious jury question.

### 7.4 The simulation recovers what you put into it

Because the rounds are simulated, the correction will "work" by construction. Define **producer types** in the generator (reliable, optimistic, erratic, one-off shock) and report how much the correction reduces **overflow and empty capacity** compared with using raw declarations. Say clearly that this tests the mechanism, not real behaviour.

### 7.5 Say what gets re-solved

Re-planning should be **stable**: points rarely change (seasonally), weekly days rarely change, and routes are re-solved every round. Otherwise producers get a different point or day each week, which breaks the "fixed weekly day" objective.

---

## 8. Define the KPIs now

`evaluate.py` is the deliverable the jury will look at, but the plan doesn't list what it measures. A proposed set, computed for every baseline and every scenario:

| Group | KPI |
|---|---|
| Producer | Time per week (walking + waiting + travel), money spent per week, **longest walk**, share of producers within the limit, trips avoided |
| Operator | Vehicle-km per week, cost per kg (or per crate) delivered, fill rate, on-time arrival at the market |
| Product | Time from collection to market for perishables, share above the maximum |
| Environment | CO₂ per kg (vehicle-km × an emission factor stated in the config) |
| Robustness | Overflow rounds and empty capacity, with and without the reliability correction |

Report **time saved per woman per week in hours**. For this challenge it is the most telling number, more than kilometres.

---

## 9. Data and reproducibility

- **Pick the pilot area early.** "Sunrise and sunset for Kairouan" implies the governorate, but the code needs a precise area: one delegation, or a radius around one market town. Everything (OSM extract, INS sectors, market) depends on it.
- **OSRM** is usually easy to run with Docker on the Geofabrik Tunisia extract, which is small. The bigger risk is **missing rural tracks** in OSM, not OSRM itself. Check a few routes against Google Maps or the field contact. For walking, use the OSRM foot profile, or straight line × detour factor; state the factor (about 1.3–1.4 is common for road networks) and test its sensitivity.
- **Truck access** can partly be read from OSM road types (`highway=track`, `surface=unpaved`), then confirmed in the field.
- **Candidate sites from OSM:** post offices and some public buildings are mapped, cooperatives and GDA premises rarely are. Expect a manual list. Your fallback already plans for it.
- **Synthetic producers:** distribute them by INS population per sector (imada). Put the volume distribution, product mix and participation rate in the config.
- **One seed is not enough.** A fixed seed makes one run reproducible, but one random instance is an anecdote. Run **10–30 seeds** and report the mean and spread. Add a **participation-rate** test (30 %, 60 %, 100 % of producers join), because savings depend heavily on density.

---

## 10. Literature and positioning

- Good practice to read the papers before citing them. Give **full references** (authors, year, venue, DOI) in the final document, and verify the Kolfa/ICARDA precedent before naming it.
- Add the keyword **location-routing problem** to the search. It is the formal name for what stages 2–4 approximate, and citing it shows you know the simplification.
- The French or Arabic search before claiming novelty is a good idea. Phrase the claim carefully anyway: "an application of standard methods to women producers in rural Tunisia", not "a new method".
- **Framing:** this module is operations research, not machine learning. That is a strength (explainable, no data needed), but if the pitch calls it "AI", be ready to explain why. "Optimisation that a dispatcher validates" is an accurate description.

---

## 11. Smaller points

- **Toy instance:** 10 producers and 3 sites is right. Write the expected answer down **before** running the code, and turn it into a unit test.
- **Link to the platform:** say where declarations come from (USSD/SMS or the community agent) and what the producer receives ("Your point: X, Tuesday 8:00–9:30"). One sentence is enough, and it ties the module to the rest of RuralDirect.
- **Anonymity:** the GitHub repository must not show team names, member names or a personal account. Check the commit author and the account before making it public.

---

## 12. Priority list

| Priority | Action |
|---|---|
| 1 | Fix the contradictions in §2, especially fixed days vs dispatch rule and the school rule |
| 2 | Add B2 (intermediary) and B3 (shared transport) baselines, and include walking and waiting time on the optimised side |
| 3 | Weight the p-median by producers, set point capacity from the site, add a set-cover pre-check |
| 4 | Define the KPIs and the stage interfaces (file formats) before splitting the work |
| 5 | Add shrinkage, a planning percentile and the fairness rule to the reliability factor |
| 6 | Replace the second routing solver with a brute-force check, and add a larger or mixed instance |
| 7 | Add seasons, heat limit and product profiles (including artisanal) to the config |
| 8 | Run multiple seeds and participation rates |
