from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from configs.config import get_pg_conn
from utils import check_db_table, insert_into_pg

pg_conn = get_pg_conn()


# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/codeakk/hex")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
graph_query_current_end_day = gql(
    """
    {
    dailyDataUpdates( orderBy: endDay, orderDirection: desc) {
        endDay
        payoutPerTShare
        payout
        shares
        }
    }
"""
)


sql_query_last_end_day = 'SELECT max(end_day::INT) FROM dl_subgraph_hex.daily_data_updates'


def query_subgraph_daily_data_updates():
    # Execute the query on the transport
    result = client.execute(graph_query_current_end_day)
    current_end_day = result["dailyDataUpdates"][0]['endDay']
    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(sql_query_last_end_day)
            last_end_day = cursor.fetchall()[0][0] + 1
    for day in range(last_end_day, current_end_day):
        # Provide a GraphQL query
        query = gql(
            f"""
                {{
                dailyDataUpdates(where: {{endDay: {day}}}, orderBy: endDay, orderDirection: desc) {{
                    endDay
                    payoutPerTShare
                    payout
                    shares
                    }}
                }}
            """
        )
        daily_data_update = client.execute(query)

        with pg_conn:
            with pg_conn.cursor() as cursor:
                insert_into_pg(
                    schema='dl_subgraph_hex',
                    table='daily_data_updates',
                    columns=f'end_day, payout_per_t_share, payout, shares',
                    values=(daily_data_update['dailyDataUpdates'][0]['endDay'],
                            daily_data_update['dailyDataUpdates'][0]['payoutPerTShare'],
                            daily_data_update['dailyDataUpdates'][0]['payout'],
                            daily_data_update['dailyDataUpdates'][0]['shares']
                            ),
                    cursor=cursor
                )
        print(f'Day {day} was processed.')


if __name__ == '__main__':
    check_db_table(schema='dl_subgraph_hex', table='daily_data_updates')
    query_subgraph_daily_data_updates()

