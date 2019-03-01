import xml.etree.ElementTree as ET
import json


class WordMaxLen:
    def __init__(self, words_list):
        self.max_len = 6
        self.count = 10
        self.word_max = self.get_max_len(words_list)

    def get_max_len(self, words_list):
        words_len = (list(filter(lambda x: len(x) > self.max_len, words_list)))
        return sorted(set(words_len), key=lambda word: (-words_len.count(word), word))[:self.count]

    def __str__(self):
        return '\n'.join(self.word_max)


def words_from_xml(file="newsafr.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    xml_items = root.findall("./channel/item/description")
    words = []
    for description in xml_items:
        words.append(description.text.lower().split())
    return sum(words, [])


def words_from_json(file="newsafr.json"):
    with open(file, encoding='utf-8') as datafile:
        json_data = json.load(datafile)
    words = []
    for description in json_data["rss"]["channel"]["items"]:
        words.append(description['description'].lower().split())
    return sum(words, [])


if __name__ == '__main__':
    max_xml = WordMaxLen(words_from_xml())
    max_json = WordMaxLen(words_from_json())
    print(f'Данные из xml-файла:\n{max_xml}')
    print(f'Данные из json-файла:\n{max_json}')
