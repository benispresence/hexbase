from datetime import datetime, timedelta

from extractions.extract_subgraph import extract_subgraph_data
from extractions.extract_ethereum import extract_ethereum_data
from configs.config import get_infura_conn, get_pg_conn
from configs.smart_contract_configs import hex_contract_dict
from utils.create_tables import create_schemas_and_tables
from classes import SmartContract
from utils.infura_counter import counter_up

web3 = get_infura_conn()
pg_conn = get_pg_conn()


def begin_db_transaction(database_cursor):
    begin = f'BEGIN;'
    database_cursor.execute(begin)


def commit_db_transaction(database_cursor):
    commit = f'COMMIT;'
    database_cursor.execute(commit)


def insert_into_pg(schema, table, columns, values, database_cursor):
    # SQL
    insert_txn_statement = f'insert into {schema}.{table} ({columns}) values {tuple(values)};'

    # INSERT TO POSTGRES
    database_cursor.execute(insert_txn_statement)


def upsert_stakes_into_pg(schema, table, columns, values, database_cursor, primary_key_column,
                          payout_value, penalty_value, served_days_value, ended_at_value,
                          previously_unlocked_value, end_transaction_hash_value):
    # SQL
    upsert_txn_statement = f'INSERT INTO {schema}.{table} ({columns}) VALUES {tuple(values)} ' \
                           f'ON CONFLICT ({primary_key_column}) DO UPDATE SET ' \
                           f'payout = {payout_value},' \
                           f'penalty = {penalty_value},' \
                           f'total_payout = {schema}.{table}.principal + {payout_value} - {penalty_value},' \
                           f'yield = ({payout_value} - {penalty_value}) / {schema}.{table}.principal,' \
                           f'served_days = {served_days_value},' \
                           f"ended_at = '{ended_at_value}'," \
                           f'previously_unlocked = {previously_unlocked_value},' \
                           f"end_transaction_hash = '{end_transaction_hash_value}';"

    # INSERT TO POSTGRES
    database_cursor.execute(upsert_txn_statement)


def update_share_rate_changes(schema, table, stake_id, share_rate, database_cursor):
    # SQL
    update_txn_statement = f'UPDATE {schema}.{table} ' \
                           f'SET share_rate_changed = True,' \
                           f'    updated_t_share_rate = {share_rate} ' \
                           f'WHERE id = {stake_id};'

    # INSERT TO POSTGRES
    database_cursor.execute(update_txn_statement)


def update_good_accounting(schema, table, stake_id, payout, penalty, timestamp_at, txn_hash, database_cursor):
    # SQL
    update_txn_statement = f'UPDATE {schema}.{table} ' \
                           f'SET good_accounted_payout = {payout},' \
                           f'    good_accounted_penalty = {penalty},' \
                           f"    good_accounted_at = '{timestamp_at}'," \
                           f'    good_accounted = True,' \
                           f"    good_accounting_transaction_hash = '{txn_hash}'" \
                           f'WHERE id = {stake_id};'

    # INSERT TO POSTGRES
    database_cursor.execute(update_txn_statement)


def load_transactions(database_cursor, block_instance, txn_dict, txn_receipts_dict, contract):
    for txn_hash in txn_dict:
        transaction = txn_dict[txn_hash]
        receipt = txn_receipts_dict[txn_hash]
        function_called, arguments = \
            transaction.get_function_arguments(abi=contract.abi,
                                               address=contract.address,
                                               web3_contract=contract.web3_contract_interface)
        if function_called == 'Null':
            insert_into_pg(schema='hex',
                           table='transactions',
                           columns='transaction_hash,'
                                   'block_number,'
                                   'created_at,'
                                   'block_gas_limit,'
                                   'block_gas_used,'
                                   'from_address,'
                                   'to_address,'
                                   'transaction_fee,'
                                   'gas,'
                                   'gas_price,'
                                   'cumulative_gas_used,'
                                   'effective_gas_price,'
                                   'gas_used, '
                                   'nonce,'
                                   'transaction_index,'
                                   'transaction_type,'
                                   'eth_amount,'
                                   'has_succeeded',
                           values=(transaction.txn_hash.hex(),
                                   int(block_instance.number),
                                   datetime.utcfromtimestamp(int(block_instance.timestamp))
                                   .strftime("%Y-%m-%d %H:%M:%S.%f"),
                                   int(block_instance.gas_limit),
                                   int(block_instance.gas_used),
                                   transaction.from_address,
                                   transaction.to_address,
                                   float(receipt.effective_gas_price)/1000000000000000000*int(receipt.gas_used),
                                   int(transaction.gas),
                                   float(transaction.gas_price)/1000000000000000000,
                                   int(receipt.cumulative_gas_used),
                                   float(receipt.effective_gas_price)/1000000000000000000,
                                   int(receipt.gas_used),
                                   int(transaction.nonce),
                                   int(transaction.transaction_index),
                                   transaction.type,
                                   float(transaction.value)/1000000000000000000,
                                   bool(receipt.status)),
                           database_cursor=database_cursor)
        else:
            insert_into_pg(schema='hex',
                           table='transactions',
                           columns='transaction_hash,'
                                   'block_number,'
                                   'created_at,'
                                   'block_gas_limit,'
                                   'block_gas_used, '
                                   'from_address,'
                                   'to_address,'
                                   'transaction_fee,'
                                   'gas,'
                                   'gas_price,'
                                   'cumulative_gas_used,'
                                   'effective_gas_price,'
                                   'gas_used,'
                                   'nonce,'
                                   'transaction_index,'
                                   'transaction_type,'
                                   'eth_amount,'
                                   'function_called,'
                                   'arguments,'
                                   'has_succeeded',
                           values=(transaction.txn_hash.hex(),
                                   int(block_instance.number),
                                   datetime.utcfromtimestamp(int(block_instance.timestamp))
                                   .strftime("%Y-%m-%d %H:%M:%S.%f"),
                                   int(block_instance.gas_limit),
                                   int(block_instance.gas_used),
                                   transaction.from_address,
                                   transaction.to_address,
                                   float(receipt.effective_gas_price) / 1000000000000000000 * int(receipt.gas_used),
                                   int(transaction.gas),
                                   float(transaction.gas_price)/1000000000000000000,
                                   int(receipt.cumulative_gas_used),
                                   float(receipt.effective_gas_price)/1000000000000000000,
                                   int(receipt.gas_used),
                                   int(transaction.nonce),
                                   int(transaction.transaction_index),
                                   transaction.type,
                                   float(transaction.value)/1000000000000000000,
                                   function_called,
                                   str(arguments).replace("'", '"'),
                                   bool(receipt.status)),
                           database_cursor=database_cursor)
    print('Transactions processed')


def sync(database_cursor, block_instance):
    insert_into_pg(schema='sync',
                   table='blocks',
                   columns='block_num, synced',
                   values=(int(block_instance.number), True),
                   database_cursor=database_cursor)
    print(f'Block number {block_instance.number} was successfully processed.')


def load_transfers(database_cursor, event_dict):
    transfers_dict = event_dict['Transfer']
    for transfer_id in transfers_dict:
        insert_into_pg(schema='hex',
                       table='transfers',
                       columns='id,'
                               'address,'
                               'recipient_address,'
                               'hex_amount,'
                               'transaction_hash,'
                               'log_index',
                       values=(transfers_dict[transfer_id].transaction_hash.hex()
                               + '_'
                               + str(transfers_dict[transfer_id].log_index),
                               transfers_dict[transfer_id].args['from'],
                               transfers_dict[transfer_id].args['to'],
                               float(transfers_dict[transfer_id].args['value'])/100000000,
                               transfers_dict[transfer_id].transaction_hash.hex(),
                               int(transfers_dict[transfer_id].log_index)),
                       database_cursor=database_cursor)
    print('Transfers processed')


def load_stakes(database_cursor, event_dict):
    stake_starts = event_dict['StakeStart']
    stake_ends = event_dict['StakeEnd']
    share_rate_changes = event_dict['ShareRateChange']
    good_accounting_txn = event_dict['StakeGoodAccounting']
    for dict_id in stake_starts:
        # DATA0
        data0 = str(stake_starts[dict_id].args['data0']).strip()
        bytes32 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes32[0:5], 'little')
        staked_hearts = int.from_bytes(bytes32[5:14], 'little')
        stake_shares = int.from_bytes(bytes32[14:23], 'little')
        staked_days = int.from_bytes(bytes32[23:25], 'little')
        auto_stake = int.from_bytes(bytes32[25:26], 'little')

        insert_into_pg(schema='hex',
                       table='stakes',
                       columns='id,'
                               'address,'
                               'principal,'
                               't_shares,'
                               'staked_days,'
                               'created_at,'
                               'started_at,'
                               'is_auto_stake,'
                               'start_transaction_hash,'
                               'share_rate_changed,'
                               'good_accounted,'
                               'previously_unlocked',
                       values=(int(stake_starts[dict_id].args['stakeId']),
                               stake_starts[dict_id].args['stakerAddr'],
                               float(staked_hearts)/100000000,
                               float(stake_shares)/1000000000000,
                               staked_days,
                               datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"),
                               (datetime.utcfromtimestamp(timestamp) + timedelta(days=1)).strftime("%Y-%m-%d"),
                               bool(auto_stake),
                               stake_starts[dict_id].transaction_hash.hex(),
                               bool(0),
                               bool(0),
                               bool(0)),
                       database_cursor=database_cursor)
    for dict_id in stake_ends:
        # DATA0
        data0 = str(stake_ends[dict_id].args['data0']).strip()
        bytes32_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes32_data0[0:5], 'little')
        payout = int.from_bytes(bytes32_data0[23:32], 'little')

        # DATA1
        data1 = str(stake_ends[dict_id].args['data1']).strip()
        bytes32_data1 = int(data1).to_bytes(32, 'little')
        penalty = int.from_bytes(bytes32_data1[0:9], 'little')
        served_days = int.from_bytes(bytes32_data1[9:11], 'little')
        prev_unlocked = int.from_bytes(bytes32_data1[11:12], 'little')
        upsert_stakes_into_pg(schema='hex',
                              table='stakes',
                              columns='id,'
                                      'payout,' 
                                      'penalty,'
                                      'served_days,'
                                      'ended_at,'
                                      'previously_unlocked,'
                                      'end_transaction_hash',
                              values=(int(stake_ends[dict_id].args['stakeId']),
                                      float(payout)/100000000,
                                      float(penalty)/100000000,
                                      served_days,
                                      datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"),
                                      bool(prev_unlocked),
                                      stake_ends[dict_id].transaction_hash.hex()),
                              database_cursor=database_cursor,
                              primary_key_column='id',
                              payout_value=float(payout)/100000000,
                              penalty_value=float(penalty)/100000000,
                              served_days_value=served_days,
                              ended_at_value=datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"),
                              previously_unlocked_value=bool(prev_unlocked),
                              end_transaction_hash_value=stake_ends[dict_id].transaction_hash.hex())

    for dict_id in share_rate_changes:
        # DATA0
        data0 = share_rate_changes[dict_id].args['data0']
        bytes_data0 = int(data0).to_bytes(32, 'little')
        share_rate = int.from_bytes(bytes_data0[5:10], 'little')

        update_share_rate_changes(schema='hex',
                                  table='stakes',
                                  stake_id=int(share_rate_changes[dict_id].args['stakeId']),
                                  share_rate=float(share_rate)/10,
                                  database_cursor=database_cursor)

    for dict_id in good_accounting_txn:
        # DATA0
        data0 = good_accounting_txn[dict_id].args['data0']
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        payout = int.from_bytes(bytes_data0[23:32], 'little')

        # DATA1
        data1 = good_accounting_txn[dict_id].args['data1']
        bytes_data1 = int(data1).to_bytes(32, 'little')
        penalty = int.from_bytes(bytes_data1[0:9], 'little')

        update_good_accounting(schema='hex',
                               table='stakes',
                               stake_id=int(good_accounting_txn[dict_id].args['stakeId']),
                               payout=float(payout)/100000000,
                               penalty=float(penalty)/100000000,
                               timestamp_at=datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f"),
                               txn_hash=good_accounting_txn[dict_id].transaction_hash.hex(),
                               database_cursor=database_cursor)
    print('Stakes processed')


def load_daily_data_updates(database_cursor, event_dict, gql_dict):
    event_updates = event_dict['DailyDataUpdate']
    gql_updates = gql_dict['DailyDataUpdate']
    for dict_id in event_updates:
        # DATA0
        data0 = str(event_updates[dict_id].args['data0']).strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        begin_day = int.from_bytes(bytes_data0[5:7], 'little')
        end_day = int.from_bytes(bytes_data0[7:9], 'little')
        insert_into_pg(schema='hex',
                       table='daily_data_updates',
                       columns='day,'
                               'next_day,'
                               'transaction_hash,'
                               'payout_per_t_share,'
                               'payout,'
                               'shares',
                       values=(begin_day,
                               end_day,
                               event_updates[dict_id].transaction_hash.hex(),
                               gql_updates['dailyDataUpdates'][0]['payoutPerTShare'],
                               float(gql_updates['dailyDataUpdates'][0]['payout'])/100000000,
                               float(gql_updates['dailyDataUpdates'][0]['shares'])/1000000000000),
                       database_cursor=database_cursor)
    print('Daily Data Updates processed')


def load_global_variables(database_cursor, gql_dict):
    gql_updates = gql_dict['GlobalInfo']
    if len(gql_updates['globalInfos']) > 0:
        insert_into_pg(schema='hex',
                       table='global_variables',
                       columns='block_number,'
                               'total_supply,'
                               'circulating_supply,'
                               'allocated_supply,'
                               'locked_supply,'
                               'total_minted,'
                               't_share_rate,'
                               'total_t_shares_staked',
                       values=(gql_updates['globalInfos'][0]['blocknumber'],
                               float(gql_updates['globalInfos'][0]['totalSupply']) / 100000000,
                               float(gql_updates['globalInfos'][0]['totalHeartsinCirculation']) / 100000000,
                               float(gql_updates['globalInfos'][0]['allocatedSupply']) / 100000000,
                               float(gql_updates['globalInfos'][0]['lockedHeartsTotal']) / 100000000,
                               float(gql_updates['globalInfos'][0]['totalMintedHearts']) / 100000000,
                               float(gql_updates['globalInfos'][0]['shareRate']) / 10,
                               float(gql_updates['globalInfos'][0]['stakeSharesTotal']) / 1000000000000),
                       database_cursor=database_cursor)
    print('Global Variables processed')


def load_swaps(database_cursor, gql_dict):
    gql_swaps_v2 = gql_dict['UniswapV2']
    gql_swaps_v3 = gql_dict['UniswapV3']
    for swap in gql_swaps_v2['swaps']:
        insert_into_pg(schema='hex',
                       table='swaps',
                       columns='id,'
                               'transaction_hash,'
                               'sender,'
                               'recipient,'
                               'hex_amount,'
                               'usdc_amount,'
                               'uniswap,'
                               'log_index',
                       values=(swap['transaction']['id'] + '_' + swap['logIndex'],
                               swap['transaction']['id'],
                               swap['sender'],
                               swap['to'],
                               float(swap['amount0In']) - float(swap['amount0Out']),
                               float(swap['amount1In']) - float(swap['amount1Out']),
                               'v2',
                               int(swap['logIndex'])),
                       database_cursor=database_cursor)

    for swap in gql_swaps_v3['swaps']:
        insert_into_pg(schema='hex',
                       table='swaps',
                       columns='id,'
                               'transaction_hash,'
                               'sender,'
                               'recipient,'
                               'hex_amount,'
                               'usdc_amount,'
                               'uniswap,'
                               'log_index',
                       values=(swap['transaction']['id'] + '_' + swap['logIndex'],
                               swap['transaction']['id'],
                               swap['sender'],
                               swap['recipient'],
                               float(swap['amount0']),
                               float(swap['amount1']),
                               'v3',
                               int(swap['logIndex'])),
                       database_cursor=database_cursor)
    print('Swaps processed')


def main():
    # CONFIGURATION
    print('\nConfiguration loading...')
    hex_contract = SmartContract(name=hex_contract_dict['name'],
                                 address=hex_contract_dict['address'],
                                 abi=hex_contract_dict['abi'],
                                 deployed_block_height=hex_contract_dict['deployed_block_height'],
                                 web3_infura_connection=web3)
    counter_up()

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
