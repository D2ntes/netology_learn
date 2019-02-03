import codecs
import json


def read_json(filename):
    json_content = ""
    try:
        with codecs.open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            json_content = json.loads(content)
            # pprint(json_content)
    except Exception as e:
        print("Ошибка чтения json: {}".format(str(e)))
    return json_content


def write_json_win1251(filename, json_data):
    with open(filename, "w", encoding='utf-8') as f:
        try:
            f.write(json.dumps(json_data, indent=2, ensure_ascii=False))
        except Exception as e:
            log_text = "ошибка записи в файл: {}".format(filename, str(e))
            print(log_text)


okved_dict = dict()
okved_key = ''
okved_value = dict()
json_dict = read_json('zchb_org_from_inn_p2_win1251.json')

for id_company in json_dict['data']:
    okved_key =(json_dict['data'][id_company]["КодОКВЭД"], json_dict['data'][id_company]["НаимОКВЭД"])
    okved_dict.setdefault(okved_key, list())
    for dop_okved in json_dict['data'][id_company]["СвОКВЭДДоп"]:
        okved_value = {dop_okved['КодОКВЭД']: dop_okved['НаимОКВЭД']}
        okved_dict[okved_key].append(okved_value)

write_json_win1251('rezult_okved.json', okved_dict)

# with open('rezult_okved_win1251.json', 'w', encoding='UTF-8') as file:
#     json.dump(str(okved_dict), file, indent=2, ensure_ascii=False)
