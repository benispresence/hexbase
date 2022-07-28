from configs.config import get_infura_conn, get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_share_rate_changes():
    get_share_rate_changes_query = 'WITH transaction_base AS ( ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.transactions ' \
                                 '  UNION ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.indirect_transactions' \
                                 '), ' \
                                 '' \
                                 'event_base AS (' \
                                 '  SELECT ' \
                                 '      split_part(split_part(e.args, \',\', 1),\':\',2) AS stake_id,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 2),\':\',2),\'}\',1) AS data0,'\
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'ShareRateChange\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.share_rate_changes' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_share_rate_changes_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='share_rate_changes')

    share_rate_changes = get_share_rate_changes()

    for change in share_rate_changes:
        stake_id = change[0].strip()
        # DATA0
        data0 = change[1].strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        share_rate = int.from_bytes(bytes_data0[5:10], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='share_rate_changes',

                               columns=f'log_index, transaction_hash, stake_id, created_at, share_rate',

                               values=(change[3], change[4].strip(), stake_id, timestamp, share_rate),

                               cursor=cursor)

        print(f'Stake Start for {change[4].strip()} with log index {change[3]} was processed')
