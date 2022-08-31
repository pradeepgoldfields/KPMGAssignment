# We need to write code that will query the meta data of an instance within aws and provide a json formatted output. The choice of language and implementation is up to you.
# Since boto3 has no equivalent for boto.utils.get_instance_metadata(), we can write a py program that we assume will run within an ec2 instanace
# improvements:
# 1. use imsdv2
# 2. run it remotely using ssh or aws config remote exec.
# 3. add support for ipv6
# after trying by myself fpr sometime, i have found a soln online. the trick is that the last elements of tree in the meta-data does not have / and the o/p of last element can be single item(text) or a json.
#idea is to create a nested dict that can be easily converted to json

# !/usr/bin/python3

from functools import reduce
from operator import getitem
import requests
import json


class Exercise2:

    def __init__(self):
        pass

#exercise 2
    def iterate_url(self, url, uriList):
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
# iterating edges and getting rid of /
                output[uri[:-1]] = self.iterate_url(new_url, list_of_uris)
# found node of type json?
            elif self.is_json(resp):
                output[uri] = json.loads(resp)
# found node of type string/number/None?
            else:
                output[uri] = resp
        return output

    def is_json(self,myjson):
        try:
            json.loads(myjson)
        except ValueError:
            return False
        return True


if __name__ == '__main__':
    base_url = 'http://169.254.169.254/latest/'
    # input_string = input('Enter elements of a list separated by space ')
    # print("\n")
    # elementPath = input_string.split()
    e = Exercise2()
    elementPath = ["meta-data/"] #if path like "meta-data/ami-id" is passed, function wold return a json with desired dict.
    metadata = e.iterate_url(base_url, elementPath)
    metadata_json = json.dumps(metadata,indent=4, sort_keys=True)
    print(metadata_json) # would print o/p of exercise2