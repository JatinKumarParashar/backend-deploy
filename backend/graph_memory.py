import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

try:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
except Exception as e:
    driver = None
    print(f"Neo4j Connection Notice: {e}")

# 4 parameters: user_id, source, relation, target
def add_graph_relation(user_id: str, source: str, relation: str, target: str):
    if not driver:
        return True
    try:
        with driver.session() as session:
            # Knowledge Graph: (Source)-[RELATION]->(Target) linked with User
            query = f"""
            MERGE (u:User {{id: $user_id}})
            MERGE (s:Entity {{name: $source}})
            MERGE (t:Entity {{name: $target}})
            MERGE (s)-[:{relation}]->(t)
            MERGE (u)-[:INTERESTED_IN]->(s)
            """
            session.run(query, user_id=user_id, source=source, target=target)
        return True
    except Exception as e:
        print(f"Graph insert notice: {e}")
        return False

def get_graph_context(user_id: str):
    if not driver:
        return []
    try:
        with driver.session() as session:
            query = """
            MATCH (u:User {id: $user_id})-[:INTERESTED_IN]->(s:Entity)-[r]->(t:Entity)
            RETURN s.name AS source, type(r) AS relation, t.name AS target
            """
            results = session.run(query, user_id=user_id)
            return [f"{r['source']} -[{r['relation']}]-> {r['target']}" for r in results]
    except Exception as e:
        print(f"Graph fetch notice: {e}")
        return []