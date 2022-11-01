import psycopg2

from configs.credentials import get_config


def get_pg_conn():
    """
    :return: A connection to the Hexbase postgres database.
    """
    config = get_config()
    pg_conn = psycopg2.connect(
        dbname=config['postgre_db']['dbname_hexbase_v4']
        , user=config['postgre_db']['user']
        , password=config['postgre_db']['password']
        , host=config['postgre_db']['host']
        , port=config['postgre_db']['port']
    )
    return pg_conn
