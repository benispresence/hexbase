#!/usr/local/bin/python3.10
from line_profiler_pycharm import profile

from extractions.ethereum import extract_ethereum_data, query_last_block
from classes.uniswap_v2 import UniswapV2Contract
from configs.web3 import get_local_node_conn
from configs.postgres import get_pg_conn
from configs.contracts import uni_v2_contract_dict
from database_structure.uniswap_v2 import create_schemas_and_tables
from loads.database import begin_db_transaction, commit_db_transaction
from loads.transactions import load_transactions
from loads.syncs import sync
from loads.contracts.uniswap_v2 import load_swaps

web3 = get_local_node_conn()
pg_conn = get_pg_conn()


def etl_uniswap_v2():
    # CONFIGURATION
    print('\nConfiguration loading...')
    univ2_contract = UniswapV2Contract(name=uni_v2_contract_dict['name'],
                                       address=uni_v2_contract_dict['address'],
                                       abi=uni_v2_contract_dict['abi'],
                                       deployed_block_height=uni_v2_contract_dict['deployed_block_height'],
                                       web3_infura_connection=web3)

    # PREREQUISITES
    print('\nPreparing database...')
    create_schemas_and_tables()

    print('\nGet latest and next block number...')
    with pg_conn:
        with pg_conn.cursor() as db_cursor:
            last_block_processed = query_last_block(database_cursor=db_cursor,
                                                    block_height=univ2_contract.deployed_block_height,
                                                    table='uniswap_v2_blocks')
    next_block_number = last_block_processed + 1
    latest_block_number = web3.eth.block_number

    while next_block_number < latest_block_number:
        # EXTRACTION
        block, transactions, events, logs, txn_receipts = extract_ethereum_data(contract=univ2_contract,
                                                                                block_number=next_block_number)

        # LOAD
        with pg_conn:
            with pg_conn.cursor() as cursor:
                begin_db_transaction(database_cursor=cursor)
                load_transactions(database_cursor=cursor, block_instance=block, schema='uniswap_v2',
                                  table='transactions', txn_dict=transactions, txn_receipts_dict=txn_receipts,
                                  contract=univ2_contract)
                load_swaps(database_cursor=cursor, event_dict=events)
                sync(database_cursor=cursor, block_instance=block, table='uniswap_v2_blocks')
                commit_db_transaction(database_cursor=cursor)

        next_block_number += 1


if __name__ == '__main__':
    etl_uniswap_v2()
