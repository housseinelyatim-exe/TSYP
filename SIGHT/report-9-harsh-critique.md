# Harsh critique: `report-9.pdf` (NEREUS), read as a tough judge

**Short version:** a strong engineering chapter inside a weak proposal. Chapter 2 is better than most student reports. Everything around it reads as written last, by different people, in a hurry. The rubric gives **35 of the 55 report points to things other than engineering**, and that's exactly where this report is thin.

## Estimated score (my judgement against the rubric, not an official score)

| Block | Max | Estimate | Why |
|---|---|---|---|
| Report quality | 5 | **2.5** | No executive summary, no conclusion; three different writing voices; heading left alone at a page break |
| Managerial | 10 | **4–5** | No Mission/Vision/Values, no market analysis, ROI explicitly refused, timeline ends on 10 Dec |
| Technical soundness | 15 | **11–12** | Strong, but contradicts itself on the core Danger rule and over-claims work that isn't done |
| Humanitarian impact | 10 | **5–6** | No contact with the community at all; SDG padding; vague Chapter 1 |
| Ethics & values | 10 | **6–7** | Mostly a copy of §2.10; wellbeing and ownership are thin |
| **Total** | **50** | **≈ 29–33** | Most of the lost points are in writing, not engineering |

---

## 1. The project name copies the challenge's name
The cover says **"NEREUS: Next-Generation Emergency eXchange for Universal Sustainability"**. That subtitle is **the challenge's own title (NEXUS)**, letter for letter. The letters of the expansion don't even spell NEREUS. A judge who wrote the brief will notice in the first second. It looks like the team didn't come up with a name. **Fix:** keep NEREUS (Nereus was the Greek god of the sea, so the name works) and write your own subtitle, for example *"NEREUS: a last-kilometre flash-flood warning chain"*.

## 2. Chapter 1 is the weakest chapter, and it's the first one judges read
- **No numbers.** "Flooding is a recurring hazard in Tunisia, affecting several regions…" could describe any country. The 2018 flood appears without its death toll, rainfall or date. The best fact in the project (**the warning was issued the day before and people still died**) is hidden in Chapter 2. It should be the first paragraph of the report.
- **Broken citation printed as text:** "Tunisia**TunisiaHydromet**". It's on page 1. It looks careless.
- **"Methodological note: Oued Souhil is a preliminary candidate site… subject to field assessment."** This tells the judge you haven't looked. Together with "illustrative", "proposed" and "described setting", the case study comes across as not believed in by its own authors.
- **The "Principle" for GSMA reads like a press release** ("helping them react quickly and stay safe. It also supports the UN SDGs"). It's fluff in a section that should be analysis.
- **The disclaimer** "gaps are stated relative to what each source describes publicly" is defensive. Saying it once in §2.2 is enough.
- **The impact table contradicts the design.** §1.5.1 says the system "cannot reach every resident directly" (SMS goes to a small registered group). Yet the impact target is **"Households covered: 90 of 100"**. Which 100? "False alarms below 5%" has no denominator. "Alert delivery ≥ 90%" conflicts with V2 "≥ 99%".
- **SDG padding.** Five SDGs: 3.d is about national capacity for early warning of *health* risks; 9.1 and 17.17 are stretches. A judge counts the weakest one, not the strongest. Two or three that fit well (11.5, 13.1, 1.5) score better than five that need explaining.

## 3. No evidence that any real person was involved, which hurts "real community needs" and "empowers local actors"
§1.5.2 says it plainly: *"Engagement with local actors is planned for Phase 2 rather than already completed."* There's no survey, no interview, no letter, and no conversation with a technician, a volunteer or Civil Protection. Every humanitarian claim is desk research. "Addresses real community needs" is scored on evidence that the need is real **here**, and this report has none. The video script mentions an interview with a researcher, but the report doesn't. If that interview happened, **put one sentence about it in Chapter 1**. Even one quoted conversation is worth more than five SDGs.

## 4. Chapter 2: strong, but the main logic is inconsistent and some claims go too far
- **The Danger rule contradicts itself.** Page 7 says "a closed Danger float is accepted even if both continuous sensors fail"; page 9 says "Danger needs two of the three methods". This is the decision that switches on a siren, and the report gives two answers. A judge with a technical background will stop trusting the rest.
- **"Median of the continuous readings"** is the median of two numbers, which is just their average. It's a small error, but it shows the text wasn't checked carefully.
- **N3 samples every 10 minutes in Normal mode.** If a storm hits only near the bridge, the "local first" beacon can fire 10 minutes after the water reaches the road. That breaks the report's main promise, and nothing in the report addresses it.
- **It describes work that doesn't exist yet as if it does:**
  - "Everything is open source and **published on GitHub** with continuous integration." Is it published? If not, say "will be".
  - "A **failure-modes analysis of every component** fed the risk register." It isn't in the report. Show it or drop the claim.
  - "Encrypted gateway storage, **signed firmware**" are presented as facts, but they're plans.

  A judge who catches one over-claim discounts every other claim.
- **Weak sources for technical claims:**
  - Wikipedia for the radio regulations [14]
  - a vendor blog for sensor weaknesses [8]
  - a Zenodo record with no authors [3]
  - a book chapter about **Morocco** for flood lead times [23]
  - a "smart campus" arXiv paper as range evidence [18]

  In the chapter judged on "use of right methodologies", this matters.
- **The CAP "institution bridge" has no one on the receiving end.** Nothing shows the regional committee can, or wants to, receive a signed CAP XML file. Without that, the institutional part is a hypothesis, and it should be labelled as one.
- **Pressure sensor:** there's no vented cable or barometric correction. Weather pressure changes during a storm put several centimetres of error into the level reading. Anyone who has used one of these sensors will ask about it.
- **The "innovation" table only beats research papers on features the papers didn't try to have,** judged on "the parts we read". The honest claim, "the combination is new", is fine. But the table sets up easy opponents.

## 5. Chapter 3 is mostly a copy of Chapter 2
- Privacy is described **three times** (§2.6, §2.10, §3.2), the tamper-evident log **three times**, and the reasons for using rules instead of AI **twice**. A judge reading in order sees the same paragraphs again and concludes the chapter was padded.
- **"This chapter articulates how… Rather than treating ethics as an abstract layer…"** sounds generated. Judges in 2026 recognise this style and mark it down for "concise language".
- **Wellbeing** gets one paragraph, about alert fatigue, folded into Equity. There's nothing on calm, specific messages, volunteer stress or surveillance. It's worth 2 points, so give it its own heading.
- **"Community ownership"** is about repairable hardware and volunteer safety. Ownership means **who owns the system and the data, and who decides**. That isn't stated anywhere.
- **Sustainability** covers only the environment, and spends lines on battery cycles and ASA vs PETG brackets. It says nothing about **economic or institutional sustainability**: who pays in year 3, and who maintains it once the student team leaves. That's the real question.
- **Equity** never says how sites are chosen. If the answer is "wherever the municipality says", the poorest areas may never get one.

## 6. Chapter 4 is a cost estimate, not a business case
The brief says: *"The project should present a business-oriented idea supported by financial and market analysis."* This chapter refuses to do either.
- **No Mission, Vision or Values.** The rubric names them, and the video requires them. Leaving them out is the easiest lost points in the report.
- **No real market analysis.** It's one paragraph, and it says *"We make no market-size estimate."* There are no customer segments, no competitors, no pricing and no willingness to pay. Honest is better than invented, but "we don't know" scores 0 of 2. A **SWOT**, a **segments table** and a **positioning table** would cost 1 page and need no invented numbers.
- **ROI is refused:** "we make no estimate", "we do not monetise the main benefit". Then it compares TND with CHF and says the comparison is in "different currencies". Just convert them. A break-even argument ("the 5-year cost equals X; one avoided vehicle loss or rescue covers it") is honest *and* scores.
- **No revenue model.** Who pays whom, for what, and how much? Is it a product, a service, or open hardware with paid installation? It isn't stated.
- **The OPEX is unrealistically low.** 760 TND/year with **no labour**, 200 TND for scheduled inspections plus post-event checks on 4 sites, and 150 TND/year to replace batteries worth about 2,000 TND. A municipal finance officer would not believe it. Either cost the technician's time or say it's provided free by the municipality.
- **"Can procure within existing local resilience budgets"** has no evidence behind it, and Tunisian municipal budgets are famously tight.
- **The timeline ends on 10 December.** Nothing covers the real deployment: permits, funding, installation, first flood season. Within Phase 2, field-testing at Oued Souhil in **week 7**, with permissions requested in **week 1** from Tunisian authorities, is optimistic. The fallback is there, which is good.
- **The team table:**
  - It's full of buzzwords ("multidisciplinary governance", "warning syntax validation", "municipal procurement roadmapping").
  - It puts **"Woman in Engineering"** and **"Young Professional (age < 35)"** in the *IEEE Affiliation* column. These are clearly for bonus points, and it reads as tokenism. Put that information in the submission form, not in a column about roles.
  - It doesn't say who backs up whom.
- **The risk register is good but mixes two scales:** Critical/Major/Moderate for severity, High/Medium/Low for likelihood. It has no owners and no ordering. It's 16 rows when ~10 well-ranked ones would be stronger.
- **No partners section.** INM, ONPC, the experimental station and the Ministry of Equipment are scattered across chapters but never brought together.

## 7. Structure and writing
- **No executive summary.** A judge reading 26 pages needs the whole story on page 1.
- **No conclusion.** The report stops at a table and goes straight to the bibliography.
- **Three voices:**
  - Chapter 1: vague, hedged, academic ("These events highlight the importance of…").
  - Chapter 2: precise and dense.
  - Chapters 3–4: corporate filler ("structured", "articulates", "landscape").

  One editor needs to read it straight through.
- **Heading numbering is uneven:** Chapter 1 goes to 1.1.1–1.1.5; the other chapters stay flat.
- **"4.5 Risk register" is left alone at the bottom of page 20.**
- **The bibliography** has entries with no author, no year, or only "In Springer".

---

## What moves the most points tonight (in order)
1. **Mission/Vision/Values plus a business model paragraph plus SWOT/segments** in Chapter 4: about **+2–3**.
2. **Chapter 1 opening with real numbers and the "warning existed" argument; delete the Methodological note; fix the broken citation:** about **+1–2**.
3. **Fix the Danger-rule contradiction and the 10-min N3 issue:** protects the technical score.
4. **Executive summary and conclusion (half a page each):** about **+1**.
5. **Change "is published" / "was analysed" to "will be"** where the work isn't done: protects credibility.
6. **Replace the cover subtitle.**

The ready-to-paste text for 1–3 is in `report-9-final-review.md`. **Submit before the deadline even if only items 1–3 are done.**
