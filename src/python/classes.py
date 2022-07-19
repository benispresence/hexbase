from decode_contract import get_function_arguments
from configs.config import get_infura_conn

web3 = get_infura_conn()


class SmartContract:
    def __init__(self, name, address, abi, deployed_block_height):
        self.name = name
        self.address = address
        self.abi = abi
        self.deployed_block_height = deployed_block_height
        self.web3_contract_interface = web3.eth.contract(address=address, abi=abi)

        # web3 event classes and objects
        if self.name == 'pulsedogecoin':
            self.transfer = dict(event_name='Transfer',
                                 event_class=self.web3_contract_interface.events.Transfer,
                                 event_object=self.web3_contract_interface.events.Transfer())
            self.approval = dict(event_name='Approval',
                                 event_class=self.web3_contract_interface.events.Approval,
                                 event_object=self.web3_contract_interface.events.Approval())
            self.claim = dict(event_name='Claim',
                              event_class=self.web3_contract_interface.events.Claim,
                              event_object=self.web3_contract_interface.events.Claim())
            self.events = [self.transfer, self.approval, self.claim]
        elif self.name == 'hex':
            self.transfer = dict(event_name='Transfer',
                                 event_class=self.web3_contract_interface.events.Transfer,
                                 event_object=self.web3_contract_interface.events.Transfer())
            self.approval = dict(event_name='Approval',
                                 event_class=self.web3_contract_interface.events.Approval,
                                 event_object=self.web3_contract_interface.events.Approval())
            self.x_f_lobby_enter = dict(event_name='XfLobbyEnter',
                                        event_class=self.web3_contract_interface.events.XfLobbyEnter,
                                        event_object=self.web3_contract_interface.events.XfLobbyEnter())
            self.x_f_lobby_exit = dict(event_name='XfLobbyExit',
                                       event_class=self.web3_contract_interface.events.XfLobbyExit,
                                       event_object=self.web3_contract_interface.events.XfLobbyExit())
            self.daily_data_update = dict(event_name='DailyDataUpdate',
                                          event_class=self.web3_contract_interface.events.DailyDataUpdate,
                                          event_object=self.web3_contract_interface.events.DailyDataUpdate())
            self.claim = dict(event_name='Claim',
                              event_class=self.web3_contract_interface.events.Claim,
                              event_object=self.web3_contract_interface.events.Claim())
            self.claim_assist = dict(event_name='ClaimAssist',
                                     event_class=self.web3_contract_interface.events.ClaimAssist,
                                     event_object=self.web3_contract_interface.events.ClaimAssist())
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
            self.events = [self.claim, self.transfer, self.stake_end, self.stake_start, self.approval,
                           self.x_f_lobby_enter, self.x_f_lobby_exit, self.daily_data_update,  self.claim_assist,
                           self.stake_good_accounting,  self.share_rate_change]
        elif self.name == 'hedron':
            self.transfer = dict(event_name='Transfer',
                                 event_class=self.web3_contract_interface.events.Transfer,
                                 event_object=self.web3_contract_interface.events.Transfer())
            self.approval = dict(event_name='Approval',
                                 event_class=self.web3_contract_interface.events.Approval,
                                 event_object=self.web3_contract_interface.events.Approval())
            self.claim = dict(event_name='Claim',
                              event_class=self.web3_contract_interface.events.Claim,
                              event_object=self.web3_contract_interface.events.Claim())
            self.loan_end = dict(event_name='LoanEnd',
                                 event_class=self.web3_contract_interface.events.LoanEnd,
                                 event_object=self.web3_contract_interface.events.LoanEnd())
            self.loan_liquidate_bid = dict(event_name='LoanLiquidateBid',
                                           event_class=self.web3_contract_interface.events.LoanLiquidateBid,
                                           event_object=self.web3_contract_interface.events.LoanLiquidateBid())
            self.loan_liquidate_exit = dict(event_name='LoanLiquidateExit',
                                            event_class=self.web3_contract_interface.events.LoanLiquidateExit,
                                            event_object=self.web3_contract_interface.events.LoanLiquidateExit())
            self.loan_liquidate_start = dict(event_name='LoanLiquidateStart',
                                             event_class=self.web3_contract_interface.events.LoanLiquidateStart,
                                             event_object=self.web3_contract_interface.events.LoanLiquidateStart())
            self.loan_payment = dict(event_name='LoanPayment',
                                     event_class=self.web3_contract_interface.events.LoanPayment,
                                     event_object=self.web3_contract_interface.events.LoanPayment())
            self.loan_start = dict(event_name='LoanStart',
                                   event_class=self.web3_contract_interface.events.LoanStart,
                                   event_object=self.web3_contract_interface.events.LoanStart())
            self.mint = dict(event_name='Mint',
                             event_class=self.web3_contract_interface.events.Mint,
                             event_object=self.web3_contract_interface.events.Mint())
            self.events = [self.transfer, self.approval, self.claim,
                           self.loan_end, self.loan_liquidate_bid, self.loan_liquidate_exit, self.loan_liquidate_start,
                           self.loan_payment, self.loan_start, self.mint]
        elif self.name == 'hex_stake_instance':
            self.transfer = dict(event_name='Transfer',
                                 event_class=self.web3_contract_interface.events.Transfer,
                                 event_object=self.web3_contract_interface.events.Transfer())
            self.approval = dict(event_name='Approval',
                                 event_class=self.web3_contract_interface.events.Approval,
                                 event_object=self.web3_contract_interface.events.Approval())
            self.approval_for_all = dict(event_name='ApprovalForAll',
                                         event_class=self.web3_contract_interface.events.ApprovalForAll,
                                         event_object=self.web3_contract_interface.events.ApprovalForAll())
            self.royalties_set = dict(event_name='RoyaltiesSet',
                                      event_class=self.web3_contract_interface.events.RoyaltiesSet,
                                      event_object=self.web3_contract_interface.events.RoyaltiesSet())
            self.hsi_start = dict(event_name='HSIStart',
                                  event_class=self.web3_contract_interface.events.HSIStart,
                                  event_object=self.web3_contract_interface.events.HSIStart())
            self.hsi_end = dict(event_name='HSIEnd',
                                event_class=self.web3_contract_interface.events.HSIEnd,
                                event_object=self.web3_contract_interface.events.HSIEnd())
            self.hsi_transfer = dict(event_name='HSITransfer',
                                     event_class=self.web3_contract_interface.events.HSITransfer,
                                     event_object=self.web3_contract_interface.events.HSITransfer())
            self.hsi_tokenize = dict(event_name='HSITokenize',
                                     event_class=self.web3_contract_interface.events.HSITokenize,
                                     event_object=self.web3_contract_interface.events.HSITokenize())
            self.hsi_detokenize = dict(event_name='HSIDetokenize',
                                       event_class=self.web3_contract_interface.events.HSIDetokenize,
                                       event_object=self.web3_contract_interface.events.HSIDetokenize())
            self.events = [self.transfer, self.approval, self.approval_for_all,
                           self.royalties_set, self.hsi_start,
                           self.hsi_end, self.hsi_transfer, self.hsi_tokenize, self.hsi_detokenize]
        elif self.name == 'maximus':
            self.transfer = dict(event_name='Transfer',
                                 event_class=self.web3_contract_interface.events.Transfer,
                                 event_object=self.web3_contract_interface.events.Transfer())
            self.approval = dict(event_name='Approval',
                                 event_class=self.web3_contract_interface.events.Approval,
                                 event_object=self.web3_contract_interface.events.Approval())
            self.events = [self.transfer, self.approval]


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

    def get_function_arguments(self, sample_abi, contract_address):
        return get_function_arguments(sample_abi, contract_address, self.input)


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

    def __str__(self):
        return f'Address: {self.address} \n' \
               f'Block Number: {self.block_number} \n' \
               f'Block Hash: {self.block_hash.hex()} \n' \
               f'Data: {self.data} \n' \
               f'Log Index: {self.log_index} \n' \
               f'Removed: {self.removed} \n' \
               f'Topics: {",".join([topic.hex() for topic in self.topics])} \n' \
               f'Transaction Hash: {self.transaction_hash.hex()} \n' \
               f'Transaction Index: {self.transaction_index}'


class TransactionReceipt:
    def __init__(self, receipt_dict):
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
