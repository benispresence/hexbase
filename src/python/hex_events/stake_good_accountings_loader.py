from configs.config import get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()


def get_stake_good_accountings():
    get_stake_good_accountings_query = 'WITH transaction_base AS ( ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.transactions ' \
                                 '  UNION ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.indirect_transactions' \
                                 '), ' \
                                 '' \
                                 'event_base AS (' \
                                 '  SELECT ' \
                                 '      split_part(split_part(split_part(e.args,\',\', 1),\':\',2),\'"\',2) ' \
                                       'AS staker_address,' \
                                 '      split_part(split_part(e.args, \',\', 2),\':\',2) AS stake_id,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 3),\':\',2),\'"\',2) ' \
                                       'AS staker_address,' \
                                 '      split_part(split_part(e.args, \',\', 4),\':\',2) AS data0,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 5),\':\',2),\'}\',1) AS data1,'\
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'StakeGoodAccounting\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.stake_good_accountings' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_stake_good_accountings_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='stake_good_accountings')

    good_accountings = get_stake_good_accountings()

    for ga in good_accountings:
        # ARGS
        staker_address = ga[0].strip()
        stake_id = ga[1].strip()
        sender_address = ga[2].strip()

        # DATA0
        data0 = ga[3].strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        staked_hearts = int.from_bytes(bytes_data0[5:14], 'little')
        stake_shares = int.from_bytes(bytes_data0[14:23], 'little')
        payout = int.from_bytes(bytes_data0[23:32], 'little')

        # DATA1
        data1 = ga[4].strip()
        bytes_data1 = int(data1).to_bytes(32, 'little')
        penalty = int.from_bytes(bytes_data1[0:9], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='stake_good_accountings',

                               columns=f'log_index, transaction_hash, staker_address, stake_id, sender_address,'
                                       f' created_at, staked_hearts, stake_shares, payout, penalty',

                               values=(ga[6], ga[7].strip(), staker_address, stake_id, sender_address, timestamp,
                                       staked_hearts, stake_shares, payout, penalty),

                               cursor=cursor)

        print(f'Stake Start for {ga[7].strip()} with log index {ga[6]} was processed')
