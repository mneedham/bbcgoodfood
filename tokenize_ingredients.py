import nltk
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

find_untokenized_ingredients_query = """\
MATCH (ingredient:Ingredient)
WHERE not((ingredient)-[:HAS_TOKEN]->())
RETURN ingredient
"""

create_tokens_query = """\
MATCH (ingredient:Ingredient {value: {value} })
UNWIND range(0, size({tokens})-1) AS sentenceIndex
CREATE (t:Token {value: {tokens}[sentenceIndex] })
SET t.index = sentenceIndex
CREATE (ingredient)-[:HAS_TOKEN]->(t)
"""

with driver.session() as session:
    result = session.run(find_untokenized_ingredients_query)

    for row in result:
        value = row["ingredient"]["value"]
        print("Processing: ", value)
        tokens = nltk.word_tokenize(value)
        session.run(create_tokens_query, {"value": value, "tokens": tokens})
