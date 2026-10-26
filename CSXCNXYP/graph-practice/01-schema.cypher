// Step 1: constraints and indexes (concept 4).
// A uniqueness constraint also creates an index, so lookups by id are fast.

CREATE CONSTRAINT zone_id     IF NOT EXISTS FOR (n:Zone)     REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT sensor_id   IF NOT EXISTS FOR (n:Sensor)   REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT actuator_id IF NOT EXISTS FOR (n:Actuator) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT unit_id     IF NOT EXISTS FOR (n:Unit)     REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT reading_id  IF NOT EXISTS FOR (n:Reading)  REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT call_id     IF NOT EXISTS FOR (n:Call)     REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT verdict_id  IF NOT EXISTS FOR (n:Verdict)  REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT decision_id IF NOT EXISTS FOR (n:Decision) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT action_id   IF NOT EXISTS FOR (n:Action)   REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT ack_id      IF NOT EXISTS FOR (n:Ack)      REQUIRE n.id IS UNIQUE;

// Every event node also gets the shared label :Event (a node can have several labels).
// /chain looks events up by correlation_id and /context filters them by time,
// so one index on :Event covers all seven event types.
CREATE INDEX event_corr IF NOT EXISTS FOR (n:Event) ON (n.correlation_id);
CREATE INDEX event_time IF NOT EXISTS FOR (n:Event) ON (n.timestamp);
