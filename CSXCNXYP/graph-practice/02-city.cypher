// Step 2: the static city map, as it would arrive on brain/internal/meta (concepts 1, 3, 7).
// UNWIND + MERGE loads a list in one query and can be re-run without making duplicates.
// This practice city is invented; the real one comes from the Twin's city description.

UNWIND [
  {id:'Z1', name:'Port'},        {id:'Z2', name:'Old Town'},
  {id:'Z3', name:'Industrial'},  {id:'Z4', name:'Residential'},
  {id:'Z5', name:'Hospital'}
] AS row
MERGE (z:Zone {id: row.id}) SET z.name = row.name;

// NEXT_TO is stored once per pair and queried without an arrow: (a)-[:NEXT_TO]-(b).
UNWIND [['Z1','Z2'], ['Z2','Z3'], ['Z2','Z4'], ['Z4','Z5'], ['Z3','Z5']] AS pair
MATCH (a:Zone {id: pair[0]}), (b:Zone {id: pair[1]})
MERGE (a)-[:NEXT_TO]-(b);

UNWIND [
  {id:'W1', type:'water_level',   zone:'Z1'}, {id:'W2', type:'water_level',   zone:'Z2'},
  {id:'T1', type:'traffic_speed', zone:'Z2'}, {id:'T2', type:'traffic_speed', zone:'Z4'},
  {id:'A1', type:'air_quality',   zone:'Z3'}, {id:'P1', type:'power_load',    zone:'Z3'}
] AS row
MATCH (z:Zone {id: row.zone})
MERGE (s:Sensor {id: row.id})
SET s.type = row.type, s.trust = 1.0, s.quarantined = false
MERGE (s)-[:IN]->(z);

UNWIND [
  {id:'PUMP1',   type:'pump',          zones:['Z1']},
  {id:'GATE1',   type:'flood_gate',    zones:['Z1','Z2']},
  {id:'TL1',     type:'traffic_light', zones:['Z2']},
  {id:'BRK1',    type:'breaker',       zones:['Z3']}
] AS row
MERGE (a:Actuator {id: row.id})
SET a.type = row.type, a.state = 'idle', a.quarantined = false
WITH a, row
UNWIND row.zones AS zid
MATCH (z:Zone {id: zid})
MERGE (a)-[:CONTROLS]->(z);

UNWIND [
  {id:'FIRE1', type:'fire_truck', zone:'Z3'},
  {id:'AMB1',  type:'ambulance',  zone:'Z5'},
  {id:'POL1',  type:'police',     zone:'Z4'}
] AS row
MATCH (z:Zone {id: row.zone})
MERGE (u:Unit {id: row.id})
SET u.type = row.type, u.available = true
MERGE (u)-[:BASED_IN]->(z);
