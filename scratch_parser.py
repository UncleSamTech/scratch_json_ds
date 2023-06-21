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
                        is_dict = 'a dictionary' if isinstance(value,dict) else 'not a dictionary'
                        #print(keys , '->' , value, type(value))
                        dict_keys.append(keys)
                        dict_value.append(value)
                        if(type(value) is str):
                            print(keys ,'is string datatype',value)
                        elif(type(value) is int):
                            print(keys , 'is an int datatype', value)
                        elif type(value) is dict:
                            print(keys , ' is a dictionary datatype', value)
                        elif type(value) is bool:
                            print(keys, 'is a bool datatype', value)
                        elif type(value) is list:
                            print(keys, 'is a list with length of ', len(value))
                        else:
                            print('unknown data structure')

                        


parse_json('json_files/actual_response.json')
