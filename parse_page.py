import re
import demjson
from bs4 import BeautifulSoup
import glob

with open("stream_all.json", "w") as json_file:
    for file_path in glob.glob("lju_recipes/*.html"):
        with open(file_path) as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            ingredients_cell = [entry for entry in soup.find_all("script") if "ingredients" in entry.text][0]
            js_object = re.findall("permutive.addon\(\"web\",(.*)\);", ingredients_cell.text.strip())
            if len(js_object) > 0:
                try:
                    print(demjson.decode(js_object[0]), file=json_file)
                except demjson.JSONDecodeError as error:
                    print(error, js_object)
