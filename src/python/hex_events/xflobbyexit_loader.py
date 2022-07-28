from configs.config import get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()


def get_xf_lobby_exits():
    get_xf_lobby_exits_query = 'WITH transaction_base AS ( ' \
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
                                 '  WHERE event = \'XfLobbyExit\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.xf_lobby_exits' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_xf_lobby_exits_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='xf_lobby_exits')

    xf_lobby_exits = get_xf_lobby_exits()

    for exit in xf_lobby_exits:
        member_address = exit[0].strip()
        entryId = exit[1].strip()
        referrer_address = exit[2].strip()

        # DATA0
        data0 = exit[3].strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        xfamount = int.from_bytes(bytes_data0[5:14], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='xf_lobby_exits',

                               columns=f'log_index, transaction_hash, member_address, entry_id, referrer_address,'
                                       f' created_at, xf_amount',

                               values=(exit[5], exit[6].strip(), member_address, entryId, referrer_address,
                                       timestamp, xfamount),

                               cursor=cursor)

        print(f'Xf Lobby Exit for {exit[6].strip()} with log index {exit[5]} was processed')
