from configs.postgres import get_pg_conn

# SCHEMAS
create_hex = f'CREATE SCHEMA IF NOT EXISTS hex;'
create_sync = 'CREATE SCHEMA IF NOT EXISTS sync;'

# TABLES
create_hex_transactions = f'CREATE TABLE IF NOT EXISTS hex.transactions(' \
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

create_hex_transfers = f'CREATE TABLE IF NOT EXISTS hex.transfers(' \
                            f'id                          CHAR(76) PRIMARY KEY,' \
                            f'address                     CHAR(42),' \
                            f'recipient_address           CHAR(42),' \
                            f'hex_amount                  NUMERIC(24,8),' \
                            f'transaction_hash            CHAR(66),' \
                            f'log_index                   INT,' \
                            f'CONSTRAINT fk_transaction ' \
                            f'FOREIGN KEY(transaction_hash) ' \
                            f'REFERENCES hex.transactions(transaction_hash)' \
                            f');'

create_hex_stakes = f'CREATE TABLE IF NOT EXISTS hex.stakes(' \
                            f'id                          BIGINT PRIMARY KEY,' \
                            f'address                     CHAR(42),' \
                            f'principal                   NUMERIC(24,8),' \
                            f't_shares                    NUMERIC(28,12),' \
                            f'payout                      NUMERIC(24,8),' \
                            f'penalty                     NUMERIC(24,8),' \
                            f'total_payout                NUMERIC(24,8),' \
                            f'yield                       NUMERIC(24,8),' \
                            f'good_accounted_payout       NUMERIC(24,8),' \
                            f'good_accounted_penalty      NUMERIC(24,8),' \
                            f'staked_days                 NUMERIC(4,0),' \
                            f'served_days                 NUMERIC(4,0),' \
                            f'created_at                  TIMESTAMP,' \
                            f'ended_at                    TIMESTAMP,' \
                            f'started_at                  DATE,' \
                            f'good_accounted_at           TIMESTAMP,' \
                            f'updated_t_share_rate        NUMERIC(10,1),' \
                            f'is_auto_stake               BOOLEAN,' \
                            f'previously_unlocked         BOOLEAN,' \
                            f'share_rate_changed          BOOLEAN,' \
                            f'good_accounted              BOOLEAN,' \
                            f'start_transaction_hash      CHAR(66),' \
                            f'end_transaction_hash        CHAR(66),' \
                            f'good_accounting_transaction_hash CHAR(66),' \
                            f'CONSTRAINT fk_transaction ' \
                            f'FOREIGN KEY(start_transaction_hash) ' \
                            f'REFERENCES hex.transactions(transaction_hash)' \
                            f');'

create_daily_data_updates = f'CREATE TABLE IF NOT EXISTS hex.daily_data_updates(' \
                            f'day                           INT PRIMARY KEY,' \
                            f'next_day                      INT,' \
                            f'transaction_hash              CHAR(66),' \
                            f'payout_per_t_share            NUMERIC,' \
                            f'payout                        NUMERIC(30,8),' \
                            f'shares                        NUMERIC(34,12),' \
                            f'CONSTRAINT fk_transaction ' \
                            f'FOREIGN KEY(transaction_hash) ' \
                            f'REFERENCES hex.transactions(transaction_hash)' \
                            f');'


create_global_variables = f'CREATE TABLE IF NOT EXISTS hex.global_variables(' \
                            f'block_number                  INT PRIMARY KEY,' \
                            f'total_supply                  NUMERIC(30,8),' \
                            f'circulating_supply            NUMERIC(30,8),' \
                            f'allocated_supply              NUMERIC(30,8),' \
                            f'locked_supply                 NUMERIC(30,8),' \
                            f'total_minted                  NUMERIC(30,8),' \
                            f't_share_rate                  NUMERIC(10,1),' \
                            f'total_t_shares_staked         NUMERIC(24,12)' \
                            f');'

create_swaps = f'CREATE TABLE IF NOT EXISTS hex.swaps(' \
                            f'id                            CHAR(76) PRIMARY KEY,' \
                            f'transaction_hash              CHAR(66),' \
                            f'sender                        CHAR(42),' \
                            f'recipient                     CHAR(42),' \
                            f'hex_amount                    NUMERIC(24,8),' \
                            f'usdc_amount                   NUMERIC(22,6),' \
                            f'uniswap                       CHAR(2),' \
                            f'log_index                     INT,' \
                            f'CONSTRAINT fk_transaction ' \
                            f'FOREIGN KEY(transaction_hash) ' \
                            f'REFERENCES hex.transactions(transaction_hash)' \
                            f');'


create_sync_blocks = 'CREATE TABLE IF NOT EXISTS sync.blocks(block_num INT PRIMARY KEY, synced BOOLEAN);'


check_sync = "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'sync';"


def create_schemas_and_tables():
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
                print('Created sync.blocks table')
                # CREATE DL ETHEREUM SCHEMA TABLES
                cursor.execute(create_hex)
                cursor.execute(create_hex_transactions)
                cursor.execute(create_hex_transfers)
                cursor.execute(create_hex_stakes)
                cursor.execute(create_daily_data_updates)
                cursor.execute(create_global_variables)
                cursor.execute(create_swaps)
                print('Created hex schema')
                print('Created hex.transactions table')
                print('Created hex.transfers table')
                print('Created hex.stakes table')
                print('Created hex.daily_data_updates table')
                print('Created hex.global_variables table')
                print('Created hex.swaps table')


if __name__ == '__main__':
    create_schemas_and_tables()
