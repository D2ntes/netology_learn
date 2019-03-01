import requests


URL = 'https://translate.yandex.net/api/v1' \
      '/tr.json/translate'


resp = requests.get(URL)

params = {
    'lang': 'ru-en', 
    'srv': 'tr-text', 
    'id': 'f5c948f1.5c59b9e9.16d39b90-6-0'
}

data = {'text': 'Привет мир!'}

resp = requests.post(URL, 
    data=data, 
    params=params
)

# получить код ответа
print(resp.status_code)

# получить байтовое представление ответа
print(resp.content)

# получить json данные ответа 
# (только если ответ в формате JSON)
print(resp.json())

