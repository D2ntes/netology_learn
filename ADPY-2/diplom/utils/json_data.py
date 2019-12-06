import json
from config import NAME_FILE_JSON

def save_result_to_json(result):
    with open(NAME_FILE_JSON, "w", encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False)