import json
import os
import collections
from pathlib import Path


def parse_json(file_path):
    string_to_parse = Path(file_path).read_text()
    data = json.loads(string_to_parse) 
    dict_keys = []
    dict_value = []
    scratch_keys = data.keys()
    for i in scratch_keys:
        if len(data[i]) > 0:
            for j in data[i]:
                if isinstance(j,dict):
                    for keys,value in j.items():
                        print(keys , '->' , value)
                        dict_keys.append(keys)
                        dict_value.append(value)

parse_json('json_files/actual_response.json')
