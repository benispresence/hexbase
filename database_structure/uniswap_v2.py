from configs.postgres import get_pg_conn

# SCHEMAS
create_uniswap_v2 = f'CREATE SCHEMA IF NOT EXISTS uniswap_v2;'
create_sync = 'CREATE SCHEMA IF NOT EXISTS sync;'

# TABLES
create_uniswap_v2_transactions = \
                                f'CREATE TABLE IF NOT EXISTS uniswap_v2.transactions(' \
                                f'transaction_hash            CHAR(66)  PRIMARY KEY,' \
                                f'block_number                INT,' \
                                f'created_at                  TIMESTAMP,' \
                                f'block_gas_limit             INT,' \
                                f'block_gas_used              INT,' \
                                f'from_address                CHAR(42),' \
                                f'to_address                  CHAR(42),' \
                                f'transaction_fee             NUMERIC(30,18),' \
                                f'gas                         INT,' \
                                f'gas_used                    INT,' \
                                f'cumulative_gas_used         BIGINT,' \
                                f'gas_price                   NUMERIC(30,18),' \
                                f'effective_gas_price         NUMERIC(30,18),' \
                                f'nonce                       INT,' \
                                f'transaction_index           SMALLINT,' \
                                f'transaction_type            CHAR(3),' \
                                f'eth_amount                  NUMERIC(30,18),' \
                                f'function_called             CHAR(19),' \
                                f'arguments                   JSONB,' \
                                f'has_succeeded               BOOLEAN' \
                                f');'

create_swaps = f'CREATE TABLE IF NOT EXISTS uniswap_v2.swaps(' \
               f'id                             CHAR(76) PRIMARY KEY,' \
               f'hex_sold                       NUMERIC(24,8),' \
               f'usdc_sold                      NUMERIC(24,6),' \
               f'hex_bought                     NUMERIC(24,8),' \
               f'usdc_bought                    NUMERIC(24,6),' \
               f'address                        CHAR(42),' \
               f'transaction_hash               CHAR(66),' \
               f'log_index                      INT,' \
               f'CONSTRAINT fk_transaction ' \
               f'FOREIGN KEY(transaction_hash) ' \
               f'REFERENCES uniswap_v2.transactions(transaction_hash)' \
               f');'

create_sync_blocks = 'CREATE TABLE IF NOT EXISTS sync.uniswap_v2_blocks(block_num INT PRIMARY KEY, synced BOOLEAN);'

check_sync = "SELECT * FROM information_schema.tables WHERE table_name = 'uniswap_v2_blocks';"


def create_schemas_and_tables():
    """
    :return: Creates the necessary schemas and tables for the Uniswap V2 smart contract data
    within the hexbase database.
    """
    pg_conn = get_pg_conn()
    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(check_sync)
            result = cursor.fetchall()  # Check for sync table existing
            if len(result) == 0:
                # CREATE SYNC SCHEMA TABLES
                cursor.execute(create_sync)
                cursor.execute(create_sync_blocks)
                print('Created sync schema')
                print('Created sync.uniswap_v2_blocks table')
                # CREATE DL ETHEREUM SCHEMA TABLES
                cursor.execute(create_uniswap_v2)
                cursor.execute(create_uniswap_v2_transactions)
                cursor.execute(create_swaps)
                print('Created uniswap_v2 schema')
                print('Created uniswap_v2.transactions table')
                print('Created uniswap_v2.swaps table')


if __name__ == '__main__':
    create_schemas_and_tables()
