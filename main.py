#!/usr/local/bin/python3.10
from line_profiler_pycharm import profile

from extractions.ethereum import extract_ethereum_data, query_last_block
from classes import SmartContract
from configs.web3 import get_local_node_conn
from configs.postgres import get_pg_conn
from configs.contract import hex_contract_dict
from database import create_schemas_and_tables
from loads import begin_db_transaction, load_transactions, load_transfers, load_stakes, \
     load_daily_data_updates, sync, commit_db_transaction

web3 = get_local_node_conn()
pg_conn = get_pg_conn()


@profile
def main():
    # CONFIGURATION
    print('\nConfiguration loading...')
    hex_contract = SmartContract(name=hex_contract_dict['name'],
                                 address=hex_contract_dict['address'],
                                 abi=hex_contract_dict['abi'],
                                 deployed_block_height=hex_contract_dict['deployed_block_height'],
                                 web3_infura_connection=web3)

    # PREREQUISITES
    print('\nPreparing database...')
    create_schemas_and_tables()

    print('\nGet latest and next block number...')
    with pg_conn:
        with pg_conn.cursor() as db_cursor:
            last_block_processed = query_last_block(database_cursor=db_cursor,
                                                    block_height=hex_contract.deployed_block_height)
    next_block_number = last_block_processed + 1
    latest_block_number = web3.eth.block_number

    while next_block_number < latest_block_number:
        # EXTRACTION
        block, transactions, events, logs, txn_receipts = extract_ethereum_data(contract=hex_contract,
                                                                                block_number=next_block_number)

        # LOAD
        with pg_conn:
            with pg_conn.cursor() as cursor:
                begin_db_transaction(database_cursor=cursor)
                load_transactions(database_cursor=cursor, block_instance=block,
                                  txn_dict=transactions, txn_receipts_dict=txn_receipts, contract=hex_contract)
                load_transfers(database_cursor=cursor, event_dict=events)
                load_stakes(database_cursor=cursor, event_dict=events)
                load_daily_data_updates(database_cursor=cursor, event_dict=events)
                sync(database_cursor=cursor, block_instance=block)
                commit_db_transaction(database_cursor=cursor)

        next_block_number += 1


if __name__ == '__main__':
    main()
