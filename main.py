#!/usr/local/bin/python3.10

from extractions.subgraph import extract_subgraph_data
from extractions.ethereum import extract_ethereum_data
from classes import SmartContract
from configs.web3 import get_local_node_conn
from configs.postgres import get_pg_conn
from configs.contract import hex_contract_dict
from database import create_schemas_and_tables
from loads import begin_db_transaction, load_transactions, load_transfers, load_stakes, load_swaps,\
    load_global_variables, load_daily_data_updates, sync, commit_db_transaction

web3 = get_local_node_conn()
pg_conn = get_pg_conn()


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

    # EXTRACTION
    print('\nExtract...')
    block, transactions, events, logs, txn_receipts = extract_ethereum_data(contract=hex_contract)
    graphql_data = extract_subgraph_data(block_instance=block)

    # LOAD
    print('\nLoad...')
    with pg_conn:
        with pg_conn.cursor() as cursor:
            begin_db_transaction(database_cursor=cursor)
            load_transactions(database_cursor=cursor, block_instance=block,
                              txn_dict=transactions, txn_receipts_dict=txn_receipts, contract=hex_contract)
            load_transfers(database_cursor=cursor, event_dict=events)
            load_stakes(database_cursor=cursor, event_dict=events)
            load_daily_data_updates(database_cursor=cursor, event_dict=events, gql_dict=graphql_data)
            load_global_variables(database_cursor=cursor, gql_dict=graphql_data)
            load_swaps(database_cursor=cursor, gql_dict=graphql_data)
            sync(database_cursor=cursor, block_instance=block)
            commit_db_transaction(database_cursor=cursor)


if __name__ == '__main__':
    for i in range(10000):
        main()
