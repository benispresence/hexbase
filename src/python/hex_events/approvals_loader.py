from configs.config import get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()


def get_approvals():
    get_approvals_query = 'WITH transaction_base AS ( ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.transactions ' \
                                 '  UNION ' \
                                 '  SELECT hash, timestamp ' \
                                 '  FROM hex.indirect_transactions' \
                                 '), ' \
                                 '' \
                                 'event_base AS (' \
                                 '  SELECT ' \
                                 '      split_part(split_part(split_part(e.args, \',\', 1),\':\',2),\'"\',2) AS owner,'\
                                 '      split_part(split_part(split_part(e.args, \',\', 2),\':\',2),\'"\',2) ' \
                                 '      AS spender,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 3),\':\',2),\'}\',1) AS value,'\
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'Approval\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.approvals' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_approvals_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='approvals')

    approvals = get_approvals()

    for approval in approvals:
        owner_address = approval[0].strip()
        spender_address = approval[1].strip()
        value = approval[2].strip()

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='approvals',

                               columns=f'log_index, transaction_hash, owner_address, spender_address, approval_value',

                               values=(approval[4], approval[5].strip(), owner_address, spender_address, value),

                               cursor=cursor)

        print(f'Approval for {approval[5].strip()} with log index {approval[4]} was processed')
