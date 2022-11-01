from datetime import datetime, timedelta

from loads.database import insert_into_pg


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


def load_daily_data_updates(database_cursor, event_dict, contract):
    event_updates = event_dict['DailyDataUpdate']
    for dict_id in event_updates:
        # DATA0
        data0 = str(event_updates[dict_id].args['data0']).strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        begin_day = int.from_bytes(bytes_data0[5:7], 'little')
        end_day = int.from_bytes(bytes_data0[7:9], 'little')
        # payout, shares, unclaimedBitcoins
        daily_data_list = contract.web3_contract_interface.functions.dailyData(begin_day).call()
        try:
            payout = float(daily_data_list[0])/100000000
        except ZeroDivisionError:
            payout = 0
        try:
            shares = float(daily_data_list[1])/1000000000000
        except ZeroDivisionError:
            shares = 0
        try:
            payout_per_t_share = payout/shares
        except ZeroDivisionError:
            payout_per_t_share = 0
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
                               payout_per_t_share,
                               payout,
                               shares),
                       database_cursor=database_cursor)