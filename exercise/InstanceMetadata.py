# We need to write code that will query the meta data of an instance within aws and provide a json formatted output. The choice of language and implementation is up to you.
# Since boto3 has no equavalent for boto.utils.get_instance_metadata(), we can write a py program that we assume will run within an ec2 instanace
# improvements:
# 1. use imsdv2
# 2. run it remotely using ssh or aws config remote exec.
# 3. add support for ipv6
# after trying by myself fpr sometime, i have found a soln online. the trick is that the last elements of tree in the meta-data does not have / and the o/p of last element can be single item(text) or a json.
#idea is to create a nested dict that can be easily converted to json

#Merging exercise 2 and 3 because the o/p of exercise 2 is a good input for exercise 3.

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

#exercise 3
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

# def json_extract(obj, key):
#     """Recursively fetch values from nested JSON."""
#     arr = []
#
#     def extract(obj, arr, key):
#         """Recursively search for values of key in JSON tree."""
#         if isinstance(obj, dict):
#             for k, v in obj.items():
#                 if isinstance(v, (dict, list)):
#                     extract(v, arr, key)
#                 elif k == key:
#                     arr.append(v)
#         elif isinstance(obj, list):
#             for item in obj:
#                 extract(item, arr, key)
#         return arr
#
#     values = extract(obj, arr, key)
#     return values

if __name__ == '__main__':
    base_url = 'http://169.254.169.254/latest/'
    # input_string = input('Enter elements of a list separated by space ')
    # print("\n")
    # elementPath = input_string.split()
    elementPath = ["meta-data/"]
    metadata = iterate_url(base_url, elementPath)
    metadata_json = json.dumps(metadata,indent=4, sort_keys=True)
    respVal = get_nested_value(metadata_json, "meta-data/ami-id")
    # print(get_nested_value(data={"a": {"b": {"c": 1}}}, keys=["a", "b", "c"]))  # => 1
    # print(get_nested_value(data=[[[1, 2, 3], [10, 20, 30]]], keys=[0, 1, 2]))  # => 30
    # print(get_nested_value(data={'a': 0, 'b': [[1, 2]]}, keys=['b', 0, 1]))  # => 2
    # print(get_nested_value(data=some_sequence, keys=[]))  # => some_sequence
    print(respVal)