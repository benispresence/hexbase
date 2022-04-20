from python.configs.config import get_pg_conn

pg_conn = get_pg_conn()

if __name__ == '__main__':
    query = f"SELECT count(*), hash, blocknumber FROM dl_ethereum.transactions " \
            f"GROUP BY hash, blocknumber HAVING count(*) > 1;"
    with pg_conn:
        with pg_conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            print('Now elements will be printed')
            for element in result:
                print(element)
