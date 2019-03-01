import json

with open("newsafr.json", encoding='utf-8') as datafile:
    json_data = json.load(datafile)

words = []
for description in json_data["rss"]["channel"]["items"]:
    words.append(description['description'].lower().split())

words_len = (list(filter(lambda x: len(x) > 6, sum(words, []))))

count_words = {}
for word in set(words_len):
    count_words.setdefault(word, words_len.count(word))

words_len_sort = sorted(count_words, key=lambda word: count_words[word], reverse=True)
print(*words_len_sort[:10], sep='\n')

# for key in words_len_sort[:10]:
#      print(key, count_words[key])
