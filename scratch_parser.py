import json
import os
import collections
from pathlib import Path


class scratch_processor:


    def __init__(self):
        self.count = 0
        self.top_keys_list = []
        self.second_keys_list = []
        self.second_value_list = []
        self.dict_key_list = []
        self.dict_value_list = []

    
    def extract_dict_values(self,value):
        if isinstance(value,dict):
            for keys,values in value.items():
                print(keys , '->', values)
                self.dict_key_list.append(keys)
                self.dict_value_list.append(values)
        #return self.dict_key_list, self.dict_value_list

    def extract_list_values(self, values):
        if isinstance(values, list) and len(values) > 0:
            for each_val in values:
                print('item is' , each_val)

    

    def parse_json(self,file_path):
        string_to_parse = Path(file_path).read_text()
        data = json.loads(string_to_parse) 
        dict_keys = []
        dict_value = []
        self.top_keys_list = data.keys()
        for i in self.top_keys_list:
            if len(data[i]) > 0:
                for j in data[i]:
                    if isinstance(j,dict):
                        for keys,value in j.items():
                            is_dict = 'a dictionary' if isinstance(value,dict) else 'not a dictionary'
                        #print(keys , '->' , value, type(value))
                            self.second_keys_list.append(keys)
                            self.second_value_list.append(value)
                            if type(value) is str:
                                print(keys ,'is string datatype with value ',value)
                            elif type(value) is int:
                                print(keys , 'is an int datatype with ', value)
                            elif type(value) is dict:
                                #print(keys , ' is a dictionary datatype', value)
                                self.extract_dict_values(value)
                            elif type(value) is bool:
                                print(keys, 'is a bool datatype with value', value)
                            elif type(value) is list:
                                #print(keys, 'is a list with length of ', len(value))
                                self.extract_list_values(value)
                            else:
                                print('unknown data structure')
    

   



                        


scratch_processor_class = scratch_processor()
scratch_processor_class.parse_json('json_files/actual_response.json')
