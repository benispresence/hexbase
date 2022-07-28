from configs.config import get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()


def get_xf_lobby_enters():
    get_xf_lobby_enters_query = 'WITH transaction_base AS ( ' \
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
                                 '      AS member_address,' \
                                 '      split_part(split_part(e.args, \',\', 2),\':\',2) AS entryId,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 3),\':\',2),\'"\',2) ' \
                                 '      AS referrer_address,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 4),\':\',2),\'}\',1) AS data0,'\
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'XfLobbyEnter\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.xf_lobby_enters' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_xf_lobby_enters_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='xf_lobby_enters')

    xf_lobby_enters = get_xf_lobby_enters()

    for enter in xf_lobby_enters:
        print(enter)
        member_address = enter[0].strip()
        entryId = enter[1].strip()
        referrer_address = enter[2].strip()

        # DATA0
        data0 = enter[3].strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        raw_amount = int.from_bytes(bytes_data0[5:17], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='xf_lobby_enters',

                               columns=f'log_index, transaction_hash, member_address, entry_id, referrer_address,'
                                       f' created_at, raw_amount',

                               values=(enter[5], enter[6].strip(), member_address, entryId, referrer_address,
                                       timestamp, raw_amount),

                               cursor=cursor)

        print(f'Xf Lobby Enter for {enter[6].strip()} with log index {enter[5]} was processed')
