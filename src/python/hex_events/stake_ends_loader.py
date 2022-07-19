from configs.config import get_infura_conn, get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_stake_ends():
    get_stake_starts_sql_query = 'WITH transaction_base AS ( ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.transactions ' \
                                 '  UNION ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.indirect_transactions' \
                                 '), ' \
                                 '' \
                                 'event_base AS (' \
                                 '  SELECT ' \
                                 '      split_part(split_part(split_part(e.args, \',\', 1),\':\',2),\'"\',2) ' \
                                 '      AS staker_address,' \
                                 '      split_part(split_part(e.args, \',\', 2),\':\',2) AS stake_id,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 3),\':\',2),\'}\',1) AS data0,'\
                                 '      split_part(split_part(split_part(e.args, \',\', 4),\':\',2),\'}\',1) AS data1,'\
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'StakeEnd\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.stake_ends' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_stake_starts_sql_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='stake_ends')

    stake_ends = get_stake_ends()

    for stake in stake_ends:
        # STAKE ID & ADDRESS
        staker_address = stake[0].strip()
        stake_id = stake[1].strip()

        # DATA0
        data0 = stake[2].strip()
        bytes32_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes32_data0[0:5], 'little')
        staked_hearts = int.from_bytes(bytes32_data0[5:14], 'little')
        stake_shares = int.from_bytes(bytes32_data0[14:23], 'little')
        payout = int.from_bytes(bytes32_data0[23:32], 'little')

        # DATA1
        data1 = stake[3].strip()
        bytes32_data1 = int(data1).to_bytes(32, 'little')
        penalty = int.from_bytes(bytes32_data1[0:9], 'little')
        served_days = int.from_bytes(bytes32_data1[9:11], 'little')
        prev_unlocked = int.from_bytes(bytes32_data1[11:12], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='stake_ends',

                               columns=f'log_index, transaction_hash, staker_address, stake_id, timestamp_stake_end, '
                                       f'staked_hearts, stake_shares, payout, penalty, served_days, prev_unlocked',

                               values=(stake[5], stake[6].strip(), staker_address, stake_id, timestamp, staked_hearts,
                                       stake_shares, payout, penalty, served_days, prev_unlocked),

                               cursor=cursor)

        print(f'Stake End for {stake[6].strip()} with log index {stake[5]} was '
              f'processed')
