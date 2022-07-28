from configs.config import get_infura_conn, get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_stake_starts():
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
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'StakeStart\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.stake_starts' \
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
    check_db_table(schema='hex_events', table='stake_starts')

    start_stakes = get_stake_starts()

    for stake in start_stakes:
        # DATA0
        data0 = stake[2].strip()
        bytes32 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes32[0:5], 'little')
        staked_hearts = int.from_bytes(bytes32[5:14], 'little')
        stake_shares = int.from_bytes(bytes32[14:23], 'little')
        staked_days = int.from_bytes(bytes32[23:25], 'little')
        auto_stake = int.from_bytes(bytes32[25:26], 'little')

        # STAKE ID & ADDRESS
        staker_address = stake[0].strip()
        stake_id = stake[1].strip()

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='stake_starts',

                               columns=f'log_index, transaction_hash, staker_address, stake_id, timestamp_stake_start, '
                                       f'staked_hearts, stake_shares, staked_days, is_auto_stake',

                               values=(stake[4], stake[5].strip(), staker_address, stake_id, timestamp, staked_hearts,
                                       stake_shares, staked_days, auto_stake),

                               cursor=cursor)

        print(f'Stake Start for {stake[5].strip()} with log index {stake[4]} was '
              f'processed')
