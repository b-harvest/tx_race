import subprocess
import json

def get_json(query):
    res = subprocess.check_output(query, shell=True)
    res_json = json.loads(res.decode('utf-8'))
    return res_json


class Gaiacli(object):
    def __init__(self, gaiacli_path='gaiacli'):
        self.gaiacli_path = gaiacli_path

    def get_status(self):
        query = '{} {}'.format(self.gaiacli_path, 'status')
        return get_json(query)

    def query_account(self, address):
        query = '{} query account {} --trust-node --output json --indent'.format(self.gaiacli_path, address)
        return get_json(query)

    def keys_list(self):
        query = '{} keys list --output json --indent'.format(self.gaiacli_path)
        return get_json(query)
