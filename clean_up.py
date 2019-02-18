import re
import json
from bs4 import BeautifulSoup
import glob
import html
import ast

with open("stream_all.json", "r") as json_file, open("stream_clean.json", "w") as clean_json_file:
    line = json_file.readline()
    while line:
        line = ast.literal_eval(line)
        line["page"]["title"] = html.unescape(line["page"]["title"])
        line["page"]["article"]["description"] = html.unescape(line["page"]["article"]["description"])
        print(json.dumps(line), file=clean_json_file)
        line = json_file.readline()

    # for file_path in glob.glob("lju_recipes/*.html"):
    #     with open(file_path) as file:
    #         soup = BeautifulSoup(file.read(), 'html.parser')
    #         ingredients_cell = [entry for entry in soup.find_all("script") if "ingredients" in entry.text][0]
    #         js_object = re.findall("permutive.addon\(\"web\",(.*)\);", ingredients_cell.text.strip())
    #         if len(js_object) > 0:
    #             try:
    #                 print(demjson.decode(js_object[0]), file=json_file)
    #             except demjson.JSONDecodeError as error:
    #                 print(error, js_object)
