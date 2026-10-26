# Graph DB practice: our schema on a small city

A learning sandbox for person B (`brain/src/graph/`). It uses **our real schema** from `team-docs/02-graph.md` section 5 on an invented 5-zone city, with one Storm-night flood chain. It isn't the production code; once you understand it, port it to `brain/src/graph/`.

| File | What it teaches |
|---|---|
| `01-schema.cypher` | Constraints and indexes (fast lookups, no duplicate ids), and the shared `:Event` label |
| `02-city.cypher` | Loading the city map with `UNWIND` + `MERGE` (re-runnable, no duplicates) |
| `03-storm-night.cypher` | Storing events and linking them: reading → verdict → incident → decision → action → ack. It also covers a nearby slowdown and a quarantined sensor |
| `04-endpoints.cypher` | The 4 Context API queries: `/context`, `/zone`, `/actuators`, `/chain` |
| `run.py` | The Python driver: load everything, run the queries, print JSON size and time |

## Run it

```bash
cd ~/Desktop/TSYP/CSXCNXYP/graph-practice
export NEO4J_PASSWORD='your-password'      # same as in the Neo4j Browser login
.venv/bin/python run.py load                # empties the DB, then loads schema + city + chain
.venv/bin/python run.py query               # the 4 endpoints with default parameters
.venv/bin/python run.py query zone zone_id=Z3
.venv/bin/python run.py query chain correlation_id=corr-0003
```

`load` and `reset` delete everything in the database. They refuse to run if the database contains any label not used by this practice set, so other data is safe.

Tested on Neo4j Community 2026.10 (the version in your Docker container). Results:

| Endpoint | Time | Size |
|---|---|---|
| `/context` | 15 ms | 819 characters |
| `/zone` | 9 ms | 339 characters |
| `/actuators` | 8 ms | 164 characters |
| `/chain` | 10 ms | 629 characters |

The spec's targets are < 100 ms and < 1,500 characters.

## Look at it in Neo4j Browser

Open http://localhost:7474 and try these:

```cypher
// the whole graph (small enough to see)
MATCH (n) RETURN n

// only the city map
MATCH p=(:Zone)-[:NEXT_TO]-(:Zone) RETURN p
MATCH p=(x)-[:IN|CONTROLS|BASED_IN]->(:Zone) RETURN p

// the flood chain
MATCH p=(e:Event {correlation_id:'corr-0001'})-[*1..2]-() RETURN p

// zones within 2 hops of the Port
MATCH (z:Zone {id:'Z1'})-[:NEXT_TO*1..2]-(n) RETURN DISTINCT n.id, n.name

// is the index used? (look for NodeIndexSeek, not AllNodesScan)
PROFILE MATCH (e:Event {correlation_id:'corr-0001'}) RETURN e
```

## Exercises (in the order of the learning plan)

1. **Model:** draw the graph from `MATCH (n) RETURN n` on paper. Which nodes are static (from `meta`) and which are events?
2. **Cypher:** write a query listing every sensor with its zone name, sorted by zone.
3. **MERGE:** paste the content of `02-city.cypher` into Neo4j Browser and run it twice, as if `meta` arrived twice. Check with `MATCH (n:Zone) RETURN count(n)` that there are still 5 zones. Then try `CREATE (:Zone {id:'Z1'})`: the uniqueness constraint refuses it. Without the constraint you would now have a duplicate.
4. **Index:** run the `PROFILE` query above, then `DROP INDEX event_corr` and profile again. Compare the "db hits", then recreate the index with `01-schema.cypher`.
5. **Traversal:** add a second incident (fire in Z3, evidence: a new air-quality reading from `A1`). Check that `/context` for INC1 does **not** show it (Z3 isn't next to Z1), but `/context` for the new incident shows the quarantined sensor P1.
6. **Model decision:** `/context` currently returns `null` fields (`"unit": null`). Make the JSON smaller by returning only the fields each kind has, since the LLM prompt must stay short.
7. **Time window:** R2 (traffic in Z2) appears in `/context` because it's within 15 min. Change its timestamp to 20 min before the incident and check that it disappears.
8. **Python:** in `run.py`, replace `session.run` writes with `session.execute_write(...)`, the pattern to use for each MQTT message (one message = one transaction, retried automatically).
9. **Growth:** write a query that deletes `Reading` nodes older than 30 min that aren't `EVIDENCE` of any incident (the spec's "don't store every normal reading").

## Choices made here (to confirm with the team)

- `Call` gets an `IN` link to its zone. The spec doesn't list one, but `/context` needs it to find calls in neighbouring zones.
- Every event also has the label `:Event`, so one index on `correlation_id` serves `/chain`.
- Timestamps are epoch milliseconds, matching the MQTT `timestamp` field.
- `Action` stores `actuator_id` as a property; a `TARGETS` link to the `Actuator` would also work.
- Sensor `latest_value` / `latest_ts` live on the Sensor node, so normal readings never become nodes.
