#!/usr/bin/python3
# require >= Python 3.5.2
import subprocess
import json
import time
import datetime
import os
from gaiad import get_settings

config = get_settings(path='settings.json')

for p in [config.target_tx_path, config.target_signed_tx_path]:
    if not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

with open('send.json','r') as f:
    send_json=json.loads(f.read())

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

    for i in range(0, 3):
        cmd = 'gaiad tx broadcast {}/send_{}.json'.format(config.target_signed_tx_path, int(config.account_sequence)+i)

        for n in config.nodes:
            for b in ['async', 'sync', 'block']:
                cmd_last = cmd[:]
                cmd_last += " -b {} ".format(b)

                if 'localhost' not in n:
                    cmd_last += " --node '{}' ".format(n)

                if b == 'block':
                    cmd_last += ' &'

                print('\t', cmd_last)
                subprocess.call(cmd_last, shell=True)
                time.sleep(0.05)
            time.sleep(0.05)
        time.sleep(0.1)

    before_block = config.last_height