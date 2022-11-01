from loads.database import insert_into_pg


def sync(database_cursor, block_instance, table):
    insert_into_pg(schema='sync',
                   table=table,
                   columns='block_num, synced',
                   values=(int(block_instance.number), True),
                   database_cursor=database_cursor)
    print(f'Block number {block_instance.number} was successfully processed.')
