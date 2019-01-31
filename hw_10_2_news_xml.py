import xml.etree.ElementTree as ET

tree = ET.parse("newsafr.xml")
root = tree.getroot()
xml_items = root.findall("channel/item/description")
words = []
for xmli in xml_items:
    words.append(xmli.text.lower().split())

words_len = (list(filter(lambda x: len(x) > 6, sum(words, []))))
print(*sorted(set(words_len), key=lambda word: (-words_len.count(word), word))[:10], sep='\n')
