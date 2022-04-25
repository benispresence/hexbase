import json

from configs.config import get_pg_conn, get_infura_conn
from configs.hex_config import hex_abi, hex_contract_address, hex_contract_creation_block_height
from decode_contract import get_function_arguments
from utils import get_last_block_number_from_b_dwh, insert_into_pg

pg_conn = get_pg_conn()


def insert_hex_transactions(start_block_number, end_block_number):
    for block in range(start_block_number, end_block_number):
        print('Processing Block Number:',block)
        hex_txn_query = f"SELECT * " \
                        f"FROM dl_ethereum.transactions " \
                        f"WHERE to_address  = '{hex_contract_address}' " \
                        f"  AND blocknumber = '{block}'"

        column_names_hex_txn = "SELECT column_name " \
                               "FROM INFORMATION_SCHEMA.COLUMNS " \
                               "WHERE TABLE_SCHEMA = 'dl_ethereum' " \
                               "  AND TABLE_NAME   = 'transactions';"


        with pg_conn:
            with pg_conn.cursor() as cursor:
                cursor.execute(hex_txn_query)
                hex_transactions = cursor.fetchall()
                cursor.execute(column_names_hex_txn)
                column_names = cursor.fetchall()
                for txn in hex_transactions:
                    txn_dict = {}
                    for column, txn_element in zip(column_names, txn):
                        txn_dict[column[0]] = txn_element
                    function_called, arguments = get_function_arguments(hex_abi,hex_contract_address,txn_dict['input'])
                    txn_dict['function_called'] = function_called
                    arguments_json = json.loads(arguments)
                    dict_arguments = dict(arguments_json)
                    for counter in range(11):
                        dict_key = 'argument_' + str(counter + 1) + '_name'
                        dict_value = 'argument_' + str(counter + 1) + '_value'
                        txn_dict[dict_key] = 'none'
                        txn_dict[dict_value] = 'none'
                    for counter, (argument, value) in enumerate(dict_arguments.items()):
                        dict_key = 'argument_' + str(counter + 1) + '_name'
                        dict_value = 'argument_' + str(counter + 1) + '_value'
                        txn_dict[dict_key] = argument
                        txn_dict[dict_value] = value

                    print(txn_dict)

                    txn_columns = txn_dict.keys()
                    column_names_needed = []
                    for element in txn_columns:
                        if element not in ['blockhash', 'to_address', 'input', 'nonce', 'r', 's',
                                                  'transactionindex', 'type', 'v', 'value', 'accesslist', 'chainid']:
                            column_names_needed.append(element)
                    txn_values = [txn_dict[column] for column in column_names_needed ]
                    txn_all_columns = ','.join(column_names_needed)
                    txn_all_columns = txn_all_columns.replace("blocknumber", "block_number")
                    txn_all_columns = txn_all_columns.replace("hash", "transaction_hash")
                    txn_all_columns = txn_all_columns.replace("from_address", "address")
                    txn_all_columns = txn_all_columns.replace("gasprice", "gas_price")

                    insert_into_pg('hex', 'transactions', txn_all_columns, txn_values)
                    print('Transaction ' , txn_dict['hash'], 'was processed.')




if __name__ == '__main__':
    last_block_hex_transactions   = get_last_block_number_from_b_dwh('hex','transactions', 'block_number')
    last_block_dl_ethereum_blocks = get_last_block_number_from_b_dwh('dl_ethereum', 'blocks', 'number')

    if last_block_hex_transactions is None:
        start_block = hex_contract_creation_block_height
    elif hex_contract_creation_block_height > last_block_hex_transactions:
        start_block = hex_contract_creation_block_height
    else:
        start_block = last_block_hex_transactions + 1

    insert_hex_transactions(9049881, 9049881 + 1)
