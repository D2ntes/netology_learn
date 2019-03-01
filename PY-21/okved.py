import codecs
import json
import pickle
from pprint import pprint


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


# т.к. сложные типы, вроде кортежа, не сериализуются в json, можно использовать двоичный формат pickle
def write_pickle(filename, json_data):
    with open(filename, "wb") as f:
        try:
            pickle.dump(json_data, f)
        except Exception as e:
            log_text = "ошибка записи в файл: {}: {}".format(filename, str(e))
            print(log_text)


def open_pickle(filename):
    with open(filename, 'rb') as f:
        json_data = pickle.load(f)
    return json_data


# Добавил кол-во допОКВЭД для каждого оснОКВЭД
def dopOkved_for_osnOkved(json_dict):
    okved_dict = dict()
    # okved_key = ''
    # okved_value = dict()
    count_repeat_dop_okved = dict()
    for id_company in json_dict['data']:
        okved_key = (json_dict['data'][id_company]["КодОКВЭД"], json_dict['data'][id_company]["НаимОКВЭД"])
        okved_dict.setdefault(okved_key, [{'Кол-во допОКВЭД': 0}])

        for dop_okved in json_dict['data'][id_company]["СвОКВЭДДоп"]:
            okved_value = {dop_okved['КодОКВЭД']: dop_okved['НаимОКВЭД']}
            count_repeat_dop_okved.setdefault((str(dop_okved['КодОКВЭД']), str(dop_okved['НаимОКВЭД'])), 1)
            if okved_value in okved_dict[okved_key]:
                count_repeat_dop_okved[(str(dop_okved['КодОКВЭД']), str(dop_okved['НаимОКВЭД']))] += 1


            else:
                okved_dict[okved_key].append(okved_value)
        okved_dict[okved_key][0]['Кол-во допОКВЭД'] = len(okved_dict[okved_key]) - 1

    # Кол-во каждого допОКВЭД:
    # print(*count_repeat_dop_okved.items(), sep='\n')

    # Кол-во допОКВЭД для каждого ОКВЭД
    # for okved_key in okved_dict:
    #     print(*okved_key, okved_dict[okved_key][0]['Кол-во допОКВЭД'], end='\n')
    write_pickle('rezult_okved.json', okved_dict)
    return okved_dict


# Поиск допОКВЭД в оснОКВЭД
def number_dop_okved(all_dop_okved, num_dopOkved_dict):
    number_dop_okved_dict = {}

    for input_number_dop_okved in all_dop_okved.keys():

        count = 0
        for key, dop_okved in num_dopOkved_dict.items():
            # print(key,dop_okved)
            for number_dop_okved in dop_okved:
                # print('number_dop_okved',number_dop_okved)
                if input_number_dop_okved in number_dop_okved.keys():
                    count += 1
                    # print(key, dop_okved)
                    # print(key, dop_okved,number_dop_okved, end='\n')
                    # print(f'оснОКВЕД{key}', end='\n')

        number_dop_okved_dict.setdefault((input_number_dop_okved, all_dop_okved[input_number_dop_okved]), count)
    write_pickle('rezult_dop_okved.json', number_dop_okved_dict)
    return number_dop_okved_dict


def all_dop_okved(okved_dict):
    all_dop_okved_dict = {}
    for dop_okved_list in okved_dict.values():
        for dop_okved in dop_okved_list[1:]:
            all_dop_okved_dict.update(dop_okved)

    return all_dop_okved_dict


def pair_okved(json_dict):
    pair_okved_dict = {}
    for id_company in json_dict['data']:
        osn_okved_code_name = (json_dict['data'][id_company]["КодОКВЭД"], json_dict['data'][id_company]["НаимОКВЭД"])
        # print(osn_okved_code_name)

        for dop_okved in json_dict['data'][id_company]["СвОКВЭДДоп"]:
            dop_okved_code_name = (dop_okved['КодОКВЭД'], dop_okved['НаимОКВЭД'])
            pair_okved_key = (osn_okved_code_name, dop_okved_code_name)
            # print(pair_okved_key)

            if pair_okved_key in pair_okved_dict.keys():
                pair_okved_dict[pair_okved_key] += 1
            else:
                pair_okved_dict.setdefault(pair_okved_key, 1)

    write_pickle('rezult_pair_okved.json', sorted(pair_okved_dict.items(), key=lambda x: -x[1]))
    return pair_okved_dict


filepath = "zchb_org_from_inn_p2_utf8.json"

# okved_dict = dopOkved_for_osnOkved(read_json(filepath))
# print(okved_dict)
#
# dop_okved_dict = number_dop_okved(all_dop_okved(open_pickle('rezult_okved.json')), open_pickle('rezult_okved.json'))
# pprint(dop_okved_dict)

pair_okved_dict = pair_okved(read_json(filepath))
pprint(sorted(pair_okved_dict.items(), key=lambda x: -x[1])[:220])  # 20 пар
