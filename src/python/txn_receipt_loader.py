from configs.config import get_pg_conn, get_infura_conn
from configs.smart_contract_configs import hex_contract_dict
from classes import SmartContract, TransactionReceipt
from utils import get_missing_transaction_receipts, check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def update_txn_table(cursor, transaction_receipt, smart_contract, table):
    print(f'Processing {transaction_receipt.transaction_hash.hex()}.')

    insert_into_pg(schema=smart_contract.name,
                   table=table,

                   columns='block_hash, block_number, cumulative_gas_used, effective_gas_price, '
                           'from_address, gas_used, status, to_address, transaction_hash,'
                           'transaction_index, type',

                   values=(transaction_receipt.block_hash.hex(), transaction_receipt.block_number,
                           transaction_receipt.cumulative_gas_used,
                           transaction_receipt.effective_gas_price, transaction_receipt.from_address,
                           transaction_receipt.gas_used, transaction_receipt.status, transaction_receipt.to_address,
                           transaction_receipt.transaction_hash.hex(), transaction_receipt.transaction_index,
                           transaction_receipt.type),
                   cursor=cursor)

    print(f'Transaction Receipt {transaction_receipt.transaction_hash.hex()} was processed')


def process_transactions_data(configuration):
    smart_contract = SmartContract(configuration['name'], configuration['address'],
                                   configuration['abi'], configuration['deployed_block_height'])

    print(f'Smart Contract: {configuration["name"]}')

    check_db_table(schema=smart_contract.name, table='indirect_transaction_receipts')
    check_db_table(schema=smart_contract.name, table='transaction_receipts')

    # GET TRANSACTION RECEIPT HASHES
    txn = get_missing_transaction_receipts(schema=smart_contract.name, indirect=False)
    indirect_txn = get_missing_transaction_receipts(schema=smart_contract.name, indirect=True)

    # INSERT TRANSACTION RECEIPTS
    print(f'Direct Transaction Receipts are getting processed')
    for tx in txn:
        with pg_conn:
            with pg_conn.cursor() as cursor:
                txn_receipt = TransactionReceipt(web3.eth.get_transaction_receipt(tx[0]))
                update_txn_table(cursor=cursor, transaction_receipt=txn_receipt,
                                 smart_contract=smart_contract, table='transaction_receipts')

    # INSERT TRANSACTION RECEIPTS
    print(f'Direct Indirect Transaction Receipts are getting processed')
    for tx in indirect_txn:
        with pg_conn:
            with pg_conn.cursor() as cursor:
                txn_receipt = TransactionReceipt(web3.eth.get_transaction_receipt(tx[0]))
                update_txn_table(cursor=cursor, transaction_receipt=txn_receipt,
                                 smart_contract=smart_contract, table='indirect_transaction_receipts')


if __name__ == '__main__':
    process_transactions_data(hex_contract_dict)
