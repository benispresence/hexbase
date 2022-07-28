from configs.config import get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()


def get_daily_data_updates():
    get_daily_data_updates_query = 'WITH transaction_base AS ( ' \
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
                                 '      AS staker_address, ' \
                                 '      split_part(split_part(split_part(e.args, \',\', 2),\':\',2),\'}\',1) AS data0,'\
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'DailyDataUpdate\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.daily_data_updates' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_daily_data_updates_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='daily_data_updates')

    daily_data_updates = get_daily_data_updates()

    for update in daily_data_updates:
        staker_address = update[0].strip()

        # DATA0
        data0 = update[1].strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        begin_day = int.from_bytes(bytes_data0[5:7], 'little')
        end_day = int.from_bytes(bytes_data0[7:9], 'little')
        is_auto_update = int.from_bytes(bytes_data0[9:10], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='daily_data_updates',

                               columns=f'log_index, transaction_hash, staker_address, created_at,'
                                       f' begin_day, end_day, is_auto_update',

                               values=(update[3], update[4].strip(), staker_address, timestamp,
                                       begin_day, end_day, is_auto_update),

                               cursor=cursor)

        print(f'Stake Start for {update[4].strip()} with log index {update[3]} was processed')
