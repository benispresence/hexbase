
def begin_db_transaction(database_cursor):
    begin = f'BEGIN;'
    database_cursor.execute(begin)


def commit_db_transaction(database_cursor):
    commit = f'COMMIT;'
    database_cursor.execute(commit)


def insert_into_pg(schema, table, columns, values, database_cursor):
    # SQL
    insert_txn_statement = f'insert into {schema}.{table} ({columns}) values {tuple(values)};'

    # INSERT TO POSTGRES
    database_cursor.execute(insert_txn_statement)
