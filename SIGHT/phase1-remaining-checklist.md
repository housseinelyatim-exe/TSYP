# Phase 1: what's left (checked 12 Oct 2026, the deadline day)

**Required:** one report PDF (30 pages max), anonymous. A video of 2 minutes or less is optional (5 points, plus up to 3 bonus points).
**Submit early today. Missing the deadline means elimination.**

## Where things stand

| Rubric block | Points | Status in `~/Desktop/report/report/` |
|---|---|---|
| Technical Soundness | 15 | ✅ Chapter 2 (8 p), revised |
| Humanitarian Impact (needs, impact, inclusion, SDGs, local actors) | 10 | ✅ Mostly covered in Chapter 1 (§1.4–1.7) |
| Ethics & Values (equity, transparency, sustainability, wellbeing, ownership) | 10 | ⚠️ Only "Ethics in the technology" (§2.x). **There is no section that goes through the five values one by one** |
| **Managerial Aspects** (timeline, risks, team roles, market, financial) | 10 | ❌ **Not written.** No Mission/Vision/Values, roles, Gantt, risk register, market, budget or ROI |
| Report Quality (structure, flow) | 5 | ⚠️ No title page, executive summary, table of contents or conclusion |
| Video | 5 (+3) | ⚠️ Script revised (`video-script-review.md`), not recorded |

The two chapters together come to 15 pages, so about 15 pages are left for everything below.

> If teammates wrote the managerial or ethics parts somewhere else (for example a Google Doc), those parts only need converting into LaTeX. Check this first.

## Must do (the report isn't complete without these)

1. **Choose the project name** and set `\projname` once in `main-ch1-2.tex`, line 39. "[Project Name]" currently appears in Chapters 1 and 2 and in `TECHNICAL-SPEC.md`. (The earlier blueprint used "SAYL".)
2. ✅ **DRAFTED → `chapter4.tex` (6 p).** **Chapter 4: Managerial aspects (~6–7 pages, 10 points).** The raw material is in `flashflood-iot-solution.md` §8.
   - Mission / Vision / Values. The video also needs these.
   - Team roles (3–5 roles, **with no names**; you can say which role holds the SIGHT, Systems Council or CEDA membership)
   - Timeline: a Gantt chart from Oct 2026 → Phase 2 on 10 Dec 2026 → a 2027 pilot
   - Risk register: technical, institutional and financial risks, each with a mitigation (the table in §8.6 is a start)
   - Market analysis: customers (municipalities, ONPC, industrial zones, insurers), size, competitors (reuse the Chapter 1 §1.3 table)
   - Budget: BOM for N1, N2, N3 and the gateway in TND; pilot cost; yearly operating cost
   - Financial analysis / ROI: cost against avoided losses (World Bank: about US$40M a year; Nabeul 2018 recovery US$100M), plus the business model
   - Potential partners: Nabeul municipality, ONPC, INM, the experimental station
3. ✅ **DRAFTED → `chapter3.tex` (3 p).** **Ethics & Values section (~2 pages, 10 points).** Give equity, transparency, sustainability, wellbeing and community ownership one paragraph each, using the rubric's exact words as headings. Source: blueprint §10 plus what Chapter 2 already says.
4. **Front and back matter:** title page (anonymous, with no school or SB), a one-page executive summary, a table of contents, and a short conclusion.
5. **Anonymity check:** search the final PDF for names, the school, the student branch and author metadata (`pdfinfo` → Author). Remove any `\author{}` or hyperref author fields.
6. **Final build:** `main-ch1-4.tex` now includes all four chapters (24 pages with the bibliography; PDF: `chapters-1-4-new.pdf`). Compile, confirm the PDF is **30 pages or fewer**, check that no references show "??", and check the figures.

## Should do if there's time

- **Chapter 2 items still open** (from `changes-chapters-1-2.md`), about one sentence each:
  - Pressure sensor: vented cable, or barometer compensation
  - Meshtastic moved off 869.525 MHz, with a private PSK
  - "Reply 1" ambiguity when two alerts are open
  - Anchor the log hash outside the gateway
- Replace the Wikipedia and vendor-blog citations ([14], [8]) with ERC/REC 70-03 or datasheets.
- **Video:** fill in **[Name]/[field]** for the researcher, or cut that part (and name nobody, for anonymity). Add the project name, Mission, Vision and Values, which are required in the video. Record a voice-over over the map and visuals, with no faces and no school. Keep it under 2:00.

## Bonus points worth claiming now

- Municipality or association letter of interest (+3), if one exists. Put it in an appendix.
- Training-session screenshots (+1 each, up to 5), a woman on the team (+1), a Young Professional on the team (+1). These go in the submission form.
- Multi-SDG (+2): already covered (11.5, 13.1, 1.5).

## Suggested order for today

1. Name → 2. Chapter 3 (managerial) → 3. Ethics section → 4. Executive summary, title page, TOC, conclusion → 5. Compile, check pages and anonymity → **6. Submit** → 7. Video if time allows (it's optional, so don't let it hold up the report).
