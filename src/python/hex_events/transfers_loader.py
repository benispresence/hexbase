from configs.config import get_infura_conn, get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_transfers():
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
                                 '      AS from_address,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 2),\':\',2),\'"\',2) ' \
                                 '      AS to_address,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 3),\':\',2),\'}\',1) ' \
                                 '      AS value,' \
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'Transfer\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.transfers' \
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
    check_db_table(schema='hex_events', table='transfers')

    transfers = get_transfers()

    for transfer in transfers:
        # ARGS
        from_address = transfer[0].strip()
        to_address = transfer[1].strip()
        value = transfer[2].strip()

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='transfers',

                               columns=f'log_index, transaction_hash, from_address, to_address, transfer_value',
                               values=(transfer[4], transfer[5].strip(), from_address, to_address, value),

                               cursor=cursor)

        print(f'Transfer for {transfer[5].strip()} with log index {transfer[4]} was processed')
