from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from configs.config import get_pg_conn
from configs.smart_contract_configs import hex_contract_dict
from utils import check_db_table, insert_into_pg

pg_conn = get_pg_conn()


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/codeakk/hex")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query_last_end_day = gql(
    """
    {
    globalInfos(orderBy: timestamp, orderDirection: desc) {
        transactionHash
        hexDay
        blocknumber
        timestamp
        totalSupply
        totalMintedHearts
        totalHeartsinCirculation
        shareRate
        stakeSharesTotal
        stakePenaltyTotal
        latestStakeId
        allocatedSupply
        nextStakeSharesTotal
        lockedHeartsTotal
        }
    }

"""
)

sql_query_last_block_number = 'SELECT max(block_number::INT) FROM dl_subgraph_hex.global_info'


def query_subgraph_global_info():
    # Execute the query on the transport
    result = client.execute(query_last_end_day)
    current_block_number = int(result["globalInfos"][0]['blocknumber'])
    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(sql_query_last_block_number)
            block_number = cursor.fetchall()[0][0]
            if block_number is None:
                last_block_number = hex_contract_dict['deployed_block_height']
            else:
                last_block_number = block_number + 1
            print(last_block_number)
    # for block in blocks from the ethereum dl extract timestamp and use as filer
    for block in range(last_block_number, current_block_number):
        print(f'Check {block}')
        # Provide a GraphQL query
        query = gql(
            f"""
                {{
                globalInfos(where: {{blocknumber: {block}}}, orderBy: blocknumber, orderDirection: desc) {{
                    transactionHash
                    hexDay
                    blocknumber
                    timestamp
                    totalSupply
                    totalMintedHearts
                    totalHeartsinCirculation
                    shareRate
                    stakeSharesTotal
                    stakePenaltyTotal
                    latestStakeId
                    allocatedSupply
                    nextStakeSharesTotal
                    lockedHeartsTotal
                    }}
                }}
            """
        )
        global_info = client.execute(query)

        if len(global_info['globalInfos']) == 0:
            continue

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(
                    schema='dl_subgraph_hex',
                    table='global_info',
                    columns=f'transaction_hash,hex_day, block_number, timestamp_block, total_supply, '
                            f'total_minted_hearts,total_hearts_in_circulation, share_rate, stake_shares_total,'
                            f'stake_penalty_total, latest_stake_id, allocated_supply, next_stake_shares_total, '
                            f'locked_hearts_total',
                    values=(global_info['globalInfos'][0]['transactionHash'],
                            global_info['globalInfos'][0]['hexDay'],
                            global_info['globalInfos'][0]['blocknumber'],
                            global_info['globalInfos'][0]['timestamp'],
                            global_info['globalInfos'][0]['totalSupply'],
                            global_info['globalInfos'][0]['totalMintedHearts'],
                            global_info['globalInfos'][0]['totalHeartsinCirculation'],
                            global_info['globalInfos'][0]['shareRate'],
                            global_info['globalInfos'][0]['stakeSharesTotal'],
                            global_info['globalInfos'][0]['stakePenaltyTotal'],
                            global_info['globalInfos'][0]['latestStakeId'],
                            global_info['globalInfos'][0]['allocatedSupply'],
                            global_info['globalInfos'][0]['nextStakeSharesTotal'],
                            global_info['globalInfos'][0]['lockedHeartsTotal']),
                    cursor=cursor
                )
        print(f'Block {block} was processed.')


if __name__ == '__main__':
    check_db_table(schema='dl_subgraph_hex', table='global_info')
    query_subgraph_global_info()

