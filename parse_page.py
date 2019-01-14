import re
import demjson
from bs4 import BeautifulSoup

file = open("data/raw/2852672.html").read()
soup = BeautifulSoup(file, 'html.parser')
ingredients_cell = [entry for entry in soup.find_all("script") if "ingredients" in entry.text][0]
blah = re.findall("permutive.addon\(\"web\",(.*)\);", ingredients_cell.text.strip())
print(demjson.decode(blah[0])["page"]["recipe"]["ingredients"])
