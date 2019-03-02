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


class UrlFromWiki:
    def __init__(self, countries_names):
        self.prefix_url = 'https://en.wikipedia.org/wiki/'
        self.countries_names = countries_names
        self.index = 0
        self.len = len(countries_names)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(countries_names) - 1:
            raise StopIteration
        self.index += 1
        return str(f"{self.countries_names[self.index][1]} - "
                   f"{self.prefix_url}{urllib.parse.quote(self.countries_names[self.index][0])}")


if __name__ == '__main__':
    countries_names = from_json()
    names = UrlFromWiki(countries_names)
    for pair in names:
        print(pair)
