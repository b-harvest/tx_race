#!/usr/bin/python3
# require >= Python 3.5.2
import subprocess
import json
import datetime
import os
from gaiacli import Gaiacli


# account check
gaiacli_path = input("input gaiacli_path (default: 'gaiacli' ex: '/home/ubuntu/go/bin/gaiacl /home/ubuntu/.gaiacli')") or 'gaiacli'


gaiacli = Gaiacli(gaiacli_path)
status = gaiacli.get_status()

# sync check
if status['sync_info']['catching_up']:
    print('not synced')
    exit()

chain_id = status['node_info']['network']
last_height = status['sync_info']['latest_block_height']
last_time = status['sync_info']['latest_block_time']

print(chain_id, last_height, last_time)

from_address = input("input from_address: ") or 'cosmos10e4vsut6suau8tk9m6dnrm0slgd6npe3hjqndl'

account = gaiacli.query_account(from_address)

account_number = int(account['value']['account_number'])
account_sequence = int(account['value']['sequence'])

print(from_address, account_number, account_sequence)

if len(account['value']['coins']) == 1:
    denom = account['value']['coins'][0]['denom']
    balance = account['value']['coins'][0]['amount']
else:
    denom = input("input denom (default uatom) : ") or 'uatom'
    amount = input("input amount: ")

key_name = None
keys = gaiacli.keys_list()
for k in keys:
    if k['address'] == from_address:
        key_name = k['name']
        break

if not key_name:
    print('key not exist')
    exit()

print(key_name, balance, denom)

to_address = input("input to_address: ")
while not to_address or not to_address.startswith('cosmos1'):
    to_address = input("re-input to_address: ")

fee_amount = input("input fee_amount (default 1) : ") or 1
gas = input("input gas (default 35000) : ") or 35000
passphrase = input("input passphrase: ")
while not passphrase or len(passphrase) < 8:
    passphrase = input("re-input passphrase: ")

number_of_tx = int(input("input number_of_tx (default 100) : ") or 100)

target_tx_path = input("input target_tx_path (default: signed_tx_path) : ") or "signed_tx_path"
target_signed_tx_path = input("input target_tx_path (default: target_signed_tx_path) : ") or "signed_tx_path"

for p in [target_tx_path, target_signed_tx_path]:
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

with open("send.json","r") as f:
    send_json=json.loads(f.read())

for sequence in range(account_sequence,account_sequence+number_of_tx):
    send_json["value"]["msg"][0]["value"]["amount"][0]["amount"] = str(int(amount))
    send_json["value"]["memo"] = "race_tx_{}_{}".format(sequence, datetime.datetime.now(), )
    tx_path = "{}/send_{}.json".format(target_tx_path, sequence)
    signed_tx_path = "{}/send_{}.json".format(target_signed_tx_path, sequence)
    with open(tx_path,"w+") as f:
        f.write(json.dumps(send_json))
    
    cmd_string = "echo {} | sudo gaiacli tx sign {} --from {} --sequence {} --account-number {} --chain-id {} --yes --offline > {}".format(passphrase, tx_path, key_name, sequence, account_number, chain_id, signed_tx_path)
    subprocess.run(cmd_string, shell=True)
    print(str(sequence) + " complete!")
