from configs.web3 import get_local_node_conn
from configs.postgres import get_pg_conn
from classes import Block, Transaction, TransactionReceipt, Log, Event

web3 = get_local_node_conn()
pg_conn = get_pg_conn()


def query_last_block(database_cursor, block_height):
    query = 'SELECT max(block_num) FROM sync.blocks;'
    database_cursor.execute(query)
    result = database_cursor.fetchall()
    if result[0][0] is None:
        return block_height - 1
    else:
        return result[0][0]


def extract_logs(contract, block_number):
    transfer_filter = contract.transfer['event_class'].createFilter(fromBlock=block_number, toBlock=block_number)
    daily_data_update_filter = contract.daily_data_update['event_class'].createFilter(fromBlock=block_number, toBlock=block_number)
    stake_start_filter = contract.stake_start['event_class'].createFilter(fromBlock=block_number, toBlock=block_number)
    stake_good_accounting_filter = contract.stake_good_accounting['event_class'].createFilter(fromBlock=block_number, toBlock=block_number)
    stake_end_filter = contract.stake_end['event_class'].createFilter(fromBlock=block_number, toBlock=block_number)
    share_rate_change_filter = contract.share_rate_change['event_class'].createFilter(fromBlock=block_number, toBlock=block_number)

    transfer_logs = transfer_filter.get_all_entries()
    daily_data_update_logs = daily_data_update_filter.get_all_entries()
    stake_start_logs = stake_start_filter.get_all_entries()
    stake_good_accounting_logs = stake_good_accounting_filter.get_all_entries()
    stake_end_logs = stake_end_filter.get_all_entries()
    share_rate_change_logs = share_rate_change_filter.get_all_entries()
    all_logs_dicts = {'Transfer': transfer_logs,
                      'DailyDataUpdate': daily_data_update_logs,
                      'StakeStart': stake_start_logs,
                      'StakeGoodAccounting': stake_good_accounting_logs,
                      'StakeEnd': stake_end_logs,
                      'ShareRateChange': share_rate_change_logs}

    return all_logs_dicts


def extract_indirect_txn_receipts(logs_dicts_dict):
    txn_receipt_events_dict = {}
    for event_key in logs_dicts_dict:
        txn_receipts_dict = {}
        for log_dict in logs_dicts_dict[event_key]:
            receipt_id = log_dict['transactionHash'].hex()+'_'+str(log_dict['logIndex'])
            if receipt_id not in txn_receipts_dict.keys():
                receipt = TransactionReceipt(web3.eth.get_transaction_receipt(log_dict['transactionHash']))
                txn_receipts_dict[receipt_id] = receipt
        txn_receipt_events_dict[event_key] = txn_receipts_dict
    return txn_receipt_events_dict


def append_txn_receipts(txn_list, txn_receipt_dict):
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
    transaction_dict = dict()
    for txn in transactions_list:
        transaction_dict[txn.txn_hash] = txn

    for txn_hash in txn_receipt_dict:
        if txn_hash not in transaction_dict.keys():
            txn = Transaction(web3.eth.get_transaction(txn_hash))
            transaction_dict[txn.txn_hash] = txn
    return transaction_dict


def transform_logs(logs_dict, indirect_txn_receipts_dict):
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


def extract_ethereum_data(contract):
    # LAST BLOCK PROCESSED
    with pg_conn:
        with pg_conn.cursor() as db_cursor:
            last_block_processed = query_last_block(database_cursor=db_cursor,
                                                    block_height=contract.deployed_block_height)
    next_block_number = last_block_processed + 1
    # BLOCK
    eth_block = Block(web3.eth.get_block(next_block_number, full_transactions=True))

    # DIRECT TRANSACTIONS
    transactions_list = [Transaction(transaction) for transaction in eth_block.transactions
                         if Transaction(transaction).to_address == contract.address]

    # EXTRACT LOGS
    logs_dict = extract_logs(contract=contract, block_number=next_block_number)

    # EXTRACT TXN RECEIPTS (for events)
    txn_receipts_dict_for_events = extract_indirect_txn_receipts(logs_dict)

    # APPEND TXN RECEIPTS
    txn_receipts_dict = append_txn_receipts(transactions_list, txn_receipts_dict_for_events)

    # APPEND TXN
    transactions_dict = append_transactions(transactions_list, txn_receipts_dict)

    # TRANSFORM LOGS
    transformed_logs_dict = transform_logs(logs_dict, txn_receipts_dict_for_events)

    # EXTRACT EVENTS
    events_dict = extract_events(transformed_logs_dict, contract)

    return eth_block, transactions_dict, events_dict, transformed_logs_dict, txn_receipts_dict
