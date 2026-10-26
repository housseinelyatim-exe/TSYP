# RuralDirect: ideas for using AI

The AI should solve **real problems of the women using the platform**: low literacy, limited time, weak bargaining power and transport difficulties. It should not be there for decoration. A new platform also has **no historical data**, so ideas that work from day 1 are more valuable than ideas that need months of sales history.

Every idea below says whether it works **from day 1** or only **after data is collected**.

---

## 1. Ideas focused on the women (inclusion)

### 1.1 Voice listing in Tunisian Darija ⭐ (strongest idea)
**Problem:** many rural women can't easily type or read an app.
**How it works:** she sends a voice message (by app, WhatsApp, or a phone call to an agent line), for example *"I have 20 litres of olive oil, I want 15 dinars per litre"*.
1. Speech-to-text converts the Darija audio into text.
2. An LLM extracts the fields: product = olive oil, quantity = 20 L, price = 15 TND/L.
3. The system **reads the listing back** to her (text-to-speech) or shows it with icons, and she confirms.

**Why it's strong:** it is directly gender-inclusive, works from day 1 and is a clear differentiator.
**Tech:** Whisper-type speech models (check Hugging Face for models fine-tuned on Tunisian Arabic), plus an LLM API for extraction.
**Risk:** Darija recognition errors. That is why the confirmation step is mandatory.

### 1.2 Voice / chat assistant (WhatsApp or SMS)
She asks in Darija: *"When is the next collection?"*, *"How much did I earn this month?"*, *"Was my oil sold?"*. The assistant answers from **her own data** in the database. It does not invent answers.
**Day 1:** yes.
**Tech:** an LLM with function calling over the platform API.

### 1.3 Automatic translation of listings
A listing written in Arabic is shown in French and English to city customers, tourists or future export buyers. This is especially useful for artisans selling to tourists.
**Day 1:** yes.

---

## 2. Ideas for artisans

### 2.1 Photo to listing ⭐
She (or the agent) takes a photo of a carpet, a basket or a jar of harissa. The AI then:
- **checks the photo quality** (blurry, too dark) and asks for a retake;
- **removes or cleans the background** so it looks professional (e.g. `rembg`);
- **suggests a category, title and description** in AR/FR/EN.

She validates or edits before anything is published.
**Day 1:** yes.

### 2.2 Maker story generator
The agent records a 1-minute interview: who she is, her village, the technique, how long the piece took. The AI turns it into a short **"meet the maker"** story. The QR code on the product links to that story. This is the main selling argument for handmade products, and it builds authenticity.
**Day 1:** yes. Requires **consent**, and she decides what is shown (privacy, INPDP).

---

## 3. Ideas for fair pricing and income

### 3.1 Fair price suggestion ⭐
**Problem:** women often accept whatever price the intermediary offers.
- **Agricultural products:** compare her price with current market and wholesale prices (find a public source such as ONAGRI or wholesale market bulletins; verify availability), plus platform sales once they exist.
  → *"Similar olive oil sells at 16–19 TND/L in Tunis this month."*
- **Artisanal products:** a simple helper based on cost of materials + hours of work × a fair hourly rate + platform fees → minimum fair price.

**Day 1:** partly (rule-based + public prices); it improves with data.
**Impact:** this directly addresses the challenge's "bargaining power" problem.

### 3.2 Income insights
A monthly summary in voice or SMS: *"You sold 45 L this month, 20% more than last month. Your best buyer is shop X."* It is simple, motivating and helps her plan.

---

## 4. Ideas for logistics (the core of Track 2)

### 4.1 Smart collection rounds and route optimisation ⭐ (already in your proposal)
- **Group producers** by location and declared quantity (clustering, e.g. K-means / DBSCAN on GPS points).
- **Optimise the route and vehicle loading** with a vehicle routing solver (Google **OR-Tools**), taking into account vehicle capacity, fresh vs non-fresh products and the delivery deadline.
- **Decide when a round is worth running:** e.g. launch the round when the total declared quantity is enough to fill the vehicle at an acceptable cost per kg.

**Day 1:** yes. It only needs declared quantities and locations, no history.
**Demo idea:** show a map with 10 producers, comparing separate trips with one optimised round, and display km, cost and CO₂ saved. Judges see the impact visually.

### 4.2 Group selling to meet big orders
A hotel or supermarket wants 500 L of olive oil, which no single woman has. The AI **combines several women's stock** to fill the order and splits the revenue fairly by quantity. This opens bigger buyers to small producers.
**Day 1:** yes. This is mostly a matching and optimisation algorithm.

### 4.3 Shelf-life priority for fresh products
Estimate the remaining freshness of a batch (product type, harvest date, temperature, time in storage) and **prioritise transport** for batches at risk of spoiling. Start with rules per product and refine with ML later.

---

## 5. Ideas that need data first (phase 2 / future work)

### 5.1 Demand forecasting
Predict what customers and shops will order by product, region and season. Include Tunisian seasonality: Ramadan, Eid, the olive harvest (Nov–Jan) and the tourist summer for crafts.
- **Start:** simple baselines (moving average, last year's same week).
- **Later:** Prophet / gradient boosting once there are a few months of orders.

Honest point for the report: forecasting **can't work at launch**. Before that, use orders from partner shops and quantities declared by producers.

### 5.2 Recommendations for customers
"Customers who bought this olive oil also bought this honey." This is a classic recommender, useful only once there is traffic.

### 5.3 Anomaly / fraud detection in traceability
Flag suspicious data: quantities that don't match between drop-off and reception, a producer declaring far more than plausible for her land, duplicate listings, or prices far from the norm. **Day 1** with simple rules, then ML later.

---

## 6. Optional: link to Track 1 (automation)

### 6.1 Visual quality grading of fresh produce
A camera at the collection point grades fruit or vegetables (size, defects, ripeness) to speed up manual sorting. Image classification can be done with a fine-tuned small model (e.g. MobileNet/YOLO). Public fruit-quality datasets exist.
This is a genuine "reduces manual work" link to Track 1, but it is **more work** (dataset, camera setup). Keep it as future work unless the team has computer-vision experience.

---

## 7. Recommendation for your prototype

Choose **3 AI features** that work from day 1 and tell a clear story:

| Feature | Who it helps | Why judges will like it |
|---|---|---|
| **Voice listing in Darija** (1.1) | Women with low literacy | Gender-inclusive and original |
| **Photo to listing + maker story** (2.1 + 2.2) | Artisans | Visible, impressive in a demo |
| **Smart collection rounds** (4.1) | All producers and operators | Core of Track 2, measurable impact (km, cost/kg, CO₂) |

Then mention **fair price suggestion (3.1)** and **demand forecasting (5.1)** as the next step once data exists.

A one-sentence pitch: *"AI that lets a woman sell by speaking, makes her products look professional, and organises shared collection so she doesn't travel alone to the market."*

---

## 8. Design rules to state in the report

- **A human always confirms.** The woman validates her listing and the operator validates the route. The AI only suggests.
- **Offline-first still applies.** AI features need connectivity, so they run on the server or on the agent's phone. A woman without internet still uses SMS/USSD, and the agent does the AI-assisted part.
- **Privacy:** voice recordings, photos and stories are personal data. Get consent, keep the minimum, and apply INPDP rules.
- **Cost:** estimate the cost per AI call (speech-to-text + LLM) per listing and include it in the business model.
- **Language:** test with real Darija voices from your interviews before claiming that it works.

---

## 9. Possible tech stack

| Need | Option |
|---|---|
| Speech-to-text (Darija) | Whisper or Tunisian fine-tuned variants (Hugging Face); test accuracy |
| Text extraction / assistant / descriptions / translation | An LLM API (e.g. Claude) with structured output and function calling |
| Text-to-speech (read back) | A TTS model or service supporting Arabic |
| Background removal | `rembg` |
| Clustering + routing | scikit-learn + Google OR-Tools |
| Forecasting (later) | Moving average baseline, then Prophet / LightGBM |
| Messaging channel | WhatsApp Business API / SMS gateway |
| Integration | FastAPI services next to your existing backend |

---

## 10. AI marketing agent for Meta ads (Facebook / Instagram), an extension, not a pillar

**Verdict:** feasible as a **human-approved prototype** and a **small-budget pilot**. It is not realistic as an autonomous production system, and it is less central than the Track 2 core (collection, aggregation, traceability). Pitch it as an extension.

### 10.1 Why it makes sense
- Many Tunisian buyers already shop on Facebook and Instagram, and many women artisans already sell through pages, groups and Messenger. *(Confirm this with your interviews or a source before stating it in the report.)*
- It fills a gap in the solution: RuralDirect moves products to the market, and the agent brings customers to the products.
- Interviews should confirm that the women lack the time or experience to run paid campaigns. Don't state it without evidence.

### 10.2 What the agent does and doesn't do
```
Inputs                               Agent steps                                  Output
──────────────────────────────────   ──────────────────────────────────────────   ────────────────────────────────
• RECEIVED, in-stock batches only    1. Select products to promote:               • 1-page strategy brief
  (post-reception status, NOT          in stock + in season + margin allows ads    • Ad copy AR / FR / EN
  declared quantities)               2. Check max cost per sale (margin rule)      • Image/format variants
• Verified product data (QR /        3. Suggest audience                          • Organic post calendar
  traceability) for claims           4. Write copy + adapt creatives              • Campaign draft, PAUSED
• Photos + maker stories (consent)   5. Create campaign draft (paused)            • Weekly recommendations
• Season calendar                    6. Read results → RECOMMEND changes            to the operator
• Budget + margin per product           to the operator
```

**The agent can't:**
- spend money without human approval (operator "Approve & launch", weekly budget cap);
- promote declared or uncollected quantities, only **received, in-stock batches**, so it never sells what hasn't been collected;
- make claims ("organic", "traditional", "pure") that aren't backed by verification or traceability data;
- publish Darija or Arabic copy without human review, because LLM dialect output is uneven.

**Margin rule:** each product has a **maximum acceptable cost per sale**, derived from its margin. The agent **refuses to promote products where ads would lose money.** This is a good argument for the jury.

### 10.3 Which products and channels are worth paying for
- Paid ads only make sense for **higher-value items** (olive oil in larger volumes, carpets, large baskets), **B2B buyers** (hotels, restaurants, shops), and **tourist and diaspora buyers** for crafts. A 20 TND item with a 1 TND platform fee can't pay for paid customer acquisition.
- **Conversion path:** many Tunisian sales close on Messenger, Instagram or WhatsApp DMs with cash on delivery. **Click-to-message ads** may convert better than website-link ads. The conversations then need handling by an operator, agent or chat assistant (§1.2).
- **Start organic:** the content calendar for the RuralDirect page and the women's pages is free, needs no Meta approval and works from day 1.

### 10.4 How to build it
| Part | Tool |
|---|---|
| Agent (planning, copy, recommendations) | LLM with tool calling in a FastAPI service |
| Agent tools | `get_received_stock()`, `get_margin_rules()`, `get_season_calendar()`, `get_verified_claims()`, `generate_ad_copy()`, `create_campaign_paused()`, `get_ad_insights()` |
| Product catalog on Meta | Commerce Catalog synced from PostgreSQL, **received stock only** |
| Campaigns + results | Meta Marketing API (campaigns, ad sets, ads, Insights) |
| Conversion tracking | Meta Pixel / Conversions API on the PWA product pages. The marketplace therefore needs public product pages. |
| Prototype | Meta sandbox ad account (no real spending) |
| Approval | Operator dashboard: review copy → "Approve & launch" |

### 10.5 Risks and how to handle them
| Risk | Mitigation |
|---|---|
| **Meta API access.** Managing *other* businesses' ad accounts (e.g. each woman's page) requires advanced permissions, App Review and Business Verification with legal documents, which a student or informal project may not have. | Run everything from **one RuralDirect-owned business and ad account** for the pilot. Check the current access tiers in Meta's developer documentation, because they change. |
| **Unit economics.** Ad cost per order is likely higher than the platform fee. | Margin rule (§10.2), ads only for high-value, B2B and tourist products, and track cost per sale. |
| **Paying Meta from Tunisia** depends on international card limits. | Check early. It could block the pilot. Don't claim the women can self-fund ads. |
| **Small budgets give too little data** for A/B testing, and Meta already optimises delivery. | Weekly **recommendations** to the operator, not autonomous budget moves. |
| **Content and policy.** Dialect quality, unsupported claims. | Human review, claims only from verified data, Meta ad policy check. |
| **Privacy.** Maker stories and photos are personal data. | Written consent from each woman (INPDP). |

### 10.6 Success metrics
- Cost per sale (and cost per sale vs. margin per product)
- Sales generated by campaigns, by product and by woman
- Share of agent drafts approved without major edits
- Operator hours of marketing work saved per week
- Click-to-message conversations → completed orders

### 10.7 Scope by phase
| Phase | Scope | Risk |
|---|---|---|
| **Phase 1 (report)** | Present as a planned extension. Mock-up of a generated brief + AR/FR/EN copy + organic calendar. | Low |
| **Phase 2 (demo)** | Agent selects olive oil (harvest season, in stock, margin OK) → brief + 3 ads → paused campaign in the sandbox → operator approves | Low |
| **Pilot** | One RuralDirect-owned ad account, 1–2 high-value products, small budget, weekly report | Medium |
| **Scale** | Accounts per producer or cooperative, advanced API access, Business Verification | High |

Pitch line: *"The women make the products, RuralDirect brings them to the market, and the AI agent brings the customers, only when it is profitable for them."*
