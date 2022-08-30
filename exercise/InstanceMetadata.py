# We need to write code that will query the meta data of an instance within aws and provide a json formatted output. The choice of language and implementation is up to you.
# Since boto3 has no equivalent for boto.utils.get_instance_metadata(), we can write a py program that we assume will run within an ec2 instanace
# improvements:
# 1. use imsdv2
# 2. run it remotely using ssh or aws config remote exec.
# 3. add support for ipv6
# after trying by myself fpr sometime, i have found a soln online. the trick is that the last elements of tree in the meta-data does not have / and the o/p of last element can be single item(text) or a json.
#idea is to create a nested dict that can be easily converted to json

#Merging exercise 2 and 3 because the o/p of exercise 2 is a good input to showcase exercise 3.

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

#exercise 2
def iterate_url(url, uriList):
    output = {}
    for uri in uriList:
        new_url = url + uri
        try:
            r = requests.get(new_url)
        except requests.exceptions.HTTPError as err:
            exit(resp(err))
            #raise SystemExit(err)
        resp = r.text
        if uri[-1] == "/":
            list_of_uris = r.text.splitlines()
            output[uri[:-1]] = iterate_url(new_url, list_of_uris)
        elif is_json(resp):
            output[uri] = json.loads(resp)
        else:
            output[uri] = resp
    return output



def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

#exercise 3 scenario 1
def get_nested_value(nestedDict, path):
    obj = json.loads(nestedDict)
    #print(obj)
    # keys = path.split("/")
    # print(keys)
    # print(type(obj))
    # for i in range(0,len(keys)):
    #     obj = nestedDict[keys[i]]
    #     # except KeyError:
    #     #     print("No such key found")
    try:
        return (reduce(getitem, path.split("/"), obj))
    except (IndexError, KeyError):
        return None

#exercise 3 scenario 2
def json_find(nestedDict, key):
    obj = json.loads(nestedDict)
    klist = []
    values = find_key(obj, klist, key)
    return values

def find_key(obj, klist, key):
   if isinstance(obj, dict):
       for k, v in obj.items():
           if isinstance(v, (dict, list)):
               find_key(v, klist, key)
           elif k == key:
               lkist.append(v)
   elif isinstance(obj, list):
       for item in obj:
           find_key(item, klist, key)
   return klist


if __name__ == '__main__':
    base_url = 'http://169.254.169.254/latest/'
    # input_string = input('Enter elements of a list separated by space ')
    # print("\n")
    # elementPath = input_string.split()
    elementPath = ["meta-data/"] #if path like "meta-data/ami-id" is passed, function wold return a json with desired dict.
    metadata = iterate_url(base_url, elementPath)
    metadata_json = json.dumps(metadata,indent=4, sort_keys=True)
    print(metadata_json) # would print o/p of exercise2
    #following are for exercise3 scenario 1
    print(get_nested_value(metadata_json, "meta-data/ami-id"))
    print(get_nested_value(json.dumps({"a": {"b": {"c": 1}}}), "a/b/c") ) # => 1
    print(get_nested_value(json.dumps({'a': 0, 'b': [[1, 2]]}), "b/0/1"))  # => 2

    # following are for exercise3 scenario 2
    print(json_find(metadata_json, "ami-id"))
    print(json_find(json.dumps({"a": {"b": {"c": 1}}}), "c"))  # => 1
    print(json_find(json.dumps([[[1, 2, 3], [10, 20, 30]]]), "2"))  # fail
    print(json_find(json.dumps({'a': 0, 'b': [1, 2]}), "b"))  # => 1,2 failed needs fixing
    print(json_find(json.dumps({'a': {'b': 1}, 'b': [[1, 2]]}), "b"))  # => 1,1,2 but returns 1, needs fixing too