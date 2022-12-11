from web3 import Web3


def get_local_node_conn():
    """
    :return: A connection to web3 via a local ethereum node.
    """
    local_node_url = "http://localhost:8545"
    web3_conn = Web3(Web3.HTTPProvider(local_node_url))
    return web3_conn
