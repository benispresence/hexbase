from configs.config import get_infura_conn, get_pg_conn
from configs.smart_contract_configs import all_contract_configs
from classes import SmartContract, Block, Transaction
from utils import has_schema, has_table, create_table, create_schema, \
    get_start_block, insert_into_pg, begin_db_transaction, commit_db_transaction

pg_conn = get_pg_conn()
web3 = get_infura_conn()


def update_txn_table(cursor, block, transaction, smart_contract):
    print(f'Processing {transaction.txn_hash.hex()}.')

    function_called, arguments = \
        transaction.get_function_arguments(sample_abi=smart_contract.abi,
                                           contract_address=smart_contract.address)

    insert_into_pg(schema=smart_contract.name,
                   table='transactions',

                   columns='hash, block_number, timestamp, block_gas_limit, block_gas_used, '
                           'total_transactions_in_block, from_address, to_address, '
                           'gas, gas_price, nonce, transaction_index, type, value, '
                           'function_called, '
                           'arguments',

                   values=(transaction.txn_hash.hex(), block.number, block.timestamp,
                           block.gas_limit, block.gas_used, len(block.get_transaction_list()),
                           transaction.from_address, transaction.to_address, transaction.gas,
                           transaction.gas_price, transaction.nonce, transaction.transaction_index,
                           transaction.type, transaction.value, function_called, arguments),
                   cursor=cursor)

    print(f'Transaction {transaction.txn_hash.hex()} was processed')


def update_tables(config):

    smart_contract = SmartContract(config['name'], config['address'],
                                   config['abi'], config['deployed_block_height'])
    start_block_num = 1 + get_start_block(smart_contract)
    current_block_num = web3.eth.block_number

    print(f'Current Block {current_block_num}')

    # BLOCKS
    for block_number in range(start_block_num, current_block_num):
        block = Block(web3.eth.get_block(block_number, full_transactions=True))

        with pg_conn:
            with pg_conn.cursor() as cursor:
                begin_db_transaction(cursor=cursor)

                # TRANSACTIONS
                for transaction in block.transactions:
                    transaction = Transaction(transaction)
                    if transaction.to_address == smart_contract.address:

                        update_txn_table(cursor=cursor, block=block, transaction=transaction,
                                         smart_contract=smart_contract)

                        # todo update_logs_table
                        # todo update_events_table

                commit_db_transaction(cursor=cursor)

        print(f'The block number {block_number} was processed')


def process_smart_contract_data(config):
    schema = config['name']

    # SCHEMA
    if not has_schema(schema):
        create_schema(schema)
        print(f'The Schema named {schema} was created, because it did not exist')

    # TABLES
    if not has_table('transactions', schema):
        create_table(schema, 'transactions')
        print(f'The Table named {schema}.transactions was created, because it did not exist')

    if not has_table('logs', schema):
        create_table(schema, 'logs')
        print(f'The Table named {schema}.logs was created, because it did not exist')

    if not has_table('events', schema):
        create_table(schema, 'events')
        print(f'The Table named {schema}.events was created, because it did not exist')

    update_tables(config)


if __name__ == '__main__':
    for config in all_contract_configs:
        print(config['name'])
        process_smart_contract_data(config)