from web3 import Web3

from configs.credentials import get_config


def get_infura_conn():
    config = get_config()
    infura_url = "https://mainnet.infura.io/v3/"+config['infura2']['token']
    web3_conn = Web3(Web3.HTTPProvider(infura_url))
    return web3_conn


def get_local_node_conn():
    local_node_url = "http://localhost:8545"
    web3_conn = Web3(Web3.HTTPProvider(local_node_url))
    return web3_conn
