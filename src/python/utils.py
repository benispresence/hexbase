from configs.config import get_pg_conn

pg_conn = get_pg_conn()


def get_indirect_transactions(schema):
    get_transactions_sql_query = f'WITH base AS (' \
                                 f'     SELECT transaction_hash FROM {schema}.events ' \
                                 f'     EXCEPT ' \
                                 f'     SELECT t.hash FROM {schema}.transactions t' \
                                 f') ' \
                                 f'SELECT * FROM base ' \
                                 f'EXCEPT ' \
                                 f'SELECT it.hash FROM {schema}.indirect_transactions it'

    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(get_transactions_sql_query)
            transactions = cursor.fetchall()

    return transactions


def get_missing_transaction_receipts(schema, indirect=False):
    if indirect == True:
        table = 'indirect_transactions'
        comparison_table = 'indirect_transaction_receipts'
    else:
        table = 'transactions'
        comparison_table = 'transaction_receipts'
    get_transactions_sql_query = f'SELECT t.hash FROM {schema}.{table} t ' \
                                 f'EXCEPT ' \
                                 f'SELECT ct.transaction_hash FROM {schema}.{comparison_table} ct;'

    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(get_transactions_sql_query)
            transactions = cursor.fetchall()

    return transactions


def get_start_block(contract, table, event_type=None):
    """
    :return: Returns the last block number from one of the tables from the (B-DWH) Blockchain Data Warehouse.
    """
    column = 'block_number'
    schema = contract.name
    if event_type is not None:
        last_block_query = f"SELECT max({column} :: INT) FROM {schema}.{table} WHERE event = '{event_type}';"
    else:
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
    elif table_name == 'indirect_transactions':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.indirect_transactions(' \
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
                           f'value                       TEXT' \
                           f');'
    elif table_name == 'transaction_receipts':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.transaction_receipts(' \
                           f'transaction_hash            TEXT PRIMARY KEY,' \
                           f'block_number                TEXT,' \
                           f'block_hash                  TEXT,' \
                           f'cumulative_gas_used         TEXT,' \
                           f'effective_gas_price         TEXT,' \
                           f'gas_used                    TEXT,' \
                           f'from_address                TEXT,' \
                           f'to_address                  TEXT,' \
                           f'status                      TEXT,' \
                           f'transaction_index           TEXT,' \
                           f'type                        TEXT' \
                           f');'
    elif table_name == 'indirect_transaction_receipts':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.indirect_transaction_receipts(' \
                           f'transaction_hash            TEXT PRIMARY KEY,' \
                           f'block_number                TEXT,' \
                           f'block_hash                  TEXT,' \
                           f'cumulative_gas_used         TEXT,' \
                           f'effective_gas_price         TEXT,' \
                           f'gas_used                    TEXT,' \
                           f'from_address                TEXT,' \
                           f'to_address                  TEXT,' \
                           f'status                      TEXT,' \
                           f'transaction_index           TEXT,' \
                           f'type                        TEXT' \
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
                           f'ALTER TABLE {schema_name}.logs ADD PRIMARY KEY (transaction_hash, log_index);'
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
                           f'ALTER TABLE {schema_name}.events ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'stake_starts':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.stake_starts(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'staker_address             TEXT,' \
                           f'stake_id                   TEXT,' \
                           f'timestamp_stake_start      TEXT,' \
                           f'staked_hearts              TEXT,' \
                           f'stake_shares               TEXT,' \
                           f'staked_days                TEXT,' \
                           f'is_auto_stake              TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.stake_starts ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'stake_ends':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.stake_ends(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'staker_address             TEXT,' \
                           f'stake_id                   TEXT,' \
                           f'timestamp_stake_end        TEXT,' \
                           f'staked_hearts              TEXT,' \
                           f'stake_shares               TEXT,' \
                           f'payout                     TEXT,' \
                           f'penalty                    TEXT,' \
                           f'served_days                TEXT,' \
                           f'prev_unlocked              TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.stake_ends ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'claims':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.claims(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'btc_address                TEXT,' \
                           f'claim_to_address           TEXT,' \
                           f'referrer_address           TEXT,' \
                           f'created_at                 TEXT,' \
                           f'raw_satoshis               TEXT,' \
                           f'adjusted_satoshis          TEXT,' \
                           f'claim_flags                TEXT,' \
                           f'claimed_hearts             TEXT,' \
                           f'sender_address             TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.claims ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'transfers':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.transfers(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'from_address               TEXT,' \
                           f'to_address                 TEXT,' \
                           f'transfer_value              TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.transfers ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'share_rate_changes':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.share_rate_changes(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'stake_id                   TEXT,' \
                           f'created_at                 TEXT,' \
                           f'share_rate                 TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.share_rate_changes ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'stake_good_accountings':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.stake_good_accountings(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'staker_address             TEXT,' \
                           f'stake_id                   TEXT,' \
                           f'sender_address             TEXT,' \
                           f'created_at                 TEXT,' \
                           f'staked_hearts              TEXT,' \
                           f'stake_shares               TEXT,' \
                           f'payout                     TEXT,' \
                           f'penalty                    TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.stake_good_accountings ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'daily_data_updates' and schema_name == 'hex_events':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.daily_data_updates(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'staker_address             TEXT,' \
                           f'created_at                 TEXT,' \
                           f'begin_day                  TEXT,' \
                           f'end_day                    TEXT,' \
                           f'is_auto_update             TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.daily_data_updates ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'xf_lobby_exits':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.xf_lobby_exits(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'member_address             TEXT,' \
                           f'entry_id                   TEXT,' \
                           f'referrer_address           TEXT,' \
                           f'created_at                 TEXT,' \
                           f'xf_amount                  TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.xf_lobby_exits ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'xf_lobby_enters':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.xf_lobby_enters(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'member_address             TEXT,' \
                           f'entry_id                   TEXT,' \
                           f'referrer_address           TEXT,' \
                           f'created_at                 TEXT,' \
                           f'raw_amount                 TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.xf_lobby_enters ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'approvals':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.approvals(' \
                           f'log_index                  TEXT,' \
                           f'transaction_hash           TEXT,' \
                           f'owner_address              TEXT,' \
                           f'spender_address            TEXT,' \
                           f'approval_value             TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.approvals ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'daily_data_updates' and schema_name == 'dl_subgraph_hex':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.daily_data_updates(' \
                           f'end_day                    TEXT,' \
                           f'payout_per_t_share         TEXT,' \
                           f'payout                     TEXT,' \
                           f'shares                     TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.daily_data_updates ' \
                           f'ADD PRIMARY KEY (end_day);'
    elif table_name == 'global_info' and schema_name == 'dl_subgraph_hex':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.global_info(' \
                           f'transaction_hash                    TEXT,' \
                           f'hex_day                             TEXT,' \
                           f'block_number                        TEXT,' \
                           f'timestamp_block                     TEXT,' \
                           f'total_supply                        TEXT,' \
                           f'total_minted_hearts                 TEXT,' \
                           f'total_hearts_in_circulation         TEXT,' \
                           f'share_rate                          TEXT,' \
                           f'stake_shares_total                  TEXT,' \
                           f'stake_penalty_total                 TEXT,' \
                           f'latest_stake_id                     TEXT,' \
                           f'allocated_supply                    TEXT,' \
                           f'next_stake_shares_total             TEXT,' \
                           f'locked_hearts_total                 TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.global_info ' \
                           f'ADD PRIMARY KEY (block_number);'
    elif table_name == 'uniswap_v3' and schema_name == 'dl_subgraph_hex':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.uniswap_v3(' \
                           f'transaction_hash                    TEXT,' \
                           f'block_number                        TEXT,' \
                           f'created_at                          TEXT,' \
                           f'sender                              TEXT,' \
                           f'recipient                           TEXT,' \
                           f'token_0_id                          TEXT,' \
                           f'token_0_symbol                      TEXT,' \
                           f'token_0_amount                      TEXT,' \
                           f'token_1_id                          TEXT,' \
                           f'token_1_symbol                      TEXT,' \
                           f'token_1_amount                      TEXT,' \
                           f'log_index                           TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.uniswap_v3 ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    elif table_name == 'uniswap_v2' and schema_name == 'dl_subgraph_hex':
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.uniswap_v2(' \
                           f'transaction_hash                    TEXT,' \
                           f'block_number                        TEXT,' \
                           f'created_at                          TEXT,' \
                           f'sender                              TEXT,' \
                           f'recipient                           TEXT,' \
                           f'token_0_id                          TEXT,' \
                           f'token_0_symbol                      TEXT,' \
                           f'token_0_amount_in                   TEXT,' \
                           f'token_0_amount_out                  TEXT,' \
                           f'token_1_id                          TEXT,' \
                           f'token_1_symbol                      TEXT,' \
                           f'token_1_amount_in                   TEXT,' \
                           f'token_1_amount_out                  TEXT,' \
                           f'log_index                           TEXT' \
                           f');' \
                           f'ALTER TABLE {schema_name}.uniswap_v2 ' \
                           f'ADD PRIMARY KEY (transaction_hash, log_index);'
    else:
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {schema_name}.{table_name};'

    # CREATE TABLE
    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(create_table_sql)


def check_db_table(schema, table):
    # SCHEMA
    if not has_schema(schema):
        create_schema(schema)
        print(f'The Schema named {schema} was created, because it did not exist')

    # TABLE
    if not has_table(table, schema):
        create_table(schema, table)
        print(f'The Table named {schema}.{table} was created, because it did not exist')


def begin_db_transaction(cursor):
    begin = f'BEGIN;'
    cursor.execute(begin)


def commit_db_transaction(cursor):
    commit = f'COMMIT;'
    cursor.execute(commit)
