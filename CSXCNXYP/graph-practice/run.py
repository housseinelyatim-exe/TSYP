"""Load the practice city into Neo4j and call the four Context API queries.

Usage:
    export NEO4J_PASSWORD=...            # your Neo4j password (never written in a file)
    .venv/bin/python run.py load         # wipe, then schema + city + Storm-night chain
    .venv/bin/python run.py query        # run the 4 endpoint queries, print JSON, size and time
    .venv/bin/python run.py query context incident_id=INC1
    .venv/bin/python run.py reset        # delete everything

Optional: NEO4J_URI (default bolt://localhost:7687), NEO4J_USER (default neo4j).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

from neo4j import GraphDatabase

HERE = Path(__file__).resolve().parent
DEFAULT_PARAMS = {
    "context": {"incident_id": "INC1"},
    "zone": {"zone_id": "Z1"},
    "actuators": {"zone_id": "Z1"},
    "chain": {"correlation_id": "corr-0001"},
}


def statements(path: Path) -> list[str]:
    """Split a .cypher file on ';' at line ends, dropping // comments."""
    text = "\n".join(l for l in path.read_text().splitlines() if not l.strip().startswith("//"))
    return [s.strip() for s in re.split(r";\s*\n", text + "\n") if s.strip()]


def endpoint_queries() -> dict[str, str]:
    """Read 04-endpoints.cypher into {name: query}."""
    parts = re.split(r"^// name: (\w+)\s*$", (HERE / "04-endpoints.cypher").read_text(), flags=re.M)
    return {name: statements_from(body) for name, body in zip(parts[1::2], parts[2::2])}


def statements_from(body: str) -> str:
    lines = [l for l in body.splitlines() if not l.strip().startswith("//")]
    return "\n".join(lines).strip().rstrip(";")


PRACTICE_LABELS = {"Zone", "Sensor", "Actuator", "Unit", "Reading", "Call", "Verdict",
                   "Incident", "Decision", "Action", "Ack", "Event"}


def wipe(s) -> None:
    """Empty the database, but refuse if it holds anything that isn't practice data."""
    other = s.run("MATCH (n) UNWIND labels(n) AS l WITH DISTINCT l "
                  "WHERE NOT l IN $known RETURN collect(l) AS other",
                  known=list(PRACTICE_LABELS)).single()["other"]
    if other:
        sys.exit(f"Database has non-practice data (labels {other}); not wiping it. "
                 "Use an empty database instead.")
    s.run("MATCH (n) DETACH DELETE n").consume()


def load(driver) -> None:
    with driver.session() as s:
        wipe(s)
        for f in ("01-schema.cypher", "02-city.cypher", "03-storm-night.cypher"):
            for q in statements(HERE / f):
                s.run(q).consume()
            print(f"loaded {f}")
        counts = s.run("MATCH (n) RETURN labels(n) AS l, count(*) AS c ORDER BY c DESC").data()
        print("nodes:", {"/".join(r["l"]): r["c"] for r in counts})


def query(driver, names: list[str], params: dict[str, str]) -> None:
    queries = endpoint_queries()
    for name in names:
        p = params or DEFAULT_PARAMS[name]
        with driver.session() as s:
            s.run(queries[name], p).consume()  # warm-up, as in a long-running service
            t0 = time.perf_counter()
            rows = s.run(queries[name], p).data()
            ms = (time.perf_counter() - t0) * 1000
        out = json.dumps(rows if len(rows) != 1 else rows[0], separators=(",", ":"), default=str)
        print(f"\n== {name} {p}  ->  {ms:.1f} ms, {len(out)} characters")
        print(json.dumps(json.loads(out), indent=2, ensure_ascii=False))


def main() -> None:
    if "NEO4J_PASSWORD" not in os.environ:
        sys.exit("Set NEO4J_PASSWORD first (export NEO4J_PASSWORD=...)")
    driver = GraphDatabase.driver(
        os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        auth=(os.environ.get("NEO4J_USER", "neo4j"), os.environ["NEO4J_PASSWORD"]),
    )
    driver.verify_connectivity()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "query"
    if cmd == "load":
        load(driver)
    elif cmd == "reset":
        with driver.session() as s:
            wipe(s)
        print("database emptied")
    elif cmd == "query":
        names = [a for a in sys.argv[2:] if "=" not in a] or list(DEFAULT_PARAMS)
        params = dict(a.split("=", 1) for a in sys.argv[2:] if "=" in a)
        query(driver, names, params)
    else:
        sys.exit(__doc__)
    driver.close()


if __name__ == "__main__":
    main()
