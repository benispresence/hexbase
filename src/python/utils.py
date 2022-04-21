from configs.config import get_pg_conn

pg_conn = get_pg_conn()


def get_last_block_number_from_b_dwh(schema, table, column):
    """
    :param schema: B-DWH Schema name (str)
    :param table: B-DWH table name (str)
    :param column: B-DWH block_number column name (str)
    :return: Returns the last block number from one of the tables from the (B-DWH) Blockchain Data Warehouse.
    """
    last_block_query = f'SELECT max({column} :: INT) FROM {schema}.{table};'

    with pg_conn:
        with pg_conn.cursor() as curs:
            curs.execute(last_block_query)
            block_num = curs.fetchall()

    return block_num[0][0]
