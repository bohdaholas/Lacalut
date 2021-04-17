import re
import requests
import json


def read_poetry_db() -> dict:
    with open('poetry_db.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def find_poetry_text(poetry_title: str):
    poetry_data = read_poetry_db()
    link = poetry_data[poetry_title][1:]

    full_name = re.search('.*/', link)[0][0:-1]
    surname = re.search('[a-z]*', full_name)[0]
    title = re.search('/.*', link)[0][1:]
    full_text = requests.get(f'http://ukrlit.org/faily/avtor/{full_name}/{surname}-{title}.txt').text

    poetry_ending = 'Постійна адреса: '
    beginning = full_text.find(poetry_title)
    ending = full_text.find(poetry_ending)
    full_text = full_text[beginning + len(poetry_title) : ending]
    try:
        odd_char_1 = re.search('\([0-9]*\)', full_text)[0]
    except TypeError:
        odd_char_1 = ''
    
    try:
        odd_char_2 = re.search('\[[0-9]*.*\s?.*\]', full_text)[0]
    except TypeError:
        odd_char_2 = ''

    return full_text.replace(odd_char_1, '').replace(odd_char_2, '').replace('*', '').strip()

# print(find_poetry_text('Доля'))