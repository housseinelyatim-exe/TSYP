# Final check: `report-12.pdf` (29 pages), 12 Oct 2026

**Verdict: ready to submit after one fix (citations in Chapter 1, ~10 min).** Everything else below is optional.

## Fixed since report-9 ✅
- Chapter 1 now opens with real numbers and the "warning existed the day before" argument.
- The broken "TunisiaHydromet" citation is gone.
- Mission, Vision and Values have been added (§4.1).
- "Woman in Engineering" and "YP" are gone from the team table.
- New conclusion with requirement traceability (Table 5.1), honest limitations and an outlook. This is good work.
- 29 pages, within the 30 limit. The PDF author field is empty, and there are no names or school.

## 🔴 Must fix: Chapter 1 has **zero citations**
Every new fact (70%/60%, US$40M, 200/225 mm, 6 deaths, US$100M, January 2026, 13th of 19, US$24M, the pilot regions, "half of US deaths are vehicle-related", "SMS delayed by hours") is printed without a source. Several aren't even in the bibliography. A judge will read these as unsupported claims, and they're the most important facts in the report.

**Steps:**
1. Append `SIGHT/chapter1-missing-bib-entries.bib` to your Overleaf `.bib` file. Skip any key that's already there (S01, S02 and S35 probably are).
2. Add `~\cite{…}` at these places:

| Sentence in §1.1 | Add |
|---|---|
| "…70% of disaster casualties and 60% of economic losses" | `~\cite{S02}` |
| "…estimated US$40 million per year" | `~\cite{S10}` |
| "…six lives, affected more than 6,000 families" | `~\cite{S01}` |
| "…recovery needs exceeding US$100 million" | `~\cite{S02}` |
| "…five deaths and 350 emergency rescues… hardest-hit governorates" | `~\cite{S12}` |
| "…rise dangerously in less than an hour" | `~\cite{S36}` |
| "…nearly half of flash-flood fatalities are vehicle-related" | `~\cite{S32}` |
| "…delayed by hours… no acknowledgement back-channel" | `~\cite{S35}` |
| "…issued the day before… stranded on rooftops" | `~\cite{S01}` |
| "…13th of 19 MENA countries… alert dissemination" | `~\cite{S02}` |
| "…Action 8a, Priority 1" | `~\cite{S08}` |
| "…US$24 million to INM" | `~\cite{S09}` |
| "…Greater Tunis, Ghardimaou, and Kebili" | `~\cite{S05}` |
| §1.2 GSMA / LoRaWAN / Hydromet / Flood Hub | `~\cite{S06}`, `~\cite{S17}`, `~\cite{S09}`, `~\cite{S24}` |

Recompile **twice** (LaTeX, then BibTeX, then LaTeX twice), then check that no "[?]" appears.

## 🟠 Still open from the earlier review (optional, in order of value)
1. **Danger rule contradiction** (§2.3 "accepted even if both continuous sensors fail" vs §2.5 "two of the three methods"). This is a one-sentence fix; the text is in `report-9-final-review.md` item 4.
2. **Orphaned heading:** "4.6 System risk register" is again alone at the bottom of page 20 (printed page number). Add `\clearpage` before it.
3. **Uncited figures in Chapter 4:** "March 2026 World Bank release… US$125 million" (cite it or cut it) and "CHF 294,452" (add `\cite{S01}`).
4. **ROI and revenue are still not there.** §4.5.3 still says "we make no estimate" and "different currencies", and the canvas wasn't added. The text is in `report-9-final-review.md` (add-on section) and `business-model-canvas.tex`. With 29 pages you only have room for **one**: use the ROI and revenue paragraph (no table), not the canvas.
5. **N3 samples every 10 min in Normal mode** (§2.3 Firmware). Add one sentence: "N3 samples every minute in all states, and a closing float wakes any node at once."
6. **Cover subtitle** is still the challenge's name ("Next-Generation Emergency eXchange for Universal Sustainability").
7. **"Methodological note:"** in §1.1.4. Just delete the label; the sentence underneath is fine.
8. **Tone of Mission/Values:** "usurping the sovereign mandate", "We reject… black-box systems" is overwritten. Optional to soften.

## Submit order
Citations in Chapter 1 → recompile → check for "[?]" and page count ≤ 30 → **submit**. Do items 1–3 only if time is comfortably left.
