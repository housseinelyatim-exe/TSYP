# AOTN — Phase 1 Problem Development
**Pillar:** Sustainable Industry
**Candidates:** #3 Small Manufacturer Digitization Gap · #4 Predictive Maintenance for Aging Industrial Equipment

---

## #3 — Small Manufacturer Digitization Gap

### Problem Statement
Small and micro-manufacturers in Tunisia (textile ateliers, food processing units, artisan workshops) manage orders, inventory, and quality control on paper or WhatsApp, causing lost orders, stockouts, and zero traceability — because existing ERP/inventory software is priced and designed for large enterprises, not their scale or budget.

### SDG Alignment
- **SDG 9** — Industry, Innovation and Infrastructure (primary)
- **SDG 8** — Decent Work and Economic Growth (secondary — formalizing informal operations improves job stability and productivity)

### Affected Groups & Needs Assessment

| Group | How the problem impacts them | Why a solution is needed |
|---|---|---|
| Small manufacturer / atelier owners (5–50 employees) | Lost revenue from stockouts and missed orders; no data to negotiate with suppliers or apply for credit | No affordable tool exists at their scale — enterprise ERPs are too expensive and complex |
| Employees / floor workers | Manual, error-prone processes; no visibility into their own output or performance | Digitization reduces error rates and gives workers clearer task tracking |
| B2B buyers / distributors sourcing from these manufacturers | Unreliable delivery estimates, no order tracking, trust issues | Order visibility improves reliability of the whole downstream chain |
| Banks / microfinance institutions | Can't assess creditworthiness without financial or production records | Digital records unlock access to credit for a segment currently excluded |

**Stats to source for the 2-page needs assessment (needs a quick data pass before submission):**
- INS (Institut National de la Statistique) or UTICA figures on the share of Tunisian manufacturing employment held by small/micro enterprises
- World Bank / ITU MENA SME digitalization-gap indices
- ANPME data on registered small-manufacturer count, if available

### Field Validation Plan (minimum: 1 domain expert + 3 target users)
- **Domain expert (1):** UTICA representative, ANPME advisor, or a business-development consultant working with ateliers — validates market size, pricing tolerance, and why current ERP tools don't fit this segment.
- **Target users (3):** Small manufacturer/atelier owners across **at least 2 sectors** (e.g., textile + food processing) to avoid a sector-locked problem statement.

**Interview questions to standardize across all 4:**
1. How do you currently track orders and inventory?
2. Describe the last time a paper/WhatsApp-based mistake cost you money or a customer.
3. What would you be willing to pay monthly for a tool that fixed this? *(business-case data point)*
4. What's stopped you from adopting existing software before?
5. *(Domain expert only)* How large is this segment, and what's kept enterprise ERP vendors from serving it?

### Business Case Angle
- **Model:** SaaS subscription, tiered by shop size/employee count
- **TAM:** sized from INS/UTICA small-manufacturer counts
- **Unit economics:** CAC via direct atelier outreach + word-of-mouth in industrial zones; LTV from subscription retention
- **Differentiator vs. incumbents:** priced and designed for micro-scale (not a stripped-down enterprise ERP)

### Prototype Scope (Phase 3)
Lightweight web/mobile app — order intake, inventory count, basic production tracking, WhatsApp-simple UX. Fits directly into a Next.js/React/Tailwind stack — low build risk, fast to demo.

### Risk Notes
- Low technical risk, but differentiation from generic "inventory app" competitors needs to be sharp in the pitch
- Business case depends heavily on getting a real willingness-to-pay number from interviews — don't skip that question

---

## #4 — Predictive Maintenance for Aging Industrial Equipment

### Problem Statement
Small and mid-size Tunisian manufacturers run aging machinery with no predictive maintenance in place, relying on reactive repair after breakdown — causing unplanned downtime, production losses, and safety incidents that disproportionately hurt factories too small to afford enterprise-grade condition-monitoring systems.

### SDG Alignment
- **SDG 9** — Industry, Innovation and Infrastructure (primary)
- **SDG 8** — Decent Work and Economic Growth (secondary — reduces safety incidents and unplanned labor disruption)

### Affected Groups & Needs Assessment

| Group | How the problem impacts them | Why a solution is needed |
|---|---|---|
| Factory owners / operations managers | Revenue loss per downtime hour; unplanned repair costs | No affordable monitoring exists at their equipment scale |
| Machine operators | Safety exposure to failure-prone equipment | Early warning reduces injury risk |
| Maintenance technicians | Reactive, unplanned workload; no diagnostic data to prioritize repairs | Predictive signals let them plan instead of react |
| Downstream clients relying on delivery schedules | Cascading delays from unplanned factory downtime | Reduced downtime improves delivery reliability |

**Stats to source:** Global unplanned-downtime cost studies (Deloitte, Siemens) exist but are foreign — use them only as context, and anchor the actual claim in numbers from your own interviews (estimated downtime hours/cost reported by the factories you speak to).

### Field Validation Plan (minimum: 1 domain expert + 3 target users)
- **Domain expert (1):** Industrial equipment vendor or senior maintenance technician who can speak to failure modes across multiple machine types.
- **Target users (3):** Maintenance managers or factory owners across **at least 2 sectors** (e.g., textile, food processing, metalworking) — Ben Arous/Grombalia industrial zones are geographically convenient.

**Interview questions to standardize across all 4:**
1. How do you currently detect or anticipate equipment failure?
2. Walk me through your last unplanned breakdown — cost, downtime, safety impact.
3. What would you pay monthly/yearly for early-warning monitoring on your critical machines?
4. What's stopped you from adopting condition-monitoring systems already on the market?
5. *(Domain expert only)* What failure modes are most common and most predictable across the equipment types you service?

### Business Case Angle
- **Model:** hardware sensor node (one-time or leased) + subscription for analytics/alerts
- **TAM:** harder to size cleanly than #3 — depends on machinery age/type data that may not be publicly tracked in Tunisia; expect to estimate from interviews
- **Differentiator vs. incumbents:** low-cost retrofit sensor vs. enterprise-grade systems (e.g., Siemens MindSphere-class tools) that are priced out of reach for this segment

### Prototype Scope (Phase 3)
Sensor node (e.g., ESP32 + accelerometer/temperature) feeding a simple anomaly-detection model, with a dashboard. Visually strong demo, but heavier build risk — needs embedded hardware familiarity or a fallback plan (simulated sensor data) if the physical build slips.

### Risk Notes
- **Given the challenge is weighted toward business over technical execution, this option spends more effort on a dimension that isn't rewarded as heavily.**
- TAM and unit economics are harder to size credibly without deeper equipment-age data
- Real risk of the hardware build slipping and eating time needed for the business case

---

## Recommendation
Given the explicit business-over-technical weighting, **#3 (Small Manufacturer Digitization Gap)** is the stronger choice: cleaner TAM sizing, lower build risk, and a business model (tiered SaaS) that's easier to defend with hard numbers from 4 interviews. #4 remains a valid backup if hardware execution becomes a differentiator later, or if #3's field validation reveals the problem isn't painful/costly enough to sustain a paid product.
