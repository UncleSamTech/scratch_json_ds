import json
import os
import collections
from pathlib import Path


def parse_json(file_path):
    string_to_parse = Path(file_path).read_text()
    data = json.loads(string_to_parse) 
    dict_keys = []
    dict_keys_type = []
    scratch_keys = data.keys()
    #print(scratch_keys)
    for i in scratch_keys:
        if len(data[i]) > 0:
            for j in data[i]:
                if isinstance(j,dict):
                    for keys in j:
                        dict_keys.append(keys)
                        dict_keys_type.append(type(j[keys]))

            print(dict_keys)
            print(dict_keys_type)
            
           
            


   # print('extensions_count' , extensions_count)
   # print('targets_count ' , targets_count)
    #print('monitors_count' , monitors_count)
    #print('meta_count' , meta_count)
parse_json('json_files/actual_response.json')
