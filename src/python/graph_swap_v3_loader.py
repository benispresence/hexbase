from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from configs.config import get_infura_conn, get_pg_conn
from configs.smart_contract_configs import hex_contract_dict
from classes import Block
from utils import check_db_table, insert_into_pg, begin_db_transaction, commit_db_transaction

pg_conn = get_pg_conn()
web3 = get_infura_conn()

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query_last_end_day = gql(
    """
    {
    swaps(orderBy: timestamp, orderDirection: desc, where: { pool: "0x69d91b94f0aaf8e8a2586909fa77a5c2c89818d5" }) {
          pool {
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
          recipient
          amount0
          amount1
          logIndex
         }
    }

"""
)

sql_query_last_block_number = 'SELECT max(block_number::INT) FROM dl_subgraph_hex.uniswap_v3'


def query_subgraph_swap_v3():
    # Execute the query on the transport
    result = client.execute(query_last_end_day)
    current_block_number = int(result["swaps"][0]['transaction']['blockNumber'])
    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(sql_query_last_block_number)
            block_number = cursor.fetchall()[0][0]
            if block_number is None:
                last_block_number = 12376598
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
                    swaps(orderBy: timestamp, orderDirection: desc, 
                          where: {{ pool: "0x69d91b94f0aaf8e8a2586909fa77a5c2c89818d5", timestamp: {block.timestamp} }}
                          ) {{
                            pool {{
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
                            recipient
                            amount0
                            amount1
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
                        table='uniswap_v3',
                        columns=f'transaction_hash, block_number, created_at, sender, recipient, token_0_id,'
                                f' token_0_symbol,token_0_amount, token_1_id, token_1_symbol, token_1_amount, log_index',
                        values=(swap['transaction']['id'], swap['transaction']['blockNumber'],
                                swap['transaction']['timestamp'], swap['sender'], swap['recipient'],
                                swap['pool']['token0']['id'], swap['pool']['token0']['symbol'], swap['amount0'],
                                swap['pool']['token1']['id'], swap['pool']['token1']['symbol'], swap['amount1'],
                                swap['logIndex'] ),
                        cursor=cursor
                    )
                commit_db_transaction(cursor=cursor)
        print(f'Block {block_num} was processed.')


if __name__ == '__main__':
    check_db_table(schema='dl_subgraph_hex', table='uniswap_v3')
    query_subgraph_swap_v3()
