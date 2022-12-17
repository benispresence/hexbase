from web3 import Web3

from configs.credentials import get_config


def get_local_node_conn():
    """
    :return: A connection to web3 via a local ethereum node.
    """
    config = get_config()
    url = config['rpc']['url']
    web3_conn = Web3(Web3.HTTPProvider(url))
    return web3_conn
