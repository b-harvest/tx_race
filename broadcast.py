#!/usr/bin/python3
# require >= Python 3.5.2
import subprocess
import json
import time
import datetime
import os
from gaiacli import get_settings

# config = get_settings(path='settings.json')
config = get_settings(path='settings_test.json')

for p in [config.target_tx_path, config.target_signed_tx_path]:
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

with open('send.json','r') as f:
    send_json=json.loads(f.read())

# a = "echo '123123123' | gaiacli tx send cosmos1ul3ef4trvjfmgaptu70ed4fjlky2aa49vna6uy 100000000000000000000muon --from cosmos1ul3ef4trvjfmgaptu70ed4fjlky2aa49vna6uy --chain-id gaia-13003 --gas 40000 --gas-prices 1.5muon --memo 'auto' --yes -b block"
before_block = 0
while True:
    config.update_status()
    config.update_account()
    if before_block == config.last_height:
        print('...')
        continue

    print("---------------------------------------------")
    print("block : {}, catching_up: {}, balance : {}, sequence : {}".format(config.last_height, config.catching_up, config.balance, config.account_sequence))
    print("---------------------------------------------")

    # # target_amount = config.amount
    # remain_for_fee = 5000000
    # if config.balance < remain_for_fee:
    #     time.sleep(3)
    #     continue
    # target_amount = config.balance - remain_for_fee

    # cmd = 'gaiacli tx broadcast {}/send_{}.json'.format(config.target_signed_tx_path, config.account_sequence)

    # cmd = "echo '{}' | gaiacli tx send {} {}{} --from {} -a {} --chain-id {} --gas {} --gas-prices {}{} --yes".format(
    #     config.passphrase, config.to_address, target_amount, config.denom, config.from_address, config.account_number, config.chain_id, config.gas, config.gas_price, config.denom
    # )
    # for b in ['block']:
    for i in range(0, 3):
        cmd = 'gaiacli tx broadcast {}/send_{}.json'.format(config.target_signed_tx_path, config.account_sequence+i)

        for n in config.nodes:
            for b in ['async', 'sync', 'block']:
                cmd_last = cmd[:]
                # memo = 'race_tx_realtime_{}_{}_{}'.format(b, config.account_sequence, datetime.datetime.now())
                # if i != 0:
                #     memo += ' sequence delta {}'.format(i)
                #     cmd_last += ' --sequence {}'.format(int(config.account_sequence)+i)
                cmd_last += " -b {} ".format(b)

                if 'localhost' not in n:
                    cmd_last += " --node '{}' ".format(n)

                if b == 'block':
                    cmd_last += ' &'

                print('\t', cmd_last)
                subprocess.call(cmd_last, shell=True)
                time.sleep(0.05)
                # subprocess.call(cmd_last, shell=True)
                # subprocess.call(cmd_last, shell=True)
            time.sleep(0.05)
        time.sleep(0.1)

    before_block = config.last_height