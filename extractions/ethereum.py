from configs.web3 import get_local_node_conn
from configs.postgres import get_pg_conn
from classes.ethereum import Block, Transaction, TransactionReceipt, Log, Event
from extractions.logs.hex import extract_logs as extract_hex_logs
from extractions.logs.uniswap_v2 import extract_logs as extract_univ2_logs

web3 = get_local_node_conn()
pg_conn = get_pg_conn()


def query_last_block(database_cursor, block_height, table):
    """
    Queries last block number which has been already processed in the load process for the relevant smart contract
    :param database_cursor: instance of pg database cursor
    :param block_height: int - block height of the smart contract
    :param table: str - table of the smart contract
    :return: int - block number
    """
    query = f'SELECT max(block_num) FROM sync.{table};'
    database_cursor.execute(query)
    result = database_cursor.fetchall()
    if result[0][0] is None:
        return block_height - 1
    else:
        return result[0][0]


def extract_indirect_txn_receipts(logs_dicts_dict):
    """
    Extracts all the transaction receipts from transactions which are indirectly triggering the relevant smart contract
    :param logs_dicts_dict: dictionary of "event"-dictionaries of logs
    :return: a dictionary of "event"-dictionaries of receipts
    """
    txn_receipt_events_dict = {}
    for event_key in logs_dicts_dict:
        # for each Event Type
        txn_receipts_dict = {}
        for log_dict in logs_dicts_dict[event_key]:
            # for each log
            receipt_id = log_dict['transactionHash'].hex()+'_'+str(log_dict['logIndex'])
            if receipt_id not in txn_receipts_dict.keys():
                receipt = TransactionReceipt(web3.eth.get_transaction_receipt(log_dict['transactionHash']))
                txn_receipts_dict[receipt_id] = receipt
        txn_receipt_events_dict[event_key] = txn_receipts_dict
    return txn_receipt_events_dict


def append_txn_receipts(txn_list, txn_receipt_dict):
    """
    Appends the "txn_receipt_dict" dictionary of "event"-dictionaries of receipts
    with transaction receipts of the direct transactions. The purpose is to include all the transaction
    receipts in one dictionary -> "txn_receipts"
    :param txn_list: list - transactions
    :param txn_receipt_dict: dictionary of "event"-dictionaries of receipts
    :return: dict of all transaction receipts
    """
    txn_receipts = dict()

    for event in txn_receipt_dict:
        for receipt_id in txn_receipt_dict[event]:
            receipt = txn_receipt_dict[event][receipt_id]
            txn_receipts[receipt.transaction_hash] = receipt

    for txn in txn_list:
        if txn.txn_hash not in txn_receipts.keys():
            receipt = TransactionReceipt(web3.eth.get_transaction_receipt(txn.txn_hash))
            txn_receipts[receipt.transaction_hash] = receipt

    return txn_receipts


def append_transactions(transactions_list, txn_receipt_dict):
    """
    Add indirect txn to the list of direct txn. Indirect txn are txn that emit an event
    while not calling the relevant smart contract directly
    :param transactions_list: list of direct transactions
    :param txn_receipt_dict: dict of all transaction receipts
    :return: dict of all transactions
    """
    transaction_dict = dict()
    for txn in transactions_list:
        transaction_dict[txn.txn_hash] = txn

    for txn_hash in txn_receipt_dict:
        if txn_hash not in transaction_dict.keys():
            txn = Transaction(web3.eth.get_transaction(txn_hash))
            transaction_dict[txn.txn_hash] = txn
    return transaction_dict


def transform_logs(logs_dict, indirect_txn_receipts_dict):
    """
    Transforms the dict of all logs is structured to the appropriate format.
    :param logs_dict: dict of logs
    :param indirect_txn_receipts_dict: dict of indirect txn receipts
    :return: dict of logs
    """
    new_logs_dict = {}
    for event_key in logs_dict:
        new_logs_list = {}
        for receipt_id in indirect_txn_receipts_dict[event_key]:
            receipt = indirect_txn_receipts_dict[event_key][receipt_id]
            log_index = receipt_id.split('_')[1]
            for log_dict in logs_dict[event_key]:
                for receipt_log in receipt.logs:
                    if log_dict['logIndex'] == receipt_log['logIndex'] == int(log_index) \
                            and log_dict['transactionHash'] == receipt_log['transactionHash']:
                        new_logs_list[receipt_id] = Log(receipt_log)
        new_logs_dict[event_key] = new_logs_list
    return new_logs_dict


def extract_events(logs_dict, contract):
    """
    Extracts all the events from the logs and places them into a dict
    :param logs_dict: dict of logs
    :param contract: The relevant smart contract instance. (class SmartContract)
    :return: dict of all events
    """
    event_type_dict = dict()
    for event_key in logs_dict:
        events_dict = {}
        for log_id in logs_dict[event_key]:
            log = logs_dict[event_key][log_id]
            for event_instance in contract.events:
                if event_key == event_instance['event_name']:
                    events_dict[log_id] = Event(event_instance['event_object'].processLog(log.log_dict))
        event_type_dict[event_key] = events_dict
    return event_type_dict


def extract_ethereum_data(contract, block_number):
    """
    Extracts block, transaction, log and txn receipt data.
    Afterwards it transforms the data into appropriate dictionaries and returns them
    :param contract: The relevant smart contract instance. (class SmartContract)
    :param block_number: int of block number
    :return: Block(), dict of txn, dict of events, dict of logs, dict of txn receipts
    """
    # BLOCK
    eth_block = Block(web3.eth.get_block(block_number, full_transactions=True))

    # DIRECT TRANSACTIONS
    transactions_list = [Transaction(transaction) for transaction in eth_block.transactions
                         if Transaction(transaction).to_address == contract.address]

    # EXTRACT LOGS
    if contract.name == 'hex':
        logs_dict = extract_hex_logs(contract=contract, block_number=block_number)
    elif contract.name == 'uniswap_v2':
        logs_dict = extract_univ2_logs(contract=contract, block_number=block_number)
    else:
        logs_dict = {'default': dict()}

    # EXTRACT INDIRECT TXN RECEIPTS (for events)
    txn_receipts_dict_for_events = extract_indirect_txn_receipts(logs_dict)

    # APPEND DIRECT TXN RECEIPTS
    txn_receipts_dict = append_txn_receipts(transactions_list, txn_receipts_dict_for_events)

    # APPEND INDIRECT TXN
    transactions_dict = append_transactions(transactions_list, txn_receipts_dict)

    # TRANSFORM LOGS
    transformed_logs_dict = transform_logs(logs_dict, txn_receipts_dict_for_events)

    # EXTRACT EVENTS
    events_dict = extract_events(transformed_logs_dict, contract)

    return eth_block, transactions_dict, events_dict, transformed_logs_dict, txn_receipts_dict
