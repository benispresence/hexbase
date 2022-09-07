from utils.decode_contract import decode_contract_input


class SmartContract:
    def __init__(self, name, address, abi, deployed_block_height, web3_infura_connection):
        self.name = name
        self.address = address
        self.abi = abi
        self.deployed_block_height = deployed_block_height
        self.web3_contract_interface = web3_infura_connection.eth.contract(address=address, abi=abi)

        # web3 events
        self.transfer = dict(event_name='Transfer',
                             event_class=self.web3_contract_interface.events.Transfer,
                             event_object=self.web3_contract_interface.events.Transfer())
        self.daily_data_update = dict(event_name='DailyDataUpdate',
                                      event_class=self.web3_contract_interface.events.DailyDataUpdate,
                                      event_object=self.web3_contract_interface.events.DailyDataUpdate())
        self.stake_start = dict(event_name='StakeStart',
                                event_class=self.web3_contract_interface.events.StakeStart,
                                event_object=self.web3_contract_interface.events.StakeStart())
        self.stake_good_accounting = dict(event_name='StakeGoodAccounting',
                                          event_class=self.web3_contract_interface.events.StakeGoodAccounting,
                                          event_object=self.web3_contract_interface.events.StakeGoodAccounting())
        self.stake_end = dict(event_name='StakeEnd',
                              event_class=self.web3_contract_interface.events.StakeEnd,
                              event_object=self.web3_contract_interface.events.StakeEnd())
        self.share_rate_change = dict(event_name='ShareRateChange',
                                      event_class=self.web3_contract_interface.events.ShareRateChange,
                                      event_object=self.web3_contract_interface.events.ShareRateChange())
        self.events = [self.transfer, self.stake_end, self.stake_start, self.stake_good_accounting,
                       self.share_rate_change, self.daily_data_update]


class Block:
    def __init__(self, block_dict):
        self.number = block_dict['number']
        self.difficulty = block_dict['difficulty']
        self.extra_data = block_dict['extraData']
        self.gas_limit = block_dict['gasLimit']
        self.gas_used = block_dict['gasUsed']
        self.hash = block_dict['hash']
        self.logs_bloom = block_dict['logsBloom']
        self.miner = block_dict['miner']
        self.mix_hash = block_dict['mixHash']
        self.nonce = block_dict['nonce']
        self.parent_hash = block_dict['parentHash']
        self.receipts_root = block_dict['receiptsRoot']
        self.sha3_uncles = block_dict['sha3Uncles']
        self.size = block_dict['size']
        self.state_root = block_dict['stateRoot']
        self.timestamp = block_dict['timestamp']
        self.total_difficulty = block_dict['totalDifficulty']
        self.transactions = block_dict['transactions']
        self.transactions_root = block_dict['transactionsRoot']
        self.uncles = block_dict['uncles']

    def get_transaction_list(self):
        txn_list = []
        for txn_dict in self.transactions:
            txn_list = txn_dict['hash']
        return txn_list


class Transaction:
    def __init__(self, txn_dict):
        self.txn_hash = txn_dict['hash']
        self.block_hash = txn_dict['blockHash']
        self.block_number = txn_dict['blockNumber']
        self.from_address = txn_dict['from']
        self.gas = txn_dict['gas']
        self.gas_price = txn_dict['gasPrice']
        self.input = txn_dict['input']
        self.nonce = txn_dict['nonce']
        self.r = txn_dict['r']
        self.s = txn_dict['s']
        self.to_address = txn_dict['to']
        self.transaction_index = txn_dict['transactionIndex']
        self.type = txn_dict['type']
        self.v = txn_dict['v']
        self.value = txn_dict['value']

        self.txn_dict = txn_dict
        self.method_id = txn_dict['input'][:10]

    def get_function_arguments(self, abi, address, web3_contract):
        return decode_contract_input(abi, address, self.input, web3_contract)


class TransactionReceipt:
    def __init__(self, receipt_dict):
        self.receipt_dict = receipt_dict
        self.block_hash = receipt_dict['blockHash']
        self.block_number = receipt_dict['blockNumber']
        self.contract_address = receipt_dict['contractAddress']
        self.cumulative_gas_used = receipt_dict['cumulativeGasUsed']
        self.effective_gas_price = receipt_dict['effectiveGasPrice']
        self.from_address = receipt_dict['from']
        self.gas_used = receipt_dict['gasUsed']
        self.logs = receipt_dict['logs']
        self.logs_bloom = receipt_dict['logsBloom']
        self.status = receipt_dict['status']
        self.to_address = receipt_dict['to']
        self.transaction_hash = receipt_dict['transactionHash']
        self.transaction_index = receipt_dict['transactionIndex']
        self.type = receipt_dict['type']


class Log:
    def __init__(self, log_dict):
        self.log_dict = log_dict
        self.address = log_dict['address']
        self.block_hash = log_dict['blockHash']
        self.block_number = log_dict['blockNumber']
        self.data = log_dict['data']
        self.log_index = log_dict['logIndex']
        self.removed = log_dict['removed']
        self.topics = log_dict['topics']
        self.transaction_hash = log_dict['transactionHash']
        self.transaction_index = log_dict['transactionIndex']


class Event:
    def __init__(self, event_dict):
        self.event_dict = event_dict
        self.args = event_dict['args']
        self.event = event_dict['event']
        self.log_index = event_dict['logIndex']
        self.transaction_index = event_dict['transactionIndex']
        self.transaction_hash = event_dict['transactionHash']
        self.address = event_dict['address']
        self.block_hash = event_dict['blockHash']
        self.block_number = event_dict['blockNumber']

    def __str__(self):
        return f'Address: {self.address} \n' \
               f'Block Number: {self.block_number} \n' \
               f'Block Hash: {self.block_hash.hex()} \n' \
               f'Args: {self.args} \n' \
               f'Log Index: {self.log_index} \n' \
               f'Event: {self.event} \n' \
               f'Transaction Hash: {self.transaction_hash.hex()} \n' \
               f'Transaction Index: {self.transaction_index}'
