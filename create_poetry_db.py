import json
import re

import requests

start_page = "a.html#%D0%9C"
poetry_page = "http://poetyka.uazone.net/"
page = requests.get(f"{poetry_page}{start_page}")
authors_links_pattern = re.compile(r"(?<=href=\")[^#]+?(?=\")")
authors_links = re.findall(authors_links_pattern, page.text)

poem_link_dict = {}

for idx, author_link in enumerate(authors_links):
    page = requests.get(f"{poetry_page}{author_link}")
    poem_link_and_name_pattern = re.compile(r"href=\"(.+)\">(.+)</a><br>")
    for poem_link, name in re.findall(poem_link_and_name_pattern, page.text):
        poem_link_dict[name] = author_link, poem_link
    percentage = (idx + 1) / len(authors_links) * 100
    print(percentage)

with open("poetry_db.json", "w", encoding="utf-8") as file:
    json.dump(poem_link_dict, file, indent=4, ensure_ascii=False)
