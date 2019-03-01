import xml.etree.ElementTree as ET
import json


def word_max_count_10(words):
    words_len = (list(filter(lambda x: len(x) > 6, words)))
    return sorted(set(words_len), key=lambda word: (-words_len.count(word), word))[:10]

def words_from_xml(file="newsafr.xml"):
    tree = ET.parse(file)
    root = tree.getroot()
    xml_items = root.findall("./channel/item/description")
    words = []
    for xmli in xml_items:
        words.append(xmli.text.lower().split())
    return sum(words, [])

def words_from_json(file="newsafr.json"):
    with open(file, encoding='utf-8') as datafile:
        json_data = json.load(datafile)

    words = []
    for description in json_data["rss"]["channel"]["items"]:
        words.append(description['description'].lower().split())
    return sum(words, [])


print('Данные из xml-файла:',*word_max_count_10(words_from_xml()), sep='\n')
print('Данные из json-файла:',*word_max_count_10(words_from_json()), sep='\n')

