"""
Module to get the poetry text by its title,
using poetpy - Python wrapper of the PoetryDB API.
"""
from poetpy import get_poetry
import re


def to_string(poetry_text: str) -> str:
    """Clear the poetry text from any non-alphabetic characters."""
    poetry_string_repr = ''
    for character in poetry_text:

        if re.search('[a-zA-Z]', character) or character == ' ':
            poetry_string_repr += character

        elif character == '\n':
            poetry_string_repr += ' '

    return poetry_string_repr.lower()


def get_poetry_text(poetry_title: str) -> str:
    """
    Find and return poetry text as a string.
    Return None if no poetry is found.
    """
    poetry_data = get_poetry('title', poetry_title)
    for poetry in poetry_data:

        try:
            if poetry['title'].lower() == poetry_title.lower():
                return to_string('\n'.join(poetry['lines']))
        except TypeError:
            return None


# print(get_poetry_text('A dream'))