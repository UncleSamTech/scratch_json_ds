import json
import os
import random
from pathlib import Path
from treelib import Node, Tree
import time


class scratch_processor:


    def __init__(self):
        self.count = 0
        self.top_keys_list = []
        self.second_keys_list = []
        self.second_value_list = []
        self.dict_key_list = []
        self.dict_value_list = []
        self.json_data = ""
        self.variables_value =[]
        self.variables_key = []
        self.blocks_object = []

    def check_key_match(self, values, match):
        self.top_keys_list = values.keys()
        return True if match in self.top_keys_list and len(self.top_keys_list) > 0 else False
    
    def gen_rand_numb(self):
        return random.randint(0,8638)
    
    def gen_uniq_value(self):
        return str(random.randint(0,8638) *  round(time.time() * 1000) *  random.randint(0,8789) * round(time.time() * 1000))

    def get_targets(self,values,match):
        if(self.check_key_match(values,match)):
            return values["targets"]
        else:
            return None
        
    def check_targets(self,values, match):
        return True if self.get_targets(values,match) is not None else False
    
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
                
    def get_variables(self, values):
        stored_targets = self.get_targets(values,"targets")
        if self.check_targets(values,"targets"):
            for dict_values in stored_targets:
                if isinstance(dict_values, dict) and "variables" in dict_values.keys():
                    stored_var = dict_values['variables']
                    for var_key, valu in stored_var.items():
                        self.variables_value.append(valu)
                        self.variables_key.append(var_key)
        print(self.variables_key, '->', self.variables_value)
        return self.variables_key, self.variables_value

    def get_costumes_sounds(self,values,unique_key):
        stored_targets = self.get_targets(values,"targets")
        if self.check_targets(values,"targets"):
            for dict_values in stored_targets:
                if isinstance(dict_values, dict) and unique_key in dict_values.keys():
                    stored_val = dict_values[unique_key]
                    print(stored_val)

    def get_monitors(self,values,match):
        if self.check_key_match(values,match):
            print(values["monitors"])
            if len(values["monitors"]) > 0:
                for i in values["monitors"]:
                    if isinstance(i,dict) and "params" in i.keys():
                        par_dict = i["params"]
                        for par_key, par_value in par_dict.items():
                            print(par_key, '->', par_value)
                    else:
                        print(i)

            return values["monitors"]
        else:
            return None

    def create_tree(self, blocks):
        tree = Tree()
        tree.create_node('scratch_block_tree','mia',data=blocks)
        if bool(blocks):
            for key, value in blocks.items():
                if isinstance(value, dict) and bool(value):
                    tree.create_node(key, key,parent='mia',data=value)
                    for sec_key, sec_value in value.items():
                        par_key = sec_key+str(self.gen_rand_numb()) + sec_key + str(self.gen_rand_numb())
                        sec_key_gen = sec_key+str(self.gen_rand_numb()) + sec_key + sec_key + str(self.gen_rand_numb())
                        tree.create_node(sec_key,par_key,parent=key,data=sec_value)
                        #tree.create_node(sec_value,sec_key_gen,parent=par_key,data=sec_value)
                       #print('d')
        return tree.show()

    def create_main_tree(self,blocks):
        if bool(blocks) and isinstance(blocks,dict):
            tree = Tree()
            tree.create_node('scratch_blocks','parent_block', data=blocks)
            par_id = self.gen_uniq_value()
            print(par_id)
            for parent_keys, parent_values in blocks.items():
                main_parent_id = parent_keys+par_id
                tree.create_node(parent_keys,main_parent_id,parent='parent_block',data=blocks)
                if isinstance(parent_values,dict) and bool(parent_values):
                    for second_key,second_values in parent_values.items():
                        second_parent_id = second_key+par_id
                        tree.create_node(second_key,second_parent_id,parent=main_parent_id,data=second_values)
                elif isinstance(parent_values,list) and len(parent_values) > 0:
                    for each_second_value in parent_values:
                        if isinstance(each_second_value,dict):
                            for third_key,third_value in each_second_value.items():
                                tree.create_node(third_key,third_key+par_id+third_key,parent=main_parent_id,data=third_value)
                        #tree.create_node(each_second_value, parent=main_parent_id,data=each_second_value)               
            tree.show()

    def get_block_objects(self,values,match):
        stored_targets = self.get_targets(values, match)
        if self.check_targets(values, match):
            for dict_values in stored_targets:
                if isinstance(dict_values,dict) and "blocks" in dict_values.keys():
                    blocks_stor = dict_values["blocks"]
                    self.create_tree(blocks_stor)
                    for blocks_key, blocks_value in blocks_stor.items():
                        if isinstance(blocks_value, dict):
                            #for sec_key, sec_value in blocks_value.items():
                                #print(blocks_key, 'top_key->', sec_key, '->' , sec_value)
                            self.blocks_object.append(blocks_value)
                            #print(blocks_key, '->', blocks_value)
                    #print(blocks_stor)
          

    def parse_json(self,file_path):
        string_to_parse = Path(file_path).read_text()
        self.json_data = json.loads(string_to_parse) 
        self.create_main_tree(self.json_data)
        self.top_keys_list = self.json_data.keys()
        for i in self.top_keys_list:
            if len(self.json_data[i]) > 0:
                for j in self.json_data[i]:
                    if isinstance(j,dict):
                        for keys,value in j.items():
                            self.second_keys_list.append(keys)
                            self.second_value_list.append(value)              
        #self.get_costumes_sounds(self.json_data,"costumes")   
        #self.get_monitors(self.json_data,"monitors")  
        #self.get_variables(self.json_data)   
        #self.get_block_objects(self.json_data, "targets")   
        #self.create_tree(self.json_data,"targets")     
        
    

scratch_processor_class = scratch_processor()
scratch_processor_class.parse_json('json_files/actual_response.json')

