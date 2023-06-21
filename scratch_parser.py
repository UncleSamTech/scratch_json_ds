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
        self.json_data = ""

    
    
    def decide_next_steps(self,value):
            if type(value) is str:
                print('string datatype with value ',value)
            elif type(value) is int:
                print('int datatype with ', value)
            elif type(value) is dict:
                #self.extract_dict_values(value)
                for keys,values in value.items():
                    print(keys , '->', values)
                    self.dict_key_list.append(keys)
                    self.dict_value_list.append(values)
            elif type(value) is bool:
                print('bool datatype with value', value)
            elif type(value) is list:
                #self.extract_list_values(value)
                for each_val in value:
                    print('item is' , each_val)
                    if isinstance(each_val,dict):
                        for keys,values in each_val.items():
                            print(keys , 'second_level->', values)
                    #self.dict_key_list.append(keys)
                    #self.dict_value_list.append(values)
            else:
                print('unknown data structure')


    def extract_dict_values(self,value):
        for keys,values in value.items():
            print(keys , '->', values)
            self.dict_key_list.append(keys)
            self.dict_value_list.append(values)
            self.decide_next_steps(value)

    def extract_list_values(self, values):
        for each_val in values:
            print('item is' , each_val)
            self.decide_next_steps(values)
                

    

    def parse_json(self,file_path):
        string_to_parse = Path(file_path).read_text()
        self.json_data = json.loads(string_to_parse) 
        self.top_keys_list = self.json_data.keys()
        for i in self.top_keys_list:
            if len(self.json_data[i]) > 0:
                for j in self.json_data[i]:
                    if isinstance(j,dict):
                        for keys,value in j.items():
                            self.second_keys_list.append(keys)
                            self.second_value_list.append(value)
                            self.decide_next_steps(value)
                            
    

   



                        


scratch_processor_class = scratch_processor()
scratch_processor_class.parse_json('json_files/actual_response.json')

