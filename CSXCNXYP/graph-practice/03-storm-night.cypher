// Step 3: one Storm-night flood chain, as the events would arrive on MQTT (concepts 3, 5, 6).
// Times are relative to "now" (epoch ms) so the 15-minute window in /context works.
// In the real service each MQTT message is one small MERGE transaction like these.

// 1. Abnormal water reading in the Port + the Guardian verdict on it.
MATCH (s:Sensor {id:'W1'})
MERGE (r:Reading {id:'R1'})
SET r.correlation_id = 'corr-0001', r.sensor_id = 'W1', r.value = 0.92, r.unit = 'm',
    r.abnormal = true, r.timestamp = timestamp() - 600000
MERGE (r)-[:FROM]->(s)
SET s.latest_value = r.value, s.latest_ts = r.timestamp;

MATCH (r:Reading {id:'R1'})
MERGE (v:Verdict {id:'V1'})
SET v.correlation_id = 'corr-0001', v.trusted = true, v.trust = 0.94, v.timestamp = r.timestamp + 2000
MERGE (v)-[:ON]->(r);

// 2. A citizen call from the same zone (calls are linked to a zone so /context can find them).
MATCH (z:Zone {id:'Z1'})
MERGE (c:Call {id:'C1'})
SET c.correlation_id = 'corr-0001', c.text = 'Street flooding, water entering basements on Dock St',
    c.timestamp = timestamp() - 540000
MERGE (c)-[:IN]->(z);

// 3. Detection opens the incident with its evidence.
MATCH (z:Zone {id:'Z1'}), (r:Reading {id:'R1'}), (c:Call {id:'C1'})
MERGE (i:Incident {id:'INC1'})
SET i.correlation_id = 'corr-0001', i.type = 'flood', i.status = 'open', i.confidence = 0.88,
    i.severity = 3, i.verified = true, i.timestamp = timestamp() - 500000
MERGE (i)-[:IN]->(z)
MERGE (i)-[:EVIDENCE]->(r)
MERGE (i)-[:EVIDENCE]->(c);

// 4. Decision -> action -> ack.
MATCH (i:Incident {id:'INC1'})
MERGE (d:Decision {id:'D1'})
SET d.correlation_id = 'corr-0001', d.summary = 'Start pump, close flood gate, dispatch police',
    d.timestamp = i.timestamp + 30000
MERGE (d)-[:FOR]->(i);

MATCH (d:Decision {id:'D1'}), (a:Actuator {id:'PUMP1'})
MERGE (x:Action {id:'ACT1'})
SET x.correlation_id = 'corr-0001', x.command = 'start', x.actuator_id = 'PUMP1',
    x.timestamp = d.timestamp + 1000
MERGE (x)-[:EXECUTES]->(d)
SET a.state = 'running';

MATCH (x:Action {id:'ACT1'})
MERGE (k:Ack {id:'ACK1'})
SET k.correlation_id = 'corr-0001', k.ok = true, k.timestamp = x.timestamp + 1500
MERGE (k)-[:CONFIRMS]->(x);

// 5. Context around it: a traffic slowdown next door (Old Town), not yet an incident.
MATCH (s:Sensor {id:'T1'})
MERGE (r:Reading {id:'R2'})
SET r.correlation_id = 'corr-0002', r.sensor_id = 'T1', r.value = 14.0, r.unit = 'km/h',
    r.abnormal = true, r.timestamp = timestamp() - 300000
MERGE (r)-[:FROM]->(s)
SET s.latest_value = r.value, s.latest_ts = r.timestamp;

// 6. A rejected reading: the Guardian quarantines the power sensor (fake-reading case).
MATCH (s:Sensor {id:'P1'})
MERGE (r:Reading {id:'R3'})
SET r.correlation_id = 'corr-0003', r.sensor_id = 'P1', r.value = 2.4, r.unit = 'MW',
    r.abnormal = true, r.timestamp = timestamp() - 200000
MERGE (r)-[:FROM]->(s)
MERGE (v:Verdict {id:'V3'})
SET v.correlation_id = 'corr-0003', v.trusted = false, v.trust = 0.12, v.timestamp = r.timestamp + 2000
MERGE (v)-[:ON]->(r)
SET s.quarantined = true, s.trust = 0.12;

// 7. Shared :Event label on every event (in the real service, set it in each MERGE:
//    MERGE (r:Reading:Event {id: $id}) ...).
MATCH (e) WHERE e:Reading OR e:Call OR e:Verdict OR e:Incident OR e:Decision OR e:Action OR e:Ack
SET e:Event;
