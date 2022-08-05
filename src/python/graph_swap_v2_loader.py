from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from configs.config import get_infura_conn, get_pg_conn
from classes import Block
from utils import check_db_table, insert_into_pg, begin_db_transaction, commit_db_transaction

pg_conn = get_pg_conn()
web3 = get_infura_conn()

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query_last_end_day = gql(
    """
    {
        swaps(orderBy: timestamp, orderDirection: desc, where: {pair: "0xf6dcdce0ac3001b2f67f750bc64ea5beb37b5824" }) {
        pair {
            token0 {
                id
                symbol
            }
            token1 {
                id
                symbol
            }
        }
        transaction {
            id
            blockNumber
            timestamp
        }
        sender
        to
        amount0In
        amount0Out
        amount1In
        amount1Out
        logIndex
        }
    }
"""
)

sql_query_last_block_number = 'SELECT max(block_number::INT) FROM dl_subgraph_hex.uniswap_v2'


def query_subgraph_swap_v2():
    # Execute the query on the transport
    result = client.execute(query_last_end_day)
    current_block_number = int(result["swaps"][0]['transaction']['blockNumber'])
    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(sql_query_last_block_number)
            block_number = cursor.fetchall()[0][0]
            if block_number is None:
                last_block_number = 10091642
            else:
                last_block_number = block_number + 1
            print(f'Last block_number {last_block_number}')
    for block_num in range(last_block_number, current_block_number):
        print(f'Check {block_num}')
        block = Block(web3.eth.get_block(block_num, full_transactions=True))
        # Provide a GraphQL query
        query = gql(
            f"""
                {{
                    swaps(  orderBy: timestamp, orderDirection: desc,
                            where: {{pair:      "0xf6dcdce0ac3001b2f67f750bc64ea5beb37b5824",
                                     timestamp: {block.timestamp}                               }} ) {{
                        pair {{
                            token0 {{
                                id
                                symbol
                            }}
                            token1 {{
                                id
                                symbol
                            }}
                        }}
                        transaction {{
                            id
                            blockNumber
                            timestamp
                        }}
                        sender
                        to
                        amount0In
                        amount0Out
                        amount1In
                        amount1Out
                        logIndex
                    }}
                }}
            """
        )
        swaps = client.execute(query)

        if len(swaps['swaps']) == 0:
            continue

        with pg_conn:
            with pg_conn.cursor() as cursor:
                begin_db_transaction(cursor=cursor)
                for swap in swaps['swaps']:
                    print(swaps)
                    insert_into_pg(
                        schema='dl_subgraph_hex',
                        table='uniswap_v2',
                        columns=f'transaction_hash, block_number, created_at, sender, recipient,'
                                f' token_0_id, token_0_symbol, token_0_amount_in, token_0_amount_out,'
                                f' token_1_id, token_1_symbol, token_1_amount_in, token_1_amount_out, log_index',
                        values=(swap['transaction']['id'], swap['transaction']['blockNumber'],
                                swap['transaction']['timestamp'], swap['sender'], swap['to'],
                                swap['pair']['token0']['id'], swap['pair']['token0']['symbol'], swap['amount0In'],
                                swap['amount0Out'], swap['pair']['token1']['id'], swap['pair']['token1']['symbol'],
                                swap['amount1In'], swap['amount1Out'], swap['logIndex']),
                        cursor=cursor
                    )
                commit_db_transaction(cursor=cursor)
        print(f'Block {block_num} was processed.')


if __name__ == '__main__':
    check_db_table(schema='dl_subgraph_hex', table='uniswap_v2')
    query_subgraph_swap_v2()
