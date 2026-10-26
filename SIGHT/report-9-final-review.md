# Final check: `report-9.pdf` (NEREUS, 26 pages), 12 Oct 2026

**Verdict:** You can submit it. It's within the 30-page limit, anonymous (no names or school; the PDF author field is empty), and all four rubric blocks have a chapter. Chapters 2–4 are solid, and the CAPEX/OPEX numbers add up.

There are **6 quick fixes worth making before you submit** (about 30–45 min in Overleaf). The rest is optional.

> Note: this PDF uses the **old Chapter 1** and an **older Chapter 2**. The rewritten versions (`~/Desktop/report/report/chapter1.tex`, `chapter2.tex`) are not in it. Swapping them in tonight is risky: section numbers, R1–R6 wording and cross-references differ. The quick fixes below patch the worst gaps instead.

---

## Must fix (each costs points or looks unfinished)

### 1. Mission / Vision / Values are missing (Managerial block + video)
The rubric lists them explicitly, and the video must state them. Paste this at the start of Chapter 4:

```latex
\section{Mission, vision and values}
\textbf{Mission.} Close the last kilometre of flash-flood warning in Tunisia: make sure that people at a wadi crossing are warned in time to act, that a responsible person confirms every alert, and that nobody's silence is ever taken as safety.

\textbf{Vision.} By 2030, no one in Tunisia dies at a wadi crossing for lack of a warning that could have reached them.

\textbf{Values.} \emph{Silence is never safe}: a missing reading or an unanswered alert is a problem, never good news. \emph{Humans decide}: the system recommends; the authorities decide on public alerts. \emph{Open and repairable}: open designs, common parts and a manual, so that local technicians keep it running. \emph{Everyone is warned}: light, sound, SMS, voice and volunteers, with no smartphone needed. \emph{Honest numbers}: false alarms and failures are published as openly as successes.
```

### 2. Broken citation in §1.1.1 (page 1)
The text reads "…hydromet roadmap for Tunisia**TunisiaHydromet**." The citation key is printed as text. Use `\cite{TunisiaHydromet}` (check the key exists in the .bib file), or delete the word.

### 3. Chapter 1 has almost no facts or citations, and still has the "Methodological note"
A judge reads Chapter 1 first. Replace the first paragraph of §1.1.1 with the version below (the keys match `refs.bib`: S01 = IFRC DREF, S02 = World Bank PID, S10 = World Bank 2022; check they're in your .bib):

```latex
Floods are Tunisia's deadliest natural hazard: they caused about 70\% of disaster casualties and 60\% of economic losses between 1957 and 2018~\cite{S02}, and cost the country about US\$40 million a year~\cite{S10}. On 22 September 2018 about 200\,mm of rain fell on Nabeul in one day; six people died and more than 6{,}000 families were affected~\cite{S01}. A warning had been issued the day before~\cite{S01}: the weak link was not the forecast but the last mile, getting a clear instruction to the right people and making sure someone acted on it.
```
Also **delete the "Methodological note" sentence** in §1.1.3, or reword it: "Exact node positions will be confirmed by a field survey in Phase 2."

### 4. Danger rule contradicts itself (Chapter 2, pages 7 and 9)
- §2.3 Fusion: "A closed Danger float is accepted **even if both continuous sensors fail**."
- §2.5: "Danger needs **two of the three methods** at N3."

Replace the Fusion sentence with:
```latex
Danger needs two of the three \emph{working} methods. If the other two are flagged degraded, a closed Danger float triggers Danger on its own (when in doubt, alarm); if the float is closed but both working sensors clearly read low, the node reports Warning with a float fault, so a float jammed by debris cannot alarm the town. The ultrasonic value is the median of five echoes.
```

### 5. N3 can react up to 10 min late (Chapter 2, Firmware, page 8)
"Every 10 minutes in Normal" also applies to N3, and the local beacon is the report's main promise. Add one sentence after "(initial values).":
```latex
N3 samples every minute in all states, and a closing float switch wakes any node at once through an interrupt, so the beacon never waits for the next scheduled sample.
```

### 6. Two figures in Chapter 4 have no source
- §4.3: "a **March 2026 World Bank release** describes as a **US\$125 million** programme". Add the citation, or cut it to "…Program (P173568)~\cite{S02}".
- §4.4.3: "**CHF 294,452**" IFRC allocation. Add `~\cite{S01}` (the IFRC DREF report, [24] in your bibliography).

---

## Should fix (cheap points)

7. **No business model or revenue: the financial analysis is costs only.** The brief asks for "a business-oriented idea… ROI/profit". Add a short paragraph at the end of §4.4.3:
   ```latex
   \textbf{Business model.} Alerts are always free for the people protected. Institutions pay: a turnkey deployment sold to a municipality or road authority at cost plus a margin (about 12{,}500\,TND per crossing), and an optional yearly service contract (software updates, second-line repair, SMS credits, season report, yearly drill). Because the design is open source, the municipality can end the contract and maintain the system itself. Employers near a wadi can sponsor a crossing that the municipality then owns. First deployments are funded by disaster-risk programmes~\cite{S02}; the season report then gives a municipality the evidence to put the running cost in its own budget.
   ```
8. **The timeline stops on 10 Dec.** "Realistic implementation timeline" covers deployment too. Add one line to §4.2: *"After the competition: permits and funding (Jan–Apr 2027), field units built (Apr–Jun), installation in the dry season (Jul–Aug), a full drill with Civil Protection (Sep), and the first live flood season (Sep 2027–Jan 2028), followed by a public season report."*
9. **No executive summary or conclusion** (Report Quality: structure and flow). You have about 4 pages of room. Half a page each is enough: problem → what NEREUS does → key numbers (3 nodes, ~10,500 TND, ~760 TND/yr, 5-s local beacon, 3-min escalation) → impact.
10. **Orphaned heading:** "4.5 System risk register" sits alone at the bottom of page 20, and its table is on page 21. Put `\clearpage` before `\section{System risk register…}`.
11. **Table 1.1 vs Table 2.6:** alert delivery target "≥ 90%" vs V2 "≥ 99%". Pick one, or label 90% as "end-to-end to a person" and 99% as "radio".
12. **Partners are only mentioned in passing.** One line listing them (Nabeul municipality, ONPC, regional committee, INM, the Oued Souhil experimental station, Ministry of Equipment, ANF, INPDP) helps the market-analysis points.

## Fine as is
- Anonymity: no names or school. Table 4.1's "Woman in Engineering" and "YP (age < 35)" describe roles, not identities, so they're OK. Make sure the same facts are in the bonus form.
- CAPEX 7,280 → 10,500 TND and OPEX 690 → 760 TND are arithmetically correct, and the 5-year figure of 14,300 TND is correct.
- The risk register (16 risks with severity, likelihood and mitigation) is strong.
- Chapter 3 covers all five rubric values (equity, wellbeing, transparency, sustainability, ownership).
- The link-budget distances table (Table 2.4) fixes the old "1.6 km only" problem.

## Order if short on time
1 → 2 → 4 → 6 → 3 → 5 → 10 → submit. Then 7–9 if there's time before the deadline. **Don't miss the deadline for polish.**

---

## Add-on: return on investment and revenue model (paste at the end of §4.4.3)

The figures use the report's own costs: 10,500 TND to build and 760 TND/yr to run. Exchange rate used: 1 CHF ≈ 3.6 TND (check today's rate). The car value and all prices and volumes are assumptions, and the text labels them as such.

```latex
\textbf{Return on investment for the buyer.} We do not try to predict how many lives one crossing will save. Instead we compute the avoided loss at which the system breaks even. Over five years a site costs about 14{,}300\,TND, so
\[
\mathrm{ROI}_{5\,\mathrm{yr}} = \frac{\text{avoided losses} - 14{,}300}{14{,}300},
\]
which is positive as soon as avoided losses exceed 14{,}300\,TND, or about 2{,}900\,TND a year. For scale: the IFRC relief allocation for the 2018 Nabeul flood alone, CHF~294{,}452 (about 1.06~million~TND)~\cite{S01}, is 74 times the five-year cost of a site. One family car kept out of the water (about 40{,}000\,TND, our assumption) would return the five-year cost 2.8 times (ROI $\approx$ 180\%). Rescue operations and injuries avoided add to this, and lives saved are not counted at all.

\textbf{Revenue model.} Alerts are always free for the people protected. Institutions pay: (1)~a \emph{turnkey deployment} per crossing, sold to the municipality or road authority at 13{,}500\,TND (cost 10{,}500\,TND), including installation, training and a first drill; (2)~an optional yearly \emph{service contract} of 1{,}800\,TND (cost about 1{,}200\,TND: the 760\,TND of Table~4.4 plus our support time), covering software updates, second-line repair, SMS credits, the season report and a yearly drill. Because the design is open source, the municipality can end the contract and run the system itself. Employers near a wadi can sponsor a crossing that the municipality then owns. The first sites are funded by disaster-risk programmes~\cite{S02}.

\begin{table}[htbp]
\centering\small
\caption{Three-year plan, in TND (planning assumptions, not forecasts).}
\begin{tabular}{@{}lrrr@{}}
\toprule
 & 2027 & 2028 & 2029 \\
\midrule
New sites (sites under service contract) & 1 pilot (0) & 3 (1) & 6 (4) \\
Revenue: grant, deployments, service & 10\,500 & 42\,300 & 88\,200 \\
Costs: deployments, service, fixed & 14\,700 & 40\,700 & 81\,800 \\
\textbf{Net result} & $-$4\,200 & 1\,600 & 6\,400 \\
Cumulative & $-$4\,200 & $-$2\,600 & \textbf{3\,800} \\
\bottomrule
\end{tabular}
\end{table}
The plan breaks even in 2029 with ten sites. The 2027 shortfall is the pilot's first year of operation and support, covered by prizes, university support or a sponsor. If only half the planned sites are sold, break-even moves to 2030.
```

Breakdown behind the table:
- **2027:** grant 10,500. Costs: pilot 10,500 + one year of service 1,200 + fixed 3,000 = 14,700.
- **2028:** revenue 3 × 13,500 + 1 × 1,800 = 42,300. Costs: 3 × 10,500 + 1 × 1,200 + fixed 8,000 = 40,700.
- **2029:** revenue 6 × 13,500 + 4 × 1,800 = 88,200. Costs: 6 × 10,500 + 4 × 1,200 + fixed 14,000 = 81,800.

Also **delete** these sentences from §4.4.3: "the figures are in different currencies", "we make no estimate of how many losses a warning at one crossing would avert", and "We do not monetise the main benefit…". The new paragraph replaces them.

---

## Add-on: conclusion with limitations (paste as an unnumbered chapter before the bibliography)

```latex
\chapter*{Conclusion}
\addcontentsline{toc}{chapter}{Conclusion}

In Nabeul in 2018 the warning existed and people still died. NEREUS addresses that last kilometre. Three solar stations watch the wadi, and a beacon and siren warn the crossing with no network. Two independent signals must agree before people are alarmed. Every alert must be confirmed by a person and escalates to the municipality and Civil Protection when nobody answers. The regional committee receives signed evidence and keeps the decision. The design is built from off-the-shelf parts and open-source software, costs about 10{,}500\,TND per crossing and 760\,TND a year to run, and can be repaired by municipal technicians.

\textbf{Limitations.} We state what this report does not yet show, and how Phase~2 and the pilot will address each point.
\begin{itemize}
\item \emph{No field data yet.} Thresholds, hold times and power figures are initial design values. They will be replaced by bench measurements (tests V1--V9) and, in the pilot, by recorded events.
\item \emph{Site not surveyed.} Oued Souhil was chosen from maps and published sources. Node heights, radio paths and the gateway site will be fixed by a field survey and walk tests.
\item \emph{No partner agreement yet.} Message wording, escalation timers and the format the regional committee accepts must be agreed with the municipality and Civil Protection. These contacts start in the first week of Phase~2.
\item \emph{Radio rules not confirmed.} Written confirmation from ANF is pending; until then the system runs within the conservative European limits.
\item \emph{Short lead time.} In small basins the water can arrive within an hour. The system promises no lead time; the beacon at the crossing is the protection that does not depend on it.
\item \emph{Costs are estimates.} Prices will be replaced by supplier quotes in the first sprint.
\end{itemize}

None of these limits the concept; each one has a test or a step in the plan. Our goal is not to measure water but to give people time to act, so that a natural hazard does not become a human tragedy.
```
