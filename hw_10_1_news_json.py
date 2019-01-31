import json

# def

with open("newsafr.json", encoding='utf-8') as datafile:
    json_data = json.load(datafile)
words = []
for description in json_data["rss"]["channel"]["items"]:
    words.append(description['description'].lower().split())

words_len = (list(filter(lambda x: len(x) > 6, sum(words, []))))

d = {}
for word in set(words_len):
    d.setdefault(word, words_len.count(word))

l = sorted(d, key=lambda word: (d[word], not word), reverse=True)
print(*l[:10], sep='\n')

# for key in l[:10]:
#      print(key, d[key])
