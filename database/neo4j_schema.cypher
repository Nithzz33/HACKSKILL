CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT case_fir IF NOT EXISTS FOR (c:Case) REQUIRE c.fir_number IS UNIQUE;
CREATE CONSTRAINT district_name IF NOT EXISTS FOR (d:District) REQUIRE d.name IS UNIQUE;

// Canonical graph pattern used by /analytics/network local projection:
// (:Person {name})-[:NAMED_IN_CASE]->(:Case {fir_number})-[:REPORTED_IN]->(:District {name})

// Example query for future Neo4j adapter:
// MATCH (p:Person)-[:NAMED_IN_CASE]->(c:Case)-[:REPORTED_IN]->(d:District)
// RETURN p.name AS suspect, collect(c.fir_number) AS cases, collect(DISTINCT d.name) AS districts
// ORDER BY size(cases) DESC;
