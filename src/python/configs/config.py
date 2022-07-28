import configparser
import psycopg2

from web3 import Web3

PATH_CONFIG = '/Users/benjaminharmat/global_config.ini'

config = configparser.ConfigParser()
config.read(PATH_CONFIG)


def get_pg_conn():
    pg_conn = psycopg2.connect(
        dbname=config['postgre_db']['dbname']
        , user=config['postgre_db']['user']
        , password=config['postgre_db']['password']
        , host=config['postgre_db']['host']
        , port=config['postgre_db']['port']
    )
    return pg_conn


def get_infura_conn():
    infura_url = "https://mainnet.infura.io/v3/"+config['infura3']['token']
    web3_conn = Web3(Web3.HTTPProvider(infura_url))
    return web3_conn


def get_local_node_conn():
    local_node_url = "http://localhost:8545"
    web3_conn = Web3(Web3.HTTPProvider(local_node_url))
    return web3_conn
