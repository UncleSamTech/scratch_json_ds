import json
import os
import sb3
import uuid
import random
from pathlib import Path

class scratch_classifier:

    def __init__(self):
        self.parent_dict = {}
        self.type = ""
        self.raw = ""

class scratch_object():
        
    def __init__(self):
        self.type = None
        self.children = None

    def get_object_type(self):
        return self.type

    def get_object_children(self):
        return self.children
    
    def navigate_type_value(self,val):
        
        if isinstance(val,list):
            return "Array"
        elif isinstance(val,str) or isinstance(val,int) or isinstance(val,bool) or val is None:
            return "Literal"
        else:
            return "Object"
        
    def get_child_count(self,child_value):
        if isinstance(child_value,dict) or isinstance(child_value,list):
            return len(child_value)


        

    
class scratch_children:

    def __init__(self,property,type):
        self.property = property
        self.type = type
        
    def get_children_property(self):
        return self.property
    
    def get_children_type(self):
        return self.type

class scratch_property:

    def __init__(self,type,key,value):
        self.type = type
        self.key = key
        self.value = value
        
    def get_property_type(self):
        return self.type

    def get_property_key(self):
        return self.key
    
    def get_property_value(self):
        return self.key
    
class scratch_identifier:

    def __init__(self,type,value,raw):
        self.type = type
        self.value = value
        self.raw = raw

    def get_identifier_type(self):
        return self.type

    def get_identifier_value(self):
        return self.value
    
    def get_identifier_raw(self):
        return self.raw
    
class scratch_array:
    
    def __init__(self,type,children):
        self.type = type
        self.children = children
        
    def get_array_type(self):
        return self.type
    
    def get_array_children(self):
        return self.children
    
class scratch_literal:

    def __init__(self,type,value,raw):
        self.type = type
        self.value = value
        self.raw = raw

    def get_literal_type(self):
        return self.type

    def get_literal_value(self):
        return self.value
    
    def get_literal_raw(self):
        return self.raw

        
        
        

            
            
