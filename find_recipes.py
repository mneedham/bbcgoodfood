import hashlib
import sys

import requests
from bs4 import BeautifulSoup
from neo4j.v1 import GraphDatabase, basic_auth


def find_recipes(search_uri):
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1'
    headers = {'user-agent': agent}
    r = requests.get(search_uri, headers=headers)
    return r.text


def generate_search_uri(page):
    return "https://www.bbcgoodfood.com/search/recipes?query=&page={0}".format(page)


driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

page = 0

while True:
    search_uri = generate_search_uri(page)
    print(search_uri)
    response = find_recipes(search_uri)

    soup = BeautifulSoup(response, 'html.parser')

    batch = []

    recipes = soup.select("div#search-results article")
    for recipe_container in recipes:
        recipe_link = recipe_container.select("h3 a")[0]
        title = recipe_link.text.strip()
        uri = "https://www.bbcgoodfood.com{}".format(recipe_link["href"])
        batch.append((title, uri))

    print(batch)
    with driver.session() as session:
        session.run("""\
        UNWIND {recipes} AS recipe
        MERGE (r:Recipe {id: recipe.id})
        ON CREATE SET r.uri = recipe.uri, r.title = recipe.title
        """, {
            "recipes": [{
                "id": hashlib.sha224(uri.encode("utf-8")).hexdigest(),
                "uri": uri,
                "title": title
            }
                for title, uri in batch]
        })

    if len(soup.select("li.pager-next a")) > 0:
        page += 1

    if page > 10:
        sys.exit(1)
