from configs.config import get_infura_conn, get_pg_conn
from utils import check_db_table, insert_into_pg


pg_conn = get_pg_conn()
web3 = get_infura_conn()


def get_claims():
    get_claims_query = 'WITH transaction_base AS ( ' \
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
                                 '      AS btc_address, ' \
                                 '      split_part(split_part(split_part(e.args, \',\', 2),\':\',2),\'"\',2) ' \
                                 '      AS claim_to_address, ' \
                                 '      split_part(split_part(split_part(e.args, \',\', 3),\':\',2),\'"\',2) ' \
                                 '      AS referrer_address, ' \
                                 '      split_part(split_part(split_part(e.args, \',\', 4),\':\',2),\'}\',1) ' \
                                 '      AS data0,' \
                                 '      split_part(split_part(split_part(e.args, \',\', 5),\':\',2),\'}\',1) ' \
                                 '      AS data1,' \
                                 '      to_timestamp(timestamp :: BIGINT) AS created_at, ' \
                                 '      e.log_index :: INT AS log_index,' \
                                 '      hash AS txn_hash ' \
                                 '  FROM hex.events e ' \
                                 '  LEFT JOIN transaction_base t ON e.transaction_hash=t.hash ' \
                                 '  WHERE event = \'Claim\' ' \
                                 '  AND (hash, log_index) NOT IN (' \
                                 '              SELECT transaction_hash, log_index ' \
                                 '              FROM hex_events.claims' \
                                 '              )' \
                                 ') ' \
                                 '' \
                                 'SELECT * ' \
                                 'FROM event_base'

    with pg_conn.cursor() as cursor:
        cursor.execute(get_claims_query)
        events = cursor.fetchall()
    return events


if __name__ == '__main__':
    check_db_table(schema='hex_events', table='claims')

    claims = get_claims()

    for claim in claims:
        # ADDRESSES
        btc_address = claim[0].strip()
        claim_to_address = claim[1].strip()
        referrer_address = claim[2].strip()

        # DATA0
        data0 = claim[3].strip()
        bytes_data0 = int(data0).to_bytes(32, 'little')
        timestamp = int.from_bytes(bytes_data0[0:5], 'little')
        raw_satoshis = int.from_bytes(bytes_data0[5:12], 'little')
        adjusted_satoshis = int.from_bytes(bytes_data0[12:19], 'little')
        claim_flags = int.from_bytes(bytes_data0[19:20], 'little')
        claimed_hearts = int.from_bytes(bytes_data0[20:29], 'little')

        # DATA1
        data1 = claim[4].strip()
        bytes_data1 = int(data1).to_bytes(32, 'little')
        sender_address = int.from_bytes(bytes_data1[0:20], 'little')

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(schema='hex_events',
                               table='claims',

                               columns=f'log_index, transaction_hash, btc_address, claim_to_address, referrer_address, '
                                       f'created_at, raw_satoshis, adjusted_satoshis, claim_flags, claimed_hearts,'
                                       f' sender_address',
                               values=(claim[6], claim[7].strip(), btc_address, claim_to_address, referrer_address,
                                       timestamp, raw_satoshis, adjusted_satoshis, claim_flags, claimed_hearts,
                                       sender_address),

                               cursor=cursor)

        print(f'Claim for {claim[7].strip()} with log index {claim[6]} was processed')
