import requests
from neo4j.v1 import GraphDatabase, basic_auth


def download_file(url, id):
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1'
    headers = {'user-agent': agent}
    r = requests.get(url, stream=True, headers=headers)
    local_filename = "data/raw/{0}".format(id)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

with driver.session() as session:
    result = session.run("""\
    MATCH (recipe:Recipe) 
    WHERE not(exists(recipe.downloaded))
    RETURN recipe
    """)

    for row in result:
        uri = row["recipe"]["uri"]
        id = row["recipe"]["id"]
        print(download_file(uri, id))
        session.run("""\
        MATCH (recipe:Recipe {id: {id}})
        SET recipe.downloaded = true
        """, {"id": id})
