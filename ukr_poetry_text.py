import requests
import json
import re

from bs4 import BeautifulSoup


def get_page_content(link: str) -> None:
    r = requests.get(f'http://poetyka.uazone.net/{link}')
    with open('poetry_page.html', 'w', encoding='utf-8') as output_file:
        output_file.write(r.text)


def read_poetry_db() -> dict:
    with open('poetry_db.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


def save_poetry_page(poetry_title: str) -> None:
    poetry_dict = read_poetry_db()

    for title, links in poetry_dict.items():
        if title.lower() == poetry_title.lower():
            if get_page_content(links[-1]) is None:
                get_page_content(links[0] + links[-1])


def clear_string(poetry_text: str) -> str:
    poetry_string_repr = ''
    for character in poetry_text:
        if re.search('[а-яА-ЯїЇіІєЄґҐ]', character) or character == ' ':
            poetry_string_repr += character
        elif character == '\n':
            poetry_string_repr += ' '
    print(poetry_text)
    return poetry_string_repr


def find_poetry_text() -> str:
    html_doc = 'poetry_page.html'
    soup = BeautifulSoup(open(html_doc, encoding='utf-8'), 'html.parser')
    # print(soup.prettify())

    poetry_text = soup.find_all('p')[1:-1][1].get_text()
    poetry_ending = poetry_text.find('*')
    return clear_string(poetry_text[:poetry_ending])


def main(poetry_title: str) -> str:
    save_poetry_page(poetry_title)
    return find_poetry_text()


print(main('Світи мені, Дніпре!'))
