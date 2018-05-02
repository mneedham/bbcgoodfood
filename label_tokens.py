from flask import Flask, render_template, request, url_for, redirect
from neo4j.v1 import GraphDatabase, basic_auth
import re

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

app = Flask(__name__)

ingredients_to_label_query = """\
MATCH (ingredient:Ingredient)
WHERE not(exists(ingredient.labelling_done))
RETURN ingredient, apoc.coll.sortNodes([(ingredient)-[:HAS_TOKEN]->(token) | token], "index") AS tokens
ORDER BY rand()
LIMIT 10
"""


@app.route("/")
def home():
    with driver.session() as session:
        result = session.run(ingredients_to_label_query)
        ingredients = [{"ingredientId": row["ingredient"]["id"],
                        "value": row["ingredient"]["value"],
                        "tokens": [token.properties for token in row["tokens"]]}
                       for row in result]
    return render_template("index.html", ingredients=ingredients)


def extract_label_keys(form):
    keys = [field for field in form if field.startswith("label_")]
    sorted_keys = sorted([(re.match("label_(\d{1,2})", label).groups()[0], label) for label in keys],
                         key=lambda tup: tup[0])
    return [key for index, key in sorted_keys]


label_tokens_query = """\
MATCH (ingredient:Ingredient {id: {id}})
SET ingredient.labelling_done = true
WITH ingredient
MATCH (ingredient)-[:HAS_TOKEN]->(token)
SET token.label = {labels}[token.index]
"""


@app.route("/ingredient/<ingredient_id>", methods=["POST"])
def post_ingredient(ingredient_id):
    label_keys = extract_label_keys(request.form)

    labels = [request.form[key] for key in label_keys]
    print(ingredient_id, labels)

    with driver.session() as session:
        session.run(label_tokens_query, {"labels": labels, "id": ingredient_id})

    return redirect(url_for('home'))
