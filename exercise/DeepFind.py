#exercise 3 can be divided into 2 scenarios based on type of i/p provided and data needed in realworld situations.
#scenario 1 is when the key path is provided like a/b/c and when value of it is expected. ex: when we need the cost(c) of a book(b) in the library(a).
#scenario 2 is when you need all the values for a key ex: in maps from a source to destination there might be n ways, if we need the durations of all n ways we can use scenario 2 soln. to get all the values of duration form a api response.

#todo:
#input validations of nested obj and keys
#error handling and failing gracefully
#unit tests can be made using assertequals and assertnotequals.

# !/usr/bin/python3

from functools import reduce
from operator import getitem
import requests
import json
import sys

class Exercise3:

    def __init__(self):
        pass

    #exercise 3 scenario 1
    # def get_nested_value(self, nested_dict, path):
    #     obj = json.loads(nested_dict)
    #     #print(obj)
    #     # keys = path.split("/")
    #     # print(keys)
    #     # print(type(obj))
    #     # for i in range(0,len(keys)):
    #     #     obj = nestedDict[keys[i]]
    #     #     # except KeyError:
    #     #     #     print("No such key found")
    #     try:
    #         return reduce(getitem, path.split("/"), obj)
    #     except (IndexError, KeyError):
    #         return None

#exercise 3 scenario 1
    def get_nested_value(self, nested_dict, path):
        keys = path.split("/")
        # nested_dict = json.loads(nested_json)
        val = self.get_nested_value_with_list_support(nested_dict, keys)
        return val

    def get_nested_value_with_list_support(self, nested_obj, keys):
        obj = nested_obj
        try:
            if isinstance(obj, dict):
                obj = self.get_nested_value_with_list_support(obj[keys[0]], keys[1:])
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, dict):
                        obj = self.get_nested_value_with_list_support(item, keys)
            else:
                return obj
        except KeyError as ex:
            return None
        return obj


    #exercise 3 scenario 2
    def json_find(self, nested_dict, key):
        obj = json.loads(nested_dict)
        klist = []
        values = self.find_key(obj, klist, key)
        return values

    def find_key(self, obj, klist, key):
        if isinstance(obj, dict):
            try:
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        self.find_key(v, klist, key)
                    elif k == key:
                        klist.append(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            self.find_key(item, klist, key)
            except KeyError as ex:
                return None
        return klist


if __name__ == '__main__':
    e = Exercise3()
    #following are for exercise3 scenario 1
    #print(e.get_nested_value(metadata_json, "meta-data/ami-id"))
    print(e.get_nested_value({"a": {"b": {"c": 1}}}, "a/b/c"))  # => 1
    print(e.get_nested_value({'a': 0, 'b': [1, {"c":[3, 1]}, 2]}, "b/c")) # => 2 is not working. needs to find soln.

    # # following are for exercise3 scenario 2
    # print(e.json_find(metadata_json, "ami-id"))
    # print(e.json_find(json.dumps({"a": {"b": {"c": 1}}}), "c"))  # => 1
    # print(e.json_find(json.dumps([[[1, 2, 3], [10, 20, 30]]]), "2"))  # fail
    # print(e.json_find(json.dumps({'a': 0, 'b': [1, 2]}), "b"))  # => 1,2 failed needs fixing
    # print(e.json_find(json.dumps({'a': {'b': 1}, 'b': [[1, 2]]}), "b"))  # => 1,1,2 but returns 1, needs fixing too