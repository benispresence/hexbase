from config import get_pg_conn, get_infura_conn
from hexbytes import HexBytes

pg_conn = get_pg_conn()
web3 = get_infura_conn()

latest_block_number = web3.eth.block_number


def insert_block_data(start_block, end_block):
    for block_num in range(start_block, end_block):
        # BLOCK DICT
        block_dict = web3.eth.get_block(block_num, full_transactions=True)
        # BLOCK COLUMNS
        columns = block_dict.keys()
        # BLOCK VALUES
        block_values = [block_dict[column] for column in columns if column != 'transactions']
        all_columns = ','.join(columns)
        new_values = []
        # TXN DICT LIST
        txn_dicts_list = block_dict['transactions']
        # INSERT TXNS AND RETURN TXNS LIST
        transactions_list = insert_transaction_data(txn_dicts_list)
        # ADD Transactions list to block values as the 19th value
        block_values.insert(18, transactions_list)

        for value in block_values:
            if isinstance(value, list):
                if not value:
                    new_values.append('')
                else:
                    transactions = ''
                    for txn in value:
                        if txn != value[-1]:
                            if isinstance(txn, HexBytes):
                                transactions = transactions + txn.hex() + '; '
                            else:
                                transactions = transactions + txn + '; '
                        else:
                            if isinstance(txn, HexBytes):
                                transactions = transactions + txn.hex()
                            else:
                                transactions = transactions + txn
                    new_values.append(transactions)
            elif isinstance(value, HexBytes):
                new_values.append(value.hex())
            else:
                new_values.append(value)

        insert_into_pg('blocks', all_columns, new_values)
        print(f'Block number {block_num} was processed.')


def insert_transaction_data(transactions):
    transactions_list = []

    for txn_dict in transactions:

        txn_columns = txn_dict.keys()
        txn_values = [txn_dict[column] for column in txn_columns]
        txn_all_columns = ','.join(txn_columns)
        txn_all_columns = txn_all_columns.replace("from", "from_address")
        txn_all_columns = txn_all_columns.replace('to', 'to_address')
        new_txn_values = []

        for txn_value in txn_values:
            if isinstance(txn_value, HexBytes):
                new_txn_values.append(txn_value.hex())
            elif isinstance(txn_value, list):
                access_list = '{'
                for attribute_dict in txn_value:
                    access_list += '{' + '{' + 'address' + ',' + attribute_dict['address'] + '}' + ','
                    keys = ''
                    for key in attribute_dict['storageKeys']:
                        keys += key
                        if key != attribute_dict['storageKeys'][-1]:
                            keys += ','
                    access_list += '{' + 'storageKeys' + ',' + '{' + keys + '}' + '}' + '}'
                    if attribute_dict != txn_value[-1]:
                        access_list += ','
                access_list += '}'
                new_txn_values.append(access_list)
            elif not txn_value:
                new_txn_values.append('')
            else:
                new_txn_values.append(txn_value)
        transactions_list.append(new_txn_values[5])

        insert_into_pg('transactions', txn_all_columns, new_txn_values)

    return transactions_list


def insert_into_pg(table, columns, values):
    # SQL
    insert_txn_statement = f'insert into dl_ethereum.{table} ({columns}) values {tuple(values)};'

    # INSERT TO POSTGRES
    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(insert_txn_statement)


def retrieve_last_block_num():
    # SQL
    last_block_query = f'SELECT max(number :: INT) FROM dl_ethereum.blocks;'

    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(last_block_query)
            block_num = curs.fetchall()
    return block_num[0][0]


if __name__ == '__main__':
    # Retrieve last block number in the BDWH Blockchain Data Warehouse
    start_block_num = retrieve_last_block_num()
    if start_block_num is None:
        start_block_num = 0
    else:
        start_block_num += 1
    end_block_num = start_block_num + 99999  # 100k requests per day
    insert_block_data(start_block_num, end_block_num)
