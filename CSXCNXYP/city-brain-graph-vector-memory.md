# City Brain: Graph + Vector Database Add-on

**Extends:** [`city-brain-phase1-proposal-v2.md`](city-brain-phase1-proposal-v2.md) · 8 October 2026

> **Idea in one line:** a **city graph** tells the Brain *how the city is connected* (what is upstream, what feeds the hospital, which road leads where). A **vector database** tells it *what happened before* (similar past incidents, what worked, known attack texts). Together they give the local LLM and the math model a memory and a map.

---

## 1. What each part is for

| | City graph | Vector database |
|---|---|---|
| **Answers** | "What is connected to what?" | "What looks similar to this?" |
| **Contains** | Zones, sensors, actuators, units, critical assets, roads, pipes, power lines, as nodes and edges | Text embeddings of past incidents, response playbooks, known attack messages |
| **Lookup** | Exact: neighbours, paths, upstream/downstream, k hops | Approximate: top-k most similar by meaning |
| **Used by** | Math model (cost, exposure, cascades) **and** LLM | Mainly the LLM, plus learned effectiveness in the math model |
| **Example** | "Which valves are upstream of the port?" → `valve-port-up`, `valve-river-2` | "Has a flood like this happened before?" → episode #14, valve-port-up worked in 40 s |

Neither is useful alone for our case: the vector DB finds a similar past flood, but only the graph knows that **this time** the downstream zone is a hospital. The combination is called **GraphRAG** (graph + retrieval-augmented generation).

---

## 2. The city graph

### 2.1 Schema

```
 (Zone)──ADJACENT_TO{dist}──(Zone)          (Zone)──FLOWS_TO──(Zone)          water flow direction
   ▲  ▲                                       ▲
   │  └──LOCATED_IN──(Sensor)──MONITORS──┐    └──CONTROLS──(Actuator: valve, signal, grid switch)
   │                                     │
   ├──LOCATED_IN──(Asset: hospital, school, substation)──FEEDS──▶(Zone|Asset)   power dependency
   ├──LOCATED_IN──(Unit: ambulance, fire, police)      status: free | busy
   └──ROAD{capacity}──(Zone)
 (Incident: past)──OCCURRED_IN──▶(Zone)   (Incident)──RESOLVED_BY──▶(Action)──USED──▶(Actuator|Unit)
```

| Node | Key attributes |
|---|---|
| `Zone` | id, type (residential, port, industrial), base exposure |
| `Sensor` | id, type, unit, alert/max levels, **live trust τ** |
| `Actuator` | id, type, state, **quarantined** flag |
| `Unit` | id, type, status, current zone |
| `Asset` | id, type, criticality (hospital 1.0, school 0.7, substation 0.8) |
| `Incident` | id, type, time, outcome, link to its vector-DB entry |

### 2.2 Where the graph comes from
- **Structure:** built at startup from the retained MQTT topics `twin/meta/zones` and `twin/meta/sensors`, plus a small `city_graph.yaml` for what the Twin doesn't publish (assets, water flow, power lines).
- **Live state:** updated from MQTT: unit status (`city/units/…`), trust (`guardian/verdict/…`), quarantine (`guardian/quarantine/…`), actuator state (`twin/ack/…`).
- **Ask the Twin team** to include `flows_to` and `feeds` in `twin/meta/zones`. If they don't, `city_graph.yaml` covers it, and a different partner's Twin only needs a new YAML file.

### 2.3 What the graph adds to the math model

| Model term (v2 §4) | Before | With the graph |
|---|---|---|
| Cost c_a | Zone hops (simple) | Shortest path on `ROAD` edges weighted by distance and live congestion |
| Exposure E_z | Fixed per zone in config | `E_z = 1 + Σ criticality of assets in z or fed by z` (1-hop on `LOCATED_IN` and `FEEDS`) |
| Candidate actuators | All valves in the zone | Valves that `CONTROLS` the zone **or are upstream** on `FLOWS_TO` |
| Cascade risk | Not modelled | Incident in z raises priority of zones reachable by `FLOWS_TO` / `FEEDS` within 2 hops: `P_z' += γ^hops · P_z` (γ = 0.5) |
| Independence rule | Different sensor IDs | Different sensors **not on the same feed or gateway** (graph check), harder to fake with one compromised device |

**Example (cascade):** fire in the industrial zone. The graph shows `substation-3 FEEDS hospital-1`. Exposure of the fire jumps from 1.0 to 1 + 0.8 (substation) + 1.0 (hospital it feeds) = 2.8, so its priority nearly triples and it wins the only free fire unit against a minor fire elsewhere. The why card shows the path `fire → substation-3 → hospital-1`.

---

## 3. The vector database

### 3.1 Collections

| Collection | What's inside | Written by | Used for |
|---|---|---|---|
| `incidents` | One entry per **resolved** incident: short text summary, type, zone, actions, outcome, time to resolve, U values | Brain, after resolution | "Similar past cases" for the LLM; learning effectiveness e_a |
| `playbooks` | Response procedures written by the team (flood, fire, accident, jam, power), split into small chunks | Team, before the event (read-only at runtime) | Grounding the LLM in proper procedure |
| `attack_patterns` | Known prompt-injection texts, spoofing descriptions, fake-call styles | Team + Guardian's confirmed attacks | Similarity check on every emergency call (B10) |

Each entry stores the **vector** plus a **payload** (metadata) with graph node IDs (`zone_id`, `actuator_id`…). That payload is the bridge between the two databases.

### 3.2 Embeddings on the edge device
- A small local embedding model on the same device as the LLM (e.g. `all-MiniLM-L6-v2`, ~90 MB, 384 dimensions, or `nomic-embed-text` via Ollama).
- About 10–50 ms per text on CPU. Calls and summaries are short, so this is cheap.
- Same offline guarantee as the LLM: nothing leaves the local network.

### 3.3 What the vector DB adds to the math model: learned effectiveness

Instead of a fixed effectiveness e_a from `rules.yaml`, use past outcomes of **similar** incidents (top-k from `incidents`) as a Bayesian update:

```
e_a = (α · e_prior + successes_a) / (α + n_a)          α = 4 (prior strength)
```

- `e_prior` is the value from `rules.yaml`.
- `n_a` = how many of the k similar past incidents used action a, `successes_a` = how many of them resolved within the deadline.
- With no history, e_a = e_prior. With history, it moves towards what actually worked.

**Example:** prior e = 0.8 for `valve-port-up`. In 5 similar past floods it was used 5 times and worked 2 times (it was often stuck). e = (4 × 0.8 + 2) / (4 + 5) = **0.58**, so the alternative valve now scores higher. The Brain *learned* from its own logs, and the numbers explain why.

---

## 4. How a lookup works (GraphRAG pipeline)

When the LLM is asked about an incident:

```
 1. Incident summary text ──embed──▶ query vector
 2. Vector DB: top-5 similar past incidents (filter: same type)        ~10 ms
              + top-3 playbook chunks for this incident type
              + similarity of call text to attack_patterns
 3. Take the node IDs from their payloads + the current zone
 4. Graph: expand 2 hops from the current zone                          < 1 ms
           (upstream valves, adjacent zones, critical assets, free units + distance,
            quarantined devices, sensor trust)
 5. Build a compact "context pack" (~300–400 tokens)
 6. Send it with the city summary on brain/llm/request
```

**Context pack example (what the LLM actually receives):**

```json
{
  "incident": "flood/port, C=0.76, severity 0.4",
  "graph": {
    "upstream_valves": [
      {"id":"valve-port-up","state":"closed","quarantined":false},
      {"id":"valve-river-2","state":"closed","quarantined":false}
    ],
    "downstream": ["docks (residential)", "hospital-1 via FLOWS_TO, 2 hops"],
    "free_units": [{"id":"rescue-1","eta_s":140}]
  },
  "similar_past": [
    {"id":"inc-14","summary":"port flood, valve-port-up stuck, river-2 worked in 40 s","outcome":"resolved"},
    {"id":"inc-09","summary":"port flood after rain, valve-port-up worked","outcome":"resolved"}
  ],
  "playbook": "Flood: 1) isolate inflow upstream 2) close inbound roads 3) rescue if severity > 0.6",
  "call_attack_similarity": 0.12
}
```

**Tools the LLM can call** (same MQTT request/response as v2):

| Tool | Backend |
|---|---|
| `graph_neighbours(node_id, hops, edge_types)` | Graph |
| `graph_path(from, to)` | Graph (road or flow path) |
| `similar_incidents(text, k, type)` | Vector DB |
| `get_playbook(incident_type, question)` | Vector DB |

---

## 5. Technology options

### 5.1 Graph store

| Option | Pros | Cons |
|---|---|---|
| **NetworkX (in memory)** ⭐ | Pure Python, zero setup, very fast for a few hundred nodes, easy to test, BFS/shortest path built in | No query language, persistence by saving to JSON |
| Neo4j | Cypher queries, nice browser view, built-in vector index too | JVM, ~1 GB RAM: heavy for an edge device; another container to keep alive on stage |
| Memgraph | Cypher, in-memory, fast | Another server; less familiar |

Our city graph is small (tens of zones, a few hundred nodes), so a database server isn't needed. **NetworkX is enough**, and the graph is rebuilt from MQTT retained topics on startup anyway.

### 5.2 Vector store

| Option | Pros | Cons |
|---|---|---|
| **Qdrant** ⭐ | Light (Rust), Docker or embedded, **payload filters** (type, zone) in the same query, good docs | One more container (or use its local mode) |
| Chroma | Simplest Python API, embedded | Slower filtering; less robust under concurrent use |
| FAISS | Fastest raw search | Library only: no metadata or filters, we'd build that ourselves |
| sqlite-vec | One file, SQL | Young project, fewer features |

### 5.3 Overall design options

| Option | Pros | Cons |
|---|---|---|
| **O1. Graph only** | Biggest gain for the math model (cost, exposure, cascades); easy | No memory of past incidents, no learning |
| **O2. Vector only** | Past incidents + playbooks for the LLM | Doesn't know the city's structure; can't answer "what's upstream?" |
| **O3. NetworkX graph + Qdrant vectors, linked by node IDs** ⭐ | Both benefits; light enough for the edge; each part testable alone | Two stores to keep consistent (handled by node IDs in payloads) |
| O4. Neo4j with native vector index | One database for both | Heavy for the edge device; more setup risk on stage |
| O5. Full GraphRAG framework (LLM extracts a graph from documents) | Popular, impressive name | Needs a big LLM and lots of time to build the graph; our graph is already known from the Twin, so there's nothing to extract |

**Recommendation: O3.**

---

## 6. Security: protecting the memory

A memory the attacker can write into is a new attack surface. Rules:

| Threat | Defence |
|---|---|
| **Memory poisoning** (attacker gets fake incidents stored so they're "remembered") | Only write to `incidents` after resolution, when the triggering sensors were `trusted` and the closed-loop check confirmed the effect. Every entry has provenance (`correlation_id`, verdicts) |
| Injected text stored and retrieved later | Raw call text is never stored; only the Brain's own generated summary. Retrieved content is labelled as data in the prompt |
| Tampering with playbooks | `playbooks` and `attack_patterns` are read-only at runtime, loaded from files in the repo with a hash check |
| Retrieved past case pushes a wrong action | It only changes the context and e_a; the action still has to pass U > 0 and the policy gate |
| Fake graph structure from a malicious Twin | Graph metadata is validated against `city_graph.yaml` (unknown edges are logged and ignored for high-risk actions) |

**Bonus security feature:** the `attack_patterns` similarity score is published on `brain/event` and can be shared with Guardian. A call scoring above 0.8 is flagged as a likely injection before the LLM even reads it.

---

## 7. New demo scenarios

| ID | Scenario | What the jury sees |
|---|---|---|
| B13 | **Cascade**: fire near substation-3 | Graph shows `substation-3 FEEDS hospital-1`; priority rises; the why card shows the path |
| B14 | **Learning**: third port flood with valve-port-up stuck again | Memory lowers e(valve-port-up) from 0.8 to 0.58; Brain picks valve-river-2 first time |
| B15 | **Injection recognised**: call text similar to a known attack | Similarity 0.91 → flagged, Guardian notified, LLM sees it labelled as suspicious |
| B16 | **Memory poisoning attempt**: fake incident during an attack | Incident not stored (sensors not trusted); timeline shows `memory_write_refused` |

The timeline can also show the **city graph live** (zones coloured by incident state, quarantined devices greyed out). It's a strong visual for the demo and helps the jury follow cause and effect.

---

## 8. Impact on the plan

| Week | Graph | Vector DB |
|---|---|---|
| **2 (12–18 Oct)** | Build graph from `twin/meta/*` + `city_graph.yaml`; cost and exposure in the math model | Pick embedding model on the edge device (with the LLM benchmark) |
| **3 (19–25 Oct)** | Cascade propagation, upstream valve lookup, LLM graph tools | Qdrant up; `playbooks` + `attack_patterns` loaded; context pack sent to the LLM |
| **4 (26 Oct–1 Nov)** | Live graph view on the timeline | `incidents` memory + learned e_a; B13–B16 |

| Role | Extra responsibility |
|---|---|
| **P2 · Detection** | City graph (builder, live updates, cascade, exposure) |
| **P3 · Reflex & resources** | Graph-based cost and candidate actuators in the assignment |
| **P5 · LLM tools & safety** | Vector DB, embeddings, context pack, memory-write rules, attack-pattern check |
| **P7 · Mocks & demo** | Live graph view on the timeline; mock Twin publishes graph metadata |

**If time runs short, cut in this order:** learned e_a → incident memory → playbooks. **Keep the graph**: it improves the math model directly and costs little.
