#!/usr/bin/python3
# require >= Python 3.5.2
import subprocess
import json
import datetime
import os
from gaiad import get_settings

config = get_settings(path='settings.json')

for p in [config.target_tx_path, config.target_signed_tx_path]:
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

with open('send.json','r') as f:
    send_json=json.loads(f.read())


for sequence in range(int(config.account_sequence), int(config.account_sequence) + int(config.number_of_tx)):

    config.start_gas_price = float(config.start_gas_price)
    total_gas = str(int(int(config.gas) * float(config.start_gas_price)))

    if int(config.gas) > int(total_gas):
        total_gas = str(int(config.gas))

    send_json['body']['messages'][0]['amount'][0]['amount'] = str(
        int(config.amount))
    send_json['body']['messages'][0]['amount'][0]['denom'] = config.denom
    send_json['body']['messages'][0]['from_address'] = config.from_address
    send_json['body']['messages'][0]['to_address'] = config.to_address
    send_json['auth_info']['fee']['amount'][0]['denom'] = config.denom
    send_json['auth_info']['fee']['amount'][0]['amount'] = total_gas
    send_json['body']['memo'] = 'race_tx_{}_{}'.format(
        sequence, datetime.datetime.now())
    tx_path = '{}/send_{}.json'.format(config.target_tx_path, sequence)
    signed_tx_path = '{}/send_{}.json'.format(config.target_signed_tx_path, sequence)
    with open(tx_path, 'w+') as f:
        f.write(json.dumps(send_json))
    
    cmd_string = 'gaiad tx sign {} --from {} --sequence {} --account-number {} --chain-id {} --yes --offline > {}'.format(
        tx_path, config.key_name, sequence, config.account_number, config.chain_id, signed_tx_path)
    print(cmd_string, total_gas)
    if not config.debug:
        subprocess.run(cmd_string, shell=True)
    print(str(sequence) + ' complete!')

    if config.start_gas_price > config.gas_price:
        config.start_gas_price -= 0.1
