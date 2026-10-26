# AOTN Phase 2.1 Solution Blueprint: Draft Review
**Draft reviewed:** `Copie de AOTN Phase 2.1 - Solution Blueprint (Template).pdf` (10 pages)
**Deadline:** 20 October 2026, 11:59pm (link submitted through the Phase 2.1 form)
**Solution:** Nadhir, a non-intrusive camera and microphone monitoring and alerting system for MT/BT substations

---

## Verdict
The content is strong and covers every section of the template. The solution follows directly from the Phase 1 finding that detection already exists and the missing piece is getting the alert to a person. The "touch nothing, re-certify nothing" angle is a real differentiator.

The draft is **not submittable yet**:
- It is **10 pages against a 6-page maximum**.
- It still contains internal notes, undecided choices, and grey guiding questions.

Most of the work left is cutting. The content itself needs only a few fixes.

---

## 1. Blocking issues (fix before submitting)

| # | Issue | Fix |
|---|---|---|
| 1 | **10 pages, max is 6** | Keep **one** diagram, as the template says. Delete the other two diagrams. Keep **either** the explanation paragraph **or** the 9-step table, not both. Delete the grey questions. Together this should fit in 6 pages. |
| 2 | **Three diagrams** (simple architecture, swimlane flow, detailed architecture with watchdog) | Keep the **detailed architecture with the cloud watchdog** (page 4). It is the only one that shows the heartbeat, which Risk 3 and the Phase 1 table both rely on. |
| 3 | **Solution name: "?????"** | Write **Nadhir**. It is already used throughout the document. |
| 4 | **Two one-sentence answers** ("choose one") | Use the **second, short one**. The first is 60+ words and does not read as one sentence. If needed, add "and predicts abnormal trends" to the short one. |
| 5 | **Internal notes left in:** "(fema alarm lamps?)", "(choose one diagram)", "(choose explanation or step by step)", the French watchdog paragraph, "nzidouh ou pas ?" | Delete all of them. The document must be entirely in English. |
| 6 | Grey guiding questions still present | The template says to delete them. |

### Decisions on the open questions in the draft
- **Watchdog: yes, keep it.** Describe it in one line inside the explanation: *"A cloud watchdog raises a SYSTEM OFFLINE alert if the box stops sending its heartbeat; the Raspberry Pi's built-in hardware watchdog restarts the box if its software freezes."* The French paragraph argues this point well; it just doesn't belong in the submission.
- **Alarm lamps:** keep them, but write "alarm lamps **where present**". Not every panel has them, and the siren and dials cover the case where they don't.

---

## 2. Content improvements (in priority order)

### 2.1 Link to Phase 1: the main validated insight is missing
The table maps 4 needs, but **none of them cites an interview**. It also leaves out the expert interview's key finding: **the existing ERP/CMMS maintenance module is too hard for floor and night staff to use, so it isn't used.** This finding answers a question reviewers will ask: *"why not just use the factory's CMMS?"*

Add a row:

| Validated need | Part of the solution |
|---|---|
| Existing ERP/CMMS maintenance tools are too complex for floor and night staff, so they go unused (industrial-organization expert interview) | Zero-app alerting for the guard: a plain SMS or voice call, acknowledged with a one-digit reply. The dashboard is only for the electrician and the manager. |

Also:
- **Name the source on each row**, e.g. "(technician interview)" or "(technical-director interviews)". Phase 2 is graded on building from *validated* needs, and the table currently reads like assertions.
- The **Decision Log** feature is not mapped to any need. Map it to the CMMS row, or to "ongoing risk monitoring with traceability (ISO 45001, Phase 1 §5)".

### 2.2 Feasibility: the budget has no numbers
"Budget: prototype components…" is a list, not a budget. Add a **rough cost table in TND** for one prototype box (Raspberry Pi, IR camera, USB mic, 4G modem, 2G module, UPS/battery, SIMs + SMS credit) and a total. Approximate prices from a local supplier are enough. A low unit cost is the core of the "affordable retrofit" claim, so put a number on it.

### 2.3 Feasibility: missing skills have no plan
The draft lists missing skills (MT/BT, embedded/IoT, CV dial reading, audio, cybersecurity) but not **how the team will get them**. Add one line per skill, for example:
- MT/BT and safe camera placement → the technical directors already interviewed act as advisors
- CV dial reading → OpenCV gauge-reading tutorials plus a test bench of printed dials before any site visit

### 2.4 Risks: the most likely project-stopper is missing
The likeliest thing to stop the project is **not getting access to a real substation** for photos, siren recordings, and a pilot. Risk 1's mitigation ("train on photos from varied conditions") depends on this data. Suggested set:
1. Gauge reading errors (High), as written
2. **No access to a real substation / data (Medium)** → ask the ICAR contacts for a pilot site; build a bench of printed dials and a recorded siren as the fallback
3. Device failure / offline (Medium), as written, plus a note to use **two different operators** for the 4G and 2G SIMs so one cell outage doesn't take out both channels

Fold the siren-misdetection risk into Risk 1 as "reading or detection errors". It shares the same mitigation (two signals must agree).

### 2.5 Don't overclaim "predictive maintenance"
Dials read every few seconds with no history don't support ML prediction at launch. Section 3 is already honest about this ("limits and trend first; ML after history is collected"). Make feature 2 match:
**"Trend detection: flags abnormal drifts and estimates time left before a limit is reached; anomaly detection is added once enough history exists."**

### 2.6 Main user: pick one
The template asks for *the* main user. Say: **Main user: the on-call qualified electrician (habilité).** **Secondary users:** the night/weekend guard (receives alerts, cannot enter the room) and the plant manager (dashboard).

### 2.7 Worth adding in one line each, if space allows
- **Privacy/security:** only extracted readings and alerts leave the site, never the video stream. This matters to factory owners and fits the AOTN ethics theme.
- **Escalation chain:** the example already shows "no reply in 5 min → voice call". State this rule in the Smart Alerting feature. It shows humans stay in the loop, which is the core of the AOTN "collective decision-making under pressure" theme.

---

## 3. What is already good (keep)
- Strong problem-to-solution continuity: "escalation is missing, not detection" carries straight over from Phase 1.
- Touch-nothing design: no wiring, so no re-certification. This is easy for a factory to say yes to.
- Two-signal confirmation (dial + lamp/siren) before an INTERVENE NOW alert.
- WATCH / INTERVENE NOW levels, with an illustrative message example.
- 4G primary + 2G SMS/voice fallback + heartbeat.
- Decision log (who, when acknowledged, decision, outcome).
- An honest skills-gap table.

---

## 4. Checklist before submitting
- [ ] Solution name = Nadhir
- [ ] One sentence, one main user, 3–5 features (consider merging Backup Communication into Smart Alerting to stay at 4)
- [ ] One diagram (the watchdog architecture) + either the explanation or the step table
- [ ] All French notes, "(choose…)" markers and grey questions deleted
- [ ] Budget table with numbers in TND
- [ ] Plan for each missing skill
- [ ] Risks: add data/site access; mention two operators for the two SIMs
- [ ] Phase 1 table: add the CMMS row, cite the interview source on each row, map the Decision Log
- [ ] Export check: **≤ 6 pages**
- [ ] Google Doc sharing set to "Anyone with the link can view", link tested in an incognito window
- [ ] Link submitted in the Phase 2.1 form before 20 Oct, 11:59pm
