from configs.config import get_pg_conn

pg_conn = get_pg_conn()


def get_transactions_from_b_dwh(schema):
    get_transactions_sql_query = f'SELECT * FROM {schema}.transactions WHERE block_number :: INT > 14954138'

    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(get_transactions_sql_query)
            transactions = cursor.fetchall()

    return transactions


def get_last_block_number_from_b_dwh(schema, table, column):
    """
    :param schema: B-DWH Schema name (str)
    :param table: B-DWH table name (str)
    :param column: B-DWH block_number column name (str)
    :return: Returns the last block number from one of the tables from the (B-DWH) Blockchain Data Warehouse.
    """
    last_block_query = f'SELECT max({column} :: INT) FROM {schema}.{table};'

    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(last_block_query)
            block_num = curs.fetchall()

    return block_num[0][0]


def get_start_block(contract):
    """
    :return: Returns the last block number from one of the tables from the (B-DWH) Blockchain Data Warehouse.
    """
    column = 'block_number'
    schema = contract.name
    table = 'transactions'
    last_block_query = f'SELECT max({column} :: INT) FROM {schema}.{table};'

    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(last_block_query)
            block_num = curs.fetchall()

    if block_num[0][0] is None:
        return contract.deployed_block_height
    else:
        return block_num[0][0]


def insert_into_pg(schema, table, columns, values, cursor):
    # SQL
    insert_txn_statement = f'insert into {schema}.{table} ({columns}) values {tuple(values)};'

    # INSERT TO POSTGRES
    cursor.execute(insert_txn_statement)


def has_schema(schema_name):
    # SQL
    query_schemata = f'SELECT schema_name FROM information_schema.schemata;'

    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(query_schemata)
            schema_list = [schema[0] for schema in curs.fetchall()]
            if schema_name in schema_list:
                return True
            else:
                return False


def has_table(table_name, schema_name):
    # SQL
    query_tables = f"SELECT relname AS table " \
                     f"FROM pg_class, pg_namespace " \
                     f"WHERE relnamespace = pg_namespace.oid AND nspname = '{schema_name}' " \
                     f"AND relkind = 'r';"

    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(query_tables)
            table_list = [table[0] for table in curs.fetchall()]
            if table_name in table_list:
                return True
            else:
                return False


def create_schema(schema_name):
    # SQL
    create_schema_sql = f'CREATE SCHEMA IF NOT EXISTS {schema_name};'

    # INSERT TO POSTGRES
    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(create_schema_sql)


def create_table(schema_name, table_name):
    # SQL
    if table_name == 'transactions':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.transactions(' \
                            f'hash                        TEXT PRIMARY KEY,' \
                            f'block_number                TEXT,' \
                            f'timestamp                   TEXT,' \
                            f'block_gas_limit             TEXT,' \
                            f'block_gas_used              TEXT,' \
                            f'total_transactions_in_block TEXT,' \
                            f'from_address                TEXT,' \
                            f'to_address                  TEXT,' \
                            f'gas                         TEXT,' \
                            f'gas_price                   TEXT,' \
                            f'nonce                       TEXT,' \
                            f'transaction_index           TEXT,' \
                            f'type                        TEXT,' \
                            f'value                       TEXT,' \
                            f'function_called             TEXT,' \
                            f'arguments                   TEXT' \
                            f');'
    elif table_name == 'logs':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.logs(' \
                           f'address             TEXT,' \
                           f'block_hash          TEXT,' \
                           f'block_number        TEXT,' \
                           f'data                TEXT,' \
                           f'log_index           TEXT,' \
                           f'removed             TEXT,' \
                           f'topics              TEXT,' \
                           f'transaction_hash    TEXT,' \
                           f'transaction_index   TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.logs ADD PRIMARY KEY (transaction_hash, transaction_index);'
    elif table_name == 'events':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.events(' \
                           f'args                TEXT,' \
                           f'event               TEXT,' \
                           f'log_index           TEXT,' \
                           f'transaction_index   TEXT,' \
                           f'transaction_hash    TEXT,' \
                           f'address             TEXT,' \
                           f'block_hash          TEXT,' \
                           f'block_number        TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.events ADD PRIMARY KEY (transaction_hash, transaction_index);'
    else:
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.{table_name};'

    # CREATE TABLE
    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(create_table_sql)


def begin_db_transaction(cursor):
    begin = f'BEGIN;'
    cursor.execute(begin)


def commit_db_transaction(cursor):
    commit = f'COMMIT;'
    cursor.execute(commit)
