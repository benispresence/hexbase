from classes.ethereum import SmartContract


class UniswapV2Contract(SmartContract):
    """
    The Uniswap v2 smart contract deployed on the ethereum blockchain.
    """
    def __init__(self, name, address, abi, deployed_block_height, web3_infura_connection):
        SmartContract.__init__(self, name, address, abi, deployed_block_height, web3_infura_connection)
        self.swap = dict(event_name='Swap',
                         event_class=self.web3_contract_interface.events.Swap,
                         event_object=self.web3_contract_interface.events.Swap())
        self.mint = dict(event_name='Mint',
                         event_class=self.web3_contract_interface.events.Mint,
                         event_object=self.web3_contract_interface.events.Mint())
        self.sync = dict(event_name='Sync',
                         event_class=self.web3_contract_interface.events.Sync,
                         event_object=self.web3_contract_interface.events.Sync())
        self.burn = dict(event_name='Burn',
                         event_class=self.web3_contract_interface.events.Burn,
                         event_object=self.web3_contract_interface.events.Burn())
        self.events = [self.swap, self.mint, self.sync, self.burn]
