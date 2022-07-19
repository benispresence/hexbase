import json

from configs.config import get_infura_conn, get_pg_conn
from configs.smart_contract_configs import hex_contract_dict
from classes import SmartContract, Log, TransactionReceipt, Event
from utils import begin_db_transaction, commit_db_transaction, insert_into_pg, get_start_block, check_db_table


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_logs(event_class, start_block, end_block):
    log_list = []
    attempts = 0
    while attempts < 4:
        try:
            web3_filter = event_class.createFilter(fromBlock=start_block, toBlock=end_block)
            print(f'Web3 Filter is: {web3_filter}')
            log_entries = web3_filter.get_all_entries()
            for log in log_entries:
                receipt = TransactionReceipt(web3.eth.get_transaction_receipt(log['transactionHash']))
                # txn_receipts have more information of the logs, which are necessary
                for receipt_log in receipt.logs:
                    if log['logIndex'] == receipt_log['logIndex']:
                        log_list.append(Log(receipt_log))
            return log_list
        except ValueError as error:
            print(error)
            attempts += 1
            print(f'Trying again to get log entries. Attempt No. : {attempts}')
    raise Exception(f'Too many attempts to get log entries.')


def get_events(event_object, log_list):
    events_list = []
    for log in log_list:
        events_list.append(Event(event_object.processLog(log.log_dict)))
    return events_list


def update_log_and_event_data(smart_contract, log_list, event_list):
    with pg_conn:
        with pg_conn.cursor() as cursor:
            begin_db_transaction(cursor=cursor)
            update_log_table(cursor, smart_contract, log_list)
            update_event_table(cursor, smart_contract, event_list)
            commit_db_transaction(cursor=cursor)


def update_log_table(db_cursor, contract, log_list):
    for log in log_list:
        print(f'Processing Transaction Log for {log.transaction_hash.hex()} with log index {log.log_index}')

        insert_into_pg(schema=contract.name,
                       table='logs',

                       columns=f'address, block_hash, block_number, data, log_index, removed, topics,'
                               f'transaction_hash, transaction_index',

                       values=(log.address, log.block_hash.hex(), log.block_number, log.data,
                               log.log_index, log.removed, ";".join([topic.hex() for topic in log.topics]),
                               log.transaction_hash.hex(), log.transaction_index),
                       cursor=db_cursor)

        print(f'Transaction Log for {log.transaction_hash.hex()} with log index {log.log_index} was '
              f'processed')


def update_event_table(db_cursor, contract, event_list):
    for event in event_list:
        print(f'Processing Transaction Event for {event.transaction_hash.hex()}'
              f' with log index {event.log_index}')

        event_args_dict = dict(event.args)
        for key in event_args_dict:
            if type(event_args_dict[key]) is bytes:
                event_args_dict[key] = web3.toHex(event_args_dict[key])

        insert_into_pg(schema=contract.name,
                       table='events',

                       columns=f'args, event, log_index, transaction_index, transaction_hash, address, block_hash,'
                               f'block_number',

                       values=(json.dumps(event_args_dict), event.event, event.log_index, event.transaction_index,
                               event.transaction_hash.hex(), event.address, event.block_hash.hex(), event.block_number),

                       cursor=db_cursor)

        print(f'Transaction Event for {event.transaction_hash.hex()} with log index {event.log_index} was '
              f'processed')


def process_transactions_data(configuration):
    smart_contract = SmartContract(configuration['name'], configuration['address'],
                                   configuration['abi'], configuration['deployed_block_height'])

    print(f'Smart Contract {configuration["name"]}')

    check_db_table(schema=smart_contract.name, table='logs')
    check_db_table(schema=smart_contract.name, table='events')

    # EVENT TYPE
    for event in smart_contract.events:
        print(f'Processing Events of type {event["event_name"]}')

        start_block_num = 1 + get_start_block(contract=smart_contract, table='events', event_type=event['event_name'])
        current_block_num = web3.eth.block_number
        print(f'Current Block in Events Table is {current_block_num} for Event Type {event["event_name"]}')

        # BLOCKS
        for block_number in range(start_block_num, current_block_num):
            # LOGS & EVENTS
            logs = get_logs(event['event_class'], block_number, block_number)
            events = get_events(event['event_object'], logs)
            update_log_and_event_data(smart_contract, logs, events)

            print(f'Block number {block_number} was processed')


if __name__ == '__main__':
    process_transactions_data(hex_contract_dict)
