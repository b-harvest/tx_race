import subprocess
import json


def get_json(query):
    res = subprocess.run(
        query, shell=True, capture_output=True)
    output = res.stdout
    if output == b'':
        output = res.stderr
    res_json = json.loads(output.decode('utf-8'))
    return res_json


def find_dic(dic, target):
    for k, v in dic.items():
        if k == target:
            return v
        if type(v) == dict:
            res = find_dic(v, target)
            if res:
                return res


class Config(object):
    sync_check = None
    gaiad_path = None
    chain_id = None
    from_address = None
    account_number = None
    account_sequence = None
    denom = None
    balance = None
    amount = None
    key_name = None
    to_address = None
    fee_amount = None
    gas = None
    start_gas_price = None
    gas_price = None
    passphrase = None
    number_of_tx = None
    target_tx_path = None
    target_signed_tx_path = None
    debug = None
    last_height = None
    last_time = None
    catching_up = None
    nodes = None

    def __init__(self, **kwargs):
        [self.__setattr__(attr, kwargs[attr]) for attr in dir(self) if not attr.startswith('_') and attr in kwargs]
        # object.__init__(**kwargs)

    def copy(self):
        kwargs = {k: v for k, v in self.__dict__.items() if k not in ['_sa_instance_state', 'id']}
        obj = self.__class__(**kwargs)
        return obj

    def get_status(self):
        query = '{} {}'.format(self.gaiad_path, 'status')
        return get_json(query)

    def get_balances(self, address):
        query = '{} query bank balances {} --output json'.format(
            self.gaiad_path, address)
        return get_json(query)

    def query_account(self, address):
        query = '{} query account {} --output json'.format(self.gaiad_path, address)
        return get_json(query)

    def keys_list(self):
        query = '{} keys list --output json'.format(self.gaiad_path)
        return get_json(query)

    def update_account(self):
        account = self.query_account(self.from_address)
        self.account_number = find_dic(account, 'account_number')
        self.account_sequence = find_dic(account, 'sequence')
        # self.balance = find_dic(account, 'sequence')
        balances = self.get_balances(self.from_address)
        coins = find_dic(balances, 'balances')
        if coins:
            for coin in coins:
                if coin['denom'] == self.denom:
                    self.balance = int(coin['amount'])

    def update_status(self):
        status = self.get_status()
        self.last_height = status['SyncInfo']['latest_block_height']
        self.last_time = status['SyncInfo']['latest_block_time']
        self.catching_up = status['SyncInfo']['catching_up']


def get_settings(path='settings.json'):
    with open(path) as fp:
        config = Config(**json.load(fp))

    if not config.gaiad_path:
        config.gaiad_path = input(
            "input gaiad_path (default: 'gaiad' ex: '/home/ubuntu/go/bin/gaiad /home/ubuntu/.gaiad')") or 'gaiad'

    # gaiacli = Gaiacli(config.gaiad_path)

    status = config.get_status()
    if status:
        last_height = status['SyncInfo']['latest_block_height']
        last_time = status['SyncInfo']['latest_block_time']

    config.update_status()

    # sync check
    if config.sync_check and status['SyncInfo']['catching_up']:
        print('not synced')
        exit()

    if not config.chain_id:
        config.chain_id = status['NodeInfo']['network']

    print(config.chain_id, last_height, last_time)

    if not config.from_address :
        config.from_address = input('input from_address: ')

    account = config.query_account(config.from_address)

    if not config.account_number:
        if account:
            config.account_number = find_dic(account, 'account_number')
            if not config.account_number:
                print(account)
            # account_number = int(account['value']['account_number'])

        if not config.account_number:
            config.account_number = int(input('input account_number : '))

    if not config.account_sequence:
        if account:
            config.account_sequence = find_dic(account, 'sequence')

        if not config.account_sequence:
            config.account_sequence = int(input('input account_sequence : '))

    print(config.from_address, config.account_number, config.account_sequence)
    config.update_account()
    print(config.from_address, config.account_number, config.account_sequence)

    if not config.denom:
        if account:
            coins = find_dic(account, 'balances')
            if coins:
                for coin in coins:
                    if coin['denom'] == config.denom:
                        config.balance = int(coin['amount'])
            else:
                print(coins)
        else:
            config.denom = input('input denom (default uatom) : ') or 'uatom'

    if not config.balance:
        if account:
            coins = find_dic(account, 'balances')
            if coins:
                for coin in coins:
                    if coin['denom'] == config.denom:
                        config.balance = int(coin['amount'])
            else:
                print(coins)
        else:
            config.balance = int(input('input test balance : '))


    if not config.amount:
        config.amount = int(input('input amount: '))

    # while config.balance - config.amount < 10000000:
    #     config.amount = int(input('amount is too big, {}, {} re-input amount: '.format(config.balance, config.amount)))


    if not config.key_name:
        config.key_name = None
        keys = config.keys_list()
        if keys:
            for k in keys:
                if k['address'] == config.from_address:
                    config.key_name = k['name']
                    break

            if not config.key_name:
                print('key not exist')
                exit()

    print(config.key_name, config.balance, config.denom)

    if not config.to_address:
        config.to_address = input('input to_address: ')
        while not config.to_address or not config.to_address.startswith('cosmos1'):
            config.to_address = input('re-input to_address: ')

    if not config.fee_amount:
        config.fee_amount = int(input('input fee_amount (default 1) : ')) or 1
    if not config.gas:
        config.gas = intput(input('input gas (default 35000) : ')) or 35000
    if not config.passphrase:
        config.passphrase = input('input passphrase: ')
        while not config.passphrase or len(config.passphrase) < 8:
            config.passphrase = input('re-input passphrase over length 8: ')
    
    if not config.gas_price:
        config.gas_price = float(input('input gas_price: default 1.5') or 1.5)

    if not config.number_of_tx:
        config.number_of_tx = int(input('input number_of_tx (default 100) : ') or 100)

    if not config.target_tx_path:
        config.target_tx_path = input('input target_tx_path (default: signed_tx_path) : ') or 'signed_tx_path'
    if not config.target_signed_tx_path:
        config.target_signed_tx_path = input('input target_tx_path (default: target_signed_tx_path) : ') or 'signed_tx_path'

    return config
