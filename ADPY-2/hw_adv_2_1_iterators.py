# -*- coding: utf-8 -*-

# Домашнее задание к лекции 1.2 «Iterators. Generators. Yield»
# Написать класс итератора, который по каждой стране из файла countries.json ищет страницу из википедии.
# Записывает в файл пару: страна – ссылка.

import json
import urllib.parse


def from_json(file="countries.json"):
    with open(file) as datafile:
        json_data = json.load(datafile)
    countries = []
    for country in json_data:
        countries.append((country['name']['common'], country['name']['official']))
    return countries


def save_to_file(data, file="url_wiki_countries.txt"):
    with open(file, 'w', encoding='utf-8') as datafile:
        datafile.write(f'{data}')


class UrlWiki:
    def __init__(self, countries_names):
        self.prefix_url = 'https://en.wikipedia.org/wiki/'
        self.countries_names = countries_names
        self.index = 0
        self.len = len(countries_names)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.countries_names) - 1:
            raise StopIteration
        self.index += 1
        return str(f"{self.countries_names[self.index][1]} - "
                   f"{self.prefix_url}{urllib.parse.quote(self.countries_names[self.index][0])}")

    def __str__(self):
        countries_urls = []
        for pair in self:
            countries_urls.append(pair)
        return '\n'.join(countries_urls)


if __name__ == '__main__':
    save_to_file(
        UrlWiki(
            from_json()
        )
    )
