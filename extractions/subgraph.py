from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


def extract_subgraph_data(block_instance):
    gql_data = {}
    for subgraph in ['GlobalInfo', 'DailyDataUpdate', 'UniswapV2', 'UniswapV3']:
        graph_dict = get_graphql_config(graph_name=subgraph, block_instance=block_instance)
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url=graph_dict['url'])
        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql(graph_dict['query'])
        result = client.execute(query)
        gql_data[subgraph] = result
    return gql_data


def get_graphql_config(graph_name, block_instance):
    subgraph_queries = {
        'GlobalInfo': {'url': "https://api.thegraph.com/subgraphs/name/codeakk/hex",
                       'query': f"""
                                    {{
                                    globalInfos(where: {{blocknumber: {block_instance.number}}},
                                                orderBy: blocknumber, orderDirection: desc)     {{
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
                       },
        'DailyDataUpdate': {'url': "https://api.thegraph.com/subgraphs/name/codeakk/hex",
                            'query': f"""
                                        {{
                                        dailyDataUpdates(where: {{blockNumber: {block_instance.number}}},
                                                         orderBy: endDay, orderDirection: desc)             {{
                                            endDay
                                            payoutPerTShare
                                            payout
                                            shares
                                            }}
                                        }}
                                    """
                            },
        'UniswapV2': {'url': "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2",
                      'query':  f"""
                                {{
                                    swaps(  orderBy: timestamp, orderDirection: desc,
                                            where: {{pair:      "0xf6dcdce0ac3001b2f67f750bc64ea5beb37b5824",
                                                     timestamp: {block_instance.timestamp}                   }} ) {{
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
                      },
        'UniswapV3': {'url': "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
                      'query':  f"""
                                    {{
                                        swaps(orderBy: timestamp, orderDirection: desc, 
                                              where: {{ pool: "0x69d91b94f0aaf8e8a2586909fa77a5c2c89818d5",
                                                        timestamp: {block_instance.timestamp}               }}
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
                      }
    }
    return subgraph_queries[graph_name]
