import json
import os
import sb3
import uuid
import random
from pathlib import Path
from scratch_classifier import scratch_object
from treelib import Node, Tree
import time
import zipfile

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
                for keys,values in value.items():
                    print(keys , '->', values)
                    self.dict_key_list.append(keys)
                    self.dict_value_list.append(values)
            elif type(value) is bool:
                print('bool datatype with value', value)
            elif type(value) is list:
                for each_val in value:
                    print('item is' , each_val)
                    if isinstance(each_val,dict):
                        for keys,values in each_val.items():
                            print(keys , 'second_level->', values)
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
        return tree
    
    def unpack_sb3(self,sb3_file,sprite=False):
        need = "project.json" if sprite else "project.json"
        with zipfile.ZipFile(sb3_file) as sb3zip:
            names = sb3zip.namelist()
            if need not in names:
                print('sprite3 must contain sprite.json')
            else:
                json_file =  json.loads(sb3zip.read(need).decode("utf-8"))
                return json.dumps(json_file)
                
    def unpack_all_dict(self, data):
        if isinstance(data,dict) and bool(data) is False:
           return data
        elif isinstance(data,dict) and bool(data):
            for keys, values in data.items():
               print(keys)
               print(self.unpack_all_dict(data[keys]) )
              
               #print(keys)
        

               
            
    def use_unpack(self, imp):
        key = self.unpack_all_dict(imp)
        print(key)
       # print(val)

    def create_main_tree(self,blocks):
        tree = Tree()
        if bool(blocks) and isinstance(blocks,dict):
            
            tree.create_node('scratch_blocks','parent_block', data=blocks)
            par_id = self.gen_uniq_value()
            for parent_keys, parent_values in blocks.items():
                main_parent_id = str(uuid.uuid4())
                tree.create_node(parent_keys,main_parent_id,parent='parent_block',data=blocks)
                if isinstance(parent_values,dict) and bool(parent_values):
                    for second_key,second_values in parent_values.items():
                        second_parent_id = str(uuid.uuid4()) + par_id
                        sec_par_val_id = str(uuid.uuid4()) + par_id + str(uuid.uuid4())
                        tree.create_node(second_key,second_parent_id,parent=main_parent_id,data=second_values)
                        tree.create_node(second_values,sec_par_val_id,parent=main_parent_id,data=second_values)
                        if isinstance(second_values,dict) and bool(second_values):
                            for sec_third_key,sec_third_value in second_values.items():
                                sec_third_par_val_id = str(uuid.uuid4()) + par_id + str(uuid.uuid4()) + par_id
                                tree.create_node(sec_third_key,sec_third_par_val_id,parent=sec_par_val_id,data=sec_third_value)  
                                tree.create_node(sec_third_value,sec_third_par_val_id,parent=sec_par_val_id,data=sec_third_value)
                                if isinstance(sec_third_value,dict) and bool(sec_third_value):
                                    for sec_fourth_key, sec_fourth_val in sec_third_value.items():
                                        sec_fourth_id =  str(uuid.uuid4())
                                        tree.create_node(sec_fourth_key,sec_fourth_id,parent=sec_third_par_val_id,data=sec_fourth_val)
                                        tree.create_node(sec_fourth_val, str(uuid.uuid4()), parent=sec_fourth_id,data=sec_fourth_val)
                
                elif isinstance(parent_values,list) and len(parent_values) > 0:
                    for each_second_value in parent_values:
                        if isinstance(each_second_value,dict) and bool(each_second_value):
                            for third_key,third_value in each_second_value.items():
                                third_par_id = str(uuid.uuid4()) + par_id + str(uuid.uuid4()) + par_id
                                third_par_id_val = str(uuid.uuid4()) + par_id + str(uuid.uuid4()) + par_id + str(uuid.uuid4())
                                tree.create_node(third_key,third_par_id,parent=main_parent_id,data=third_value)
                                if isinstance(third_value, dict) and bool(third_value):
                                    for fourth_key, fourth_value in third_value.items():
                                        fourth_par_id =  str(uuid.uuid4()) + par_id + par_id
                                        fourth_par_id_val = fourth_par_id+par_id
                                        tree.create_node(fourth_key,fourth_par_id,parent=third_par_id,data=fourth_value)
                                        tree.create_node(fourth_value,fourth_par_id_val,parent=fourth_par_id,data=fourth_value)
                                        if isinstance(fourth_value,dict) and bool(fourth_value):
                                            for fifth_dict_key, fifth_dict_value in fourth_value.items():
                                                fifth_par_id = str(uuid.uuid4()) + par_id
                                                tree.create_node(fifth_dict_key,fifth_par_id,parent=fourth_par_id_val,data=fifth_dict_value)
                                                if isinstance(fifth_dict_value,dict) and bool(fifth_dict_value):
                                                    for sixth_key, sixth_value in fifth_dict_value.items():
                                                        sixth_par_id = str(uuid.uuid4()) + par_id + fifth_par_id
                                                        tree.create_node(sixth_key,sixth_par_id, parent=fifth_par_id,data=sixth_value)
                                                        tree.create_node(sixth_value,str(uuid.uuid4()),parent=sixth_par_id,data=sixth_value)
                                elif isinstance(third_value, list) and len(third_value):
                                    for sub_third_value in third_value:
                                        if isinstance(sub_third_value, list) and len(sub_third_value) > 0:
                                            for sub_fourth_key,sub_fourth_value in sub_third_value.items():
                                                sub_fourth_par_id = str(uuid.uuid4()) + third_par_id + third_par_id_val
                                                tree.create_node(sub_fourth_key,sub_fourth_par_id,parent=third_par_id,data=sub_fourth_value)
                                                tree.create_node(sub_fourth_value,str(uuid.uuid4()),parent=sub_fourth_par_id,data=sub_fourth_value)
                                else:
                                    non_list_third_id = str(uuid.uuid4()) + third_par_id + par_id
                                    third_value = 'None' if third_value is None else third_value
                                    tree.create_node(third_value, non_list_third_id,parent=third_par_id,data=third_value)
                        elif isinstance(each_second_value,list) and len(each_second_value) > 0:
                            for sub_each_second_value in each_second_value:
                                if isinstance(sub_each_second_value,dict) and bool(sub_each_second_value):
                                    for sub_each_key, sub_each_value in sub_each_second_value:
                                        tree.create_node(sub_each_key,str(uuid.uuid5),parent=main_parent_id,data=sub_each_value)
                        
                        else:
                            each_second_value = 'None' if each_second_value is None else each_second_value
                            tree.create_node(each_second_value,str(uuid.uuid4()),parent=main_parent_id,data=each_second_value)
                else:
                    tree.create_node(parent_values,parent=main_parent_id,data=parent_values)
                   
            
        elif isinstance(blocks,list) and len(blocks) > 0:
            for sing_block in blocks:
                if isinstance(sing_block,dict) and bool():
                    for sub_sing_block_key, sub_sing_block_value in sing_block:
                        sub_sing_block_id = str(uuid.uuid4())
                        tree.create_node(sub_sing_block_key,sub_sing_block_id,parent='list_block',data=sub_sing_block_value)
                        
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
                            self.blocks_object.append(blocks_value)
                                 
    def check_nested_dict(self,values):
       if isinstance(values,dict) and bool(values):
           for value in values.values():
               if isinstance(value,dict):
                   print(value)   
    
    def check_dict_depth(self, dic,level=1):
        if not isinstance(dic,dict) or not dic:
            return level
        depth = max(self.check_dict_depth(dic[key], level + 1) for key in dic)
        print(depth)
        return depth

    def rev(self,val):
        rev = ""
        if val == ""  or len(val) == 1:
            rev = val

        for i in range(len(val)):
           rev = val[i+1:] + val[i]
           print(rev)
        return rev
    
    def dec_bin(self,dec_num, result=""):
        if dec_num == 0:
            return result
        
        result = str(dec_num % 2) + result
        print(result)
        while dec_num != 0:
            val = dec_num / 2
        print(result)
        print(val)
        #return self.dec_bin(dec_num / 2, result)

    def get_blocks_recurs(self,json_data,target_match,block_match):
        
        
        empty_dict = {}
        if self.check_targets(json_data,target_match):
            targets_data = json_data[target_match]
            for each_data in targets_data:
                if isinstance(each_data,dict) and bool(each_data):
                   empty_dict =  each_data[block_match] 
        return empty_dict
                            

    def classify_type(self,param):
        emmitted_type = ""
        if isinstance(param,int) or isinstance(param,str) or isinstance(param,bool):
            emmitted_type = "Identifier"
        elif isinstance(param,dict):
            emmitted_type = "Object"
        else:
            emmitted_type = "Array"
        return emmitted_type
                            
    def rec_extr_dict(self,blocks):
        tree = Tree()
        scratch_objects = scratch_object()
        tree.create_node('','parent_block', data=blocks)
        if isinstance(blocks,dict) and bool(blocks):
            for key,value in blocks.items():
                
                if isinstance(value,dict):
                   self.rec_extr_dict(value)
                
                else:
                    sec_key =  str(uuid.uuid4())
                    ano_key = scratch_objects.navigate_type_value(value)
                    
                    tree.create_node(ano_key,sec_key,parent='parent_block',data=value)
                    tree.create_node(value,str(uuid.uuid4()),parent=sec_key,data=value)
          
                    
        tree.show()


                 

    def parse_json(self,file_path):
        string_to_parse2 = self.unpack_sb3(file_path)
        self.json_data = json.loads(string_to_parse2) 
        
        val = self.get_blocks_recurs(self.json_data,'targets','blocks')
        self.rec_extr_dict(val)
        

    
    
    


    
                 
        
        
    

scratch_processor_class = scratch_processor()
scratch_processor_class.parse_json('json_files/complete_project.sb3')


