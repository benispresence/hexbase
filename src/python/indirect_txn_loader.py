from configs.config import get_pg_conn, get_infura_conn
from configs.smart_contract_configs import hex_contract_dict
from classes import SmartContract, Transaction, Block
from utils import get_indirect_transactions, check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def update_txn_table(cursor, block, transaction, smart_contract):
    print(f'Processing {transaction.txn_hash.hex()}.')

    insert_into_pg(schema=smart_contract.name,
                   table='indirect_transactions',

                   columns='hash, block_number, timestamp, block_gas_limit, block_gas_used, '
                           'total_transactions_in_block, from_address, to_address, '
                           'gas, gas_price, nonce, transaction_index, type, value',

                   values=(transaction.txn_hash.hex(), block.number, block.timestamp,
                           block.gas_limit, block.gas_used, len(block.get_transaction_list()),
                           transaction.from_address, transaction.to_address, transaction.gas,
                           transaction.gas_price, transaction.nonce, transaction.transaction_index,
                           transaction.type, transaction.value),
                   cursor=cursor)

    print(f'Transaction {transaction.txn_hash.hex()} was processed')


def process_transactions_data(configuration):
    smart_contract = SmartContract(configuration['name'], configuration['address'],
                                   configuration['abi'], configuration['deployed_block_height'])

    print(f'Smart Contract: {configuration["name"]}')

    check_db_table(schema=smart_contract.name, table='indirect_transactions')

    # GET indirect_transaction hashes
    txn = get_indirect_transactions(schema=smart_contract.name)
    # INSERT indirect transaction_hashes
    for tx in txn:
        with pg_conn:
            with pg_conn.cursor() as cursor:
                transaction = Transaction(web3.eth.get_transaction(tx[0]))
                block = Block(web3.eth.get_block(transaction.block_number, full_transactions=True))
                update_txn_table(cursor=cursor, block=block, transaction=transaction, smart_contract=smart_contract)
        print(f'The txn {transaction.txn_hash.hex()} was processed')


if __name__ == '__main__':
    process_transactions_data(hex_contract_dict)
