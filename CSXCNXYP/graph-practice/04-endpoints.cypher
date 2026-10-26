// Step 4: the four Context API queries from 02-graph.md section 5.2 (concepts 2, 5).
// Each one returns ready-made JSON in a single round trip. $params come from the URL.
// run.py splits this file on the "// name:" lines.

// name: context
// GET /context/{incident_id}: incident, evidence, events in the same + neighbouring zones
// in the last 15 min, actuators and units, quarantined devices.
MATCH (i:Incident {id: $incident_id})-[:IN]->(z:Zone)
WITH i, z, [z] + COLLECT { MATCH (z)-[:NEXT_TO]-(n:Zone) RETURN n } AS zones
WITH i, z, zones, i.timestamp - 900000 AS since
RETURN
  i {.id, .type, .status, .confidence, .severity, .verified, .timestamp, zone: z.id} AS incident,
  COLLECT { MATCH (i)-[:EVIDENCE]->(e)
            RETURN e {.id, kind: [x IN labels(e) WHERE x <> 'Event'][0], .value, .unit, .text, .timestamp} } AS evidence,
  COLLECT { UNWIND zones AS zz
            MATCH (zz)<-[:IN]-(s:Sensor)<-[:FROM]-(r:Reading)
            WHERE r.timestamp >= since AND NOT (i)-[:EVIDENCE]->(r)
            RETURN r {.id, zone: zz.id, sensor: s.id, sensor_type: s.type, .value, .unit, .timestamp} } AS related_readings,
  COLLECT { UNWIND zones AS zz
            MATCH (zz)<-[:IN]-(c:Call)
            WHERE c.timestamp >= since AND NOT (i)-[:EVIDENCE]->(c)
            RETURN c {.id, zone: zz.id, .text, .timestamp} } AS related_calls,
  COLLECT { UNWIND zones AS zz
            MATCH (zz)<-[:IN]-(o:Incident)
            WHERE o <> i AND o.timestamp >= since
            RETURN o {.id, zone: zz.id, .type, .status} } AS related_incidents,
  COLLECT { UNWIND zones AS zz
            MATCH (a:Actuator)-[:CONTROLS]->(zz)
            RETURN DISTINCT a {.id, .type, .state, .quarantined} } AS actuators,
  COLLECT { UNWIND zones AS zz
            MATCH (u:Unit)-[:BASED_IN]->(zz)
            RETURN u {.id, .type, .available, zone: zz.id} } AS units,
  COLLECT { UNWIND zones AS zz
            MATCH (d)-[:IN|CONTROLS]->(zz)
            WHERE (d:Sensor OR d:Actuator) AND d.quarantined
            RETURN DISTINCT d.id } AS quarantined;

// name: zone
// GET /zone/{zone_id}: neighbours, sensors with latest value and trust, actuators, units.
MATCH (z:Zone {id: $zone_id})
RETURN z {
  .id, .name,
  neighbours: COLLECT { MATCH (z)-[:NEXT_TO]-(n:Zone) RETURN n.id },
  sensors:    COLLECT { MATCH (s:Sensor)-[:IN]->(z)
                        RETURN s {.id, .type, .latest_value, .latest_ts, .trust, .quarantined} },
  actuators:  COLLECT { MATCH (a:Actuator)-[:CONTROLS]->(z) RETURN a {.id, .type, .state, .quarantined} },
  units:      COLLECT { MATCH (u:Unit)-[:BASED_IN]->(z) RETURN u {.id, .type, .available} }
} AS zone;

// name: actuators
// GET /actuators?zone_id=...
MATCH (a:Actuator)-[:CONTROLS]->(:Zone {id: $zone_id})
RETURN a {.id, .type, .state, .quarantined} AS actuator
ORDER BY a.id;

// name: chain
// GET /chain/{correlation_id}: reading -> verdict -> incident -> decision -> action -> ack.
// Every event carries correlation_id and the :Event label, so one indexed lookup finds them all.
MATCH (e:Event {correlation_id: $correlation_id})
RETURN e {.id, kind: [x IN labels(e) WHERE x <> 'Event'][0], .timestamp,
          links: COLLECT { MATCH (e)-[l]->(t) RETURN type(l) + ' ' + t.id }} AS event
ORDER BY e.timestamp;
