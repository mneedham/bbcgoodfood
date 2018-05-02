import nltk
from bs4 import BeautifulSoup
from neo4j.v1 import GraphDatabase, basic_auth
from nltk import word_tokenize

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

with driver.session() as session:
    result = session.run("""\
    MATCH (recipe:Recipe)
    WHERE not(exists(recipe.parsed))
    RETURN recipe.id AS id
    """)

    recipe_ids = [row["id"] for row in result]

    for recipe_id in recipe_ids:
        with open("data/raw/{0}".format(recipe_id)) as file:
            soup = BeautifulSoup(file, 'html.parser')
            categories = [item.get("content") for item in soup.select("meta") if
                          item.get("itemprop") == "recipeCategory"]
            ingredients = ["".join([element.string
                                    for element in (list(row.children))
                                    if element.string])
                           for row in soup.select("ul.ingredients-list__group li")]

            for ingredient in ingredients:
                print(ingredient)

                params = {
                    "id": recipe_id,
                    "ingredients": ingredients
                }

                session.run("""\
                MATCH (recipe:Recipe {id: {id} })
                UNWIND {ingredients} AS ingredient
                MERGE (i:Ingredient {id: apoc.util.md5([ingredient]) })
                SET i.value = ingredient
                MERGE (recipe)-[:HAS_INGREDIENT]->(i)
                SET recipe.parsed = true
                """, params)

                # print([(value, tag)
                #        for value, tag in nltk.pos_tag(word_tokenize(ingredient))
                #        if tag in ["NN", "NNS"] and value not in ["tsp", "tbsp"]])

            # title = soup.select("h1")[0].text
