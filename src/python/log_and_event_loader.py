from hexbytes import HexBytes
from Crypto.Hash import keccak

from configs.config import get_infura_conn, get_pg_conn
from configs.smart_contract_configs import pulsedogecoin_contract_dict
from classes import SmartContract, Log, TransactionReceipt, Event
from utils import has_schema, has_table, create_table, create_schema, get_transactions_from_b_dwh, \
    begin_db_transaction, commit_db_transaction, insert_into_pg

pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_logs(txn_list):
    log_list = []
    for txn in txn_list:
        receipt = TransactionReceipt(web3.eth.get_transaction_receipt(HexBytes(txn)))
        for log in receipt.logs:
            log_list.append(Log(log))
    return log_list


def get_events(configuration, log_list):
    events_list = []
    contract = web3.eth.contract(address=configuration['address'], abi=configuration['abi'])
    for log in log_list:
        if configuration['name'] == 'pulsedogecoin':
            events_list.append(get_pulsedogecoin_event(log, contract))
    return events_list


def get_event_hash(bitstring):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(bitstring)
    keccak_hash = f'0x{keccak_hash.hexdigest()}'
    return keccak_hash


def get_pulsedogecoin_event(log, contract):  # todo put this into its seperate script and adding other smartcontracts
    log_event_hash = log.topics[0].hex()

    if log_event_hash == get_event_hash(b'Approval(address,address,uint256)'):
        event = Event(contract.events.Approval().processLog(log.log_dict))
    elif log_event_hash == get_event_hash(b'Transfer(address,address,uint256)'):
        event = Event(contract.events.Transfer().processLog(log.log_dict))
    elif log_event_hash == get_event_hash(b'Claim(address,uint256)'):
        event = Event(contract.events.Claim().processLog(log.log_dict))
    else:
        raise Exception(f'Event not found for transaction: {log.transaction_hash.hex()} '
                        f'with index {log.transaction_index}')
    return event


def process_log_and_event_data(configuration, log_list, event_list):
    schema = configuration['name']

    smart_contract = SmartContract(configuration['name'], configuration['address'],
                                   configuration['abi'], configuration['deployed_block_height'])

    if not has_schema(schema):
        create_schema(schema)
        print(f'The Schema named {schema} was created, because it did not exist')

    if not has_table('logs', schema):
        create_table(schema, 'logs')
        print(f'The Table named {schema}.logs was created, because it did not exist')

    if not has_table('events', schema):
        create_table(schema, 'events')
        print(f'The Table named {schema}.events was created, because it did not exist')

    with pg_conn:
        with pg_conn.cursor() as cursor:
            begin_db_transaction(cursor=cursor)
            update_log_table(cursor, smart_contract, log_list)
            update_event_table(cursor, smart_contract, event_list)
            commit_db_transaction(cursor=cursor)


def update_log_table(db_cursor, contract, log_list):
    for log in log_list:
        print(f'Processing Transaction Log for {log.transaction_hash.hex()} with index {log.transaction_index.hex()}')

        insert_into_pg(schema=contract.name,
                       table='logs',

                       columns=f'address, block_hash, block_number, data, log_index, removed, topics,'
                               f'transaction_hash, transaction_index',

                       values=(log.address, log.block_hash.hex(), log.block_number, log.data.hex(),
                               log.log_index, log.removed, log.topics, log.transaction_hash.hex(),
                               log.transaction_index),
                       cursor=db_cursor)

        print(f'Transaction Log for {log.transaction_hash.hex()} with index {log.transaction_index.hex()} was '
              f'processed')


def update_event_table(db_cursor, contract, event_list):
    for event in event_list:
        print(f'Processing Transaction Event for {event.transaction_hash.hex()}'
              f' with index {event.transaction_index.hex()}')

        insert_into_pg(schema=contract.name,
                       table='events',

                       columns=f'args, event, log_index, transaction_index, transaction_hash, address, block_hash,'
                               f'block_number',

                       values=(event.args, event.event, event.log_index, event.transaction_index,
                               event.transaction_hash, event.address, event.block_hash, event.block_number),

                       cursor=db_cursor)

        print(f'Transaction Event for {event.transaction_hash.hex()} with index {event.transaction_index.hex()} was '
              f'processed')


if __name__ == '__main__':
    config = pulsedogecoin_contract_dict  # todo make it universal

    transactions_data = get_transactions_from_b_dwh(config['name'])  # todo make it universal
    transaction_hash_list = [txn[0] for txn in transactions_data]

    logs = get_logs(transaction_hash_list)

    events = get_events(config, logs)

    process_log_and_event_data(config, logs, events)
