from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

with driver.session() as session:
    session.run("""\
    CREATE INDEX ON :Recipe(uri)
    """)

    session.run("""\
    CREATE CONSTRAINT ON (r:Recipe)
    ASSERT r.id IS UNIQUE
    """)

    session.run("""\
    CREATE CONSTRAINT ON (i:Ingredient)
    ASSERT i.id IS UNIQUE
    """)
