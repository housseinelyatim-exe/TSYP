# Review: RuralDirect solution proposal

**Reviewed file:** `~/Desktop/WIE_Solution_Documentation.pdf` (dated 11 Oct 2026)
**Status of the document:** an early solution proposal at the study stage. It is **not** the Phase 1 report.
**Target users:** women farmers **and** women artisans selling their products
**Reviewed against:** the challenge brief (TSYP14 WIE), Track 2

This review is about the **solution design**. Report formatting is covered briefly in §7, for later.

---

## 1. Overall assessment

The concept is solid and fits Track 2 well. You have a full chain from the producer to the customer, inclusive access (USSD/SMS, an agent, offline use), price transparency and traceability. You are also already thinking about the Tunisian context: e-Dinar, APIA, Law 2000-83 and INPDP.

The main gaps to settle while you study the project:

1. **The flow is designed for agricultural products only.** Artisans are a target group but don't appear in the design.
2. **There is no operator or business model yet.** Nobody is named to run the physical side, and nothing says who pays for it.
3. **Women's specific constraints don't yet drive design decisions.**
4. **Some concepts overlap or conflict:** lockers vs collection points, online vs shelf sales, and the payment flow.

---

## 2. Make the design cover both farmers and artisans

Every flow in the proposal (collection rounds, handling, storage, aggregation, the olive oil and tomato examples) is agricultural. Artisan products such as weaving, textiles, pottery, essential oils and processed foods behave differently:

| Aspect | Fresh agricultural | Shelf-stable agri-food (olive oil, couscous, honey, essential oils) | Artisanal (textiles, weaving, crafts) |
|---|---|---|---|
| Perishability | High, needs fast transport and sometimes cold storage | Low | None |
| Unit | kg / crate, bulk | Bottle / jar, batch | Single piece, often unique |
| Pricing | Per kg, market-dependent | Per unit | Per piece, based on time and skill |
| Selling point | Freshness, origin | Quality, purity, origin | Maker's story, technique, region, handmade |
| Ordering | Stock | Stock | Stock **or made-to-order** |
| Best storage/handover | Staffed collection point, quick turnaround | Collection point **or locker** | **Locker** or collection point |
| Traceability value | Freshness + origin | Anti-fraud (e.g. pure olive oil) | **Authenticity + the woman's story** |

**Suggestion:** define **product profiles** (Fresh / Shelf-stable / Artisanal) in the data model. The handling steps, storage, collection frequency and listing page would then depend on the profile. This also settles the lockers question (§5.1): lockers suit artisanal and shelf-stable products, while staffed collection points suit fresh produce.

Features specific to artisans:
- A **maker profile and story** (photo, village, technique, time to make). This is the main selling argument for crafts, and the QR code can lead to it.
- **Made-to-order / custom orders**, with a deposit and an estimated completion date.
- **Per-piece listings** with photos. The Community Market Agent can take good photos for women who cannot.
- **Extra sales channels:** tourist and handicraft shops, hotels, fairs, and possibly export later. The handicraft sector body ONAT (Office National de l'Artisanat) could be a partner; verify that it is relevant.
- **Artisan cooperatives or groups** as an onboarding route, similar to GDA/SMSA groups for farmers.

---

## 3. Put women at the centre of the design

The challenge explicitly asks for gender-inclusive engineering. The proposal says it serves "rural women", but none of the features is shaped by women's constraints yet. Turn the constraints into features:

| Constraint of rural women | Design response |
|---|---|
| Limited mobility, often dependent on others or on unsafe transport | Collection points close to villages, shared collection rounds, pickup for groups |
| Little time because of care work and farm work | Flexible drop-off windows, lockers for drop-off at any time, short onboarding |
| Shared or basic phone, often owned by a husband or child | USSD/SMS, a PIN-protected account, agent-assisted access |
| Low literacy or digital literacy | Voice/IVR or icon-based UI, Tunisian Arabic (Derja), agent support |
| Income captured by intermediaries or the household | **Payment into an e-Dinar wallet in her own name**, with a clear sale record |
| Informal status without official documents | Tiered verification (§5.5) |
| Little bargaining power | Price transparency, group selling, visible market prices |

**Recruit Community Market Agents among local women.** This creates paid jobs, builds trust and fits the empowerment goal.

**Validate before you design further.** Talk to 3–5 women farmers, 2–3 women artisans and one cooperative or GDA. Ask how they sell today, who transports their goods, how much the intermediary takes, which phone they use and who controls the money. These answers will tell you which features matter.

---

## 4. Define who operates it and who pays (the biggest open question)

The solution relies on **physical operations**: collection points, handling staff, storage, transport and agents. The proposal doesn't say who runs them. Choose a model:

| Option | Pros | Cons |
|---|---|---|
| **A. The platform runs logistics itself** | Full control | Expensive and hard to start |
| **B. Partner with existing cooperatives (GDA/SMSA, artisan associations)** to run collection points, while the platform provides software and coordination | Low cost, existing trust and premises | Depends on how active each cooperative is |
| **C. Third-party transporters, paid per round** | Flexible | Requires enough volume per round |

**Option B + C** looks the most realistic for a student project and a pilot.

Points to settle as well:
- **Revenue:** today the example gives the platform 1 TND out of 20 (5%). Is that enough? Could you add subscriptions for partner markets, B2B buyer fees or NGO/program funding at the start?
- **Partner shops:** what does a supermarket or craft shop gain? Local, traceable products, a CSR image, a margin. Is it **consignment** (the woman bears the risk of unsold items) or a **firm purchase**?
- **Damage and spoilage:** who bears the loss between drop-off and sale?
- **Prove the gain:** compare what a woman earns today through an intermediary with what she would earn on RuralDirect for one product. Use real numbers from your interviews.

---

## 5. Design inconsistencies to resolve

### 5.1 Lockers vs collection points
The document uses both terms interchangeably. With product profiles (§2), the split is natural: **lockers** for artisanal and shelf-stable products, available at any time, and **staffed collection points** for fresh produce during collection rounds.

### 5.2 Online orders vs shelf sales
- **Online orders:** the customer orders on the platform, so the sale and payment are known.
- **Shelf sales at a partner shop:** the platform doesn't see the sale at the checkout.

For shelf sales, decide how a sale reaches the producer's dashboard: the shop reports it, the batch is marked sold when the shop receives it (firm purchase), or the shop's checkout system is integrated. Also decide **when the woman gets paid**: on drop-off, on sale or on a weekly settlement. This matters a lot to her.

### 5.3 Payment flow
If RuralDirect collects the customer's money and splits it, it acts as a payment intermediary, which requires central bank (BCT) authorisation. Design it so that **money never passes through the platform**. Either the licensed provider (La Poste e-Dinar or a payment institution) does the split, or the partner shop pays producers directly and the platform keeps only the ledger. Also plan for **cash** payments.

### 5.4 Traceability you can trust
Producers and operators enter the QR data themselves. Make it credible:
- Each step is confirmed by a different actor (producer, then operator, then shop).
- An append-only audit log, which you already have as an entity.
- Optional quality checks for products prone to fraud, such as olive oil acidity or essential-oil purity.
- For artisanal products, maker verification (the agent saw the item being made).

### 5.5 Verification without excluding women
Requiring official agricultural or business documents (the APIA guide) would exclude many women who work informally. Use **tiered verification**:
- **Basic:** ID plus an agent visit or cooperative membership. This is enough to sell through the platform.
- **Full:** legal status and documents, needed for B2B contracts or supermarkets.

The platform can then **help women formalise step by step**, which is itself an impact argument.

### 5.6 Food safety and labelling
Processed food (olive oil, couscous, jams, honey) sold in shops needs sanitary and labelling compliance. Find out which authority applies in Tunisia (likely INSSPA; verify). The platform can help producers meet these rules through templates, label generation and cooperative-level certification.

---

## 6. Other remarks

- **The AI optimisation module** is the most innovative part, but it is currently a "possible extension". Decide whether it is core. If it is, keep it simple and credible: group producers by location and quantity, then use a vehicle-routing solver (e.g. OR-Tools). Note that **demand forecasting cannot work at launch**, because a new platform has no order history. Start with quantities declared by producers and orders from partner shops.
- **Technical architecture:** §15 repeats the business flow. When you get to it, draw the software components (PWA with offline sync, API, database, SMS/USSD gateway, payment adapter, QR service, roles/permissions, optimisation module) and the relations between entities.
- **USSD** needs an agreement with a mobile operator and costs money. For the prototype, use a simulator and present operator partnership as the deployment path.
- **Track 1 and Track 3 links are weak.** Keep Track 2 as the clear primary track. The most convincing Track 3 argument is that **shared, organised collection reduces women's travel in unsafe informal transport**, which is a known issue in Tunisia (find a source).
- **Small fixes in the current draft:** steps 9 and 10 of the example are duplicates. The price example has no unit (per litre? per bottle?). The heading "Access Without a Smartphone" also lists smartphones. The tomato example appears without any process for fresh produce.

---

## 7. For later: when you turn this into the Phase 1 report (due 05 Nov 2026)

- Required structure: Title, Abstract (150–250 words), Keywords (3–6), Introduction, Related Work, Methodology, Results & Discussion, Conclusion & Future Work, References. **Maximum 6 pages.**
- Add **sourced numbers** on the problem (INS, ONAGRI, FAO, World Bank Global Findex, CREDIF). Use your interview findings as well.
- Related Work: compare with intermediaries, existing marketplaces and aggregation models (e.g. Twiga Foods in Kenya), and state your differentiator in one sentence.
- Results: prototype screenshots plus a simulated collection round (trips, km and cost/kg before vs after aggregation).
- The brief warns about **AI-content and plagiarism detection**, so write the report in your own words.

---

## 8. Questions to answer during the study phase

1. Which products will the pilot cover? Suggestion: **one shelf-stable agri-food product (olive oil) plus one artisanal product (e.g. woven textiles)** in one region.
2. Who operates the collection points? Is there a cooperative or GDA you can partner with?
3. Which sales channel comes first: online, a partner shop or a craft/tourist shop?
4. Consignment or firm purchase? When is the woman paid?
5. How will the money flow? Which licensed provider handles payments?
6. What do women earn today, and what would they earn with RuralDirect?
7. Is the AI optimisation module core or a later extension?
