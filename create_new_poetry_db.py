import json
import re
import requests

poetry_page = "http://ukrlit.org/tvory/poeziia_poemy_virshi/virshi"
page = requests.get(f"{poetry_page}")
poem_name_link_pattern = re.compile(r'<li><a href="(\S+?)" title="\S+?">(.+?)</a>.+?</li>')

matches = re.findall(poem_name_link_pattern, requests.get(poetry_page).text)

poem_name_link_dict = {}
for poem_link, poem_name in matches:
    poem_name_link_dict[poem_name] = poem_link

with open("poetry_db.json", "w", encoding="utf-8") as file:
    json.dump(poem_name_link_dict, file, indent=4, ensure_ascii=False)
