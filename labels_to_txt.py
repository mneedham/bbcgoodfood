from neo4j.v1 import GraphDatabase, basic_auth
import csv

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

tokenized_ingredients_query = """\
MATCH (ingredient:Ingredient {labelling_done: true})
RETURN ingredient.value AS ingredient, apoc.coll.sortNodes([(ingredient)-[:HAS_TOKEN]->(token) | token], "index") AS tokens
"""

with driver.session() as session, open("/tmp/data.txt", "w") as file:
    writer = csv.writer(file, delimiter=" ")
    result = session.run(tokenized_ingredients_query)

    for row in result:
        for token in row["tokens"]:
            writer.writerow([token["value"], token["label"]])

        writer.writerow([])
