import requests


URL = 'https://itunes.apple.com/search'

params = {'term': 'Владимирский централ'}

resp = requests.get(URL, params=params)
resp_json = resp.json()

for item in resp_json['results']:
    name = f'{item["artistName"]}: {item["trackName"]}.jpg'
    cover_url = item["artworkUrl100"]

    cover_resp = requests.get(cover_url)
    with open(f'covers/{name}', 'wb') as f:
        print(f'Запись {name} в файл')
        f.write(cover_resp.content)
