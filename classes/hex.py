from classes.ethereum import SmartContract


class HexContract(SmartContract):
    """
    The hex smart contract deployed on the ethereum blockchain.
    """
    def __init__(self, name, address, abi, deployed_block_height, web3_infura_connection):
        SmartContract.__init__(self, name, address, abi, deployed_block_height, web3_infura_connection)
        # web3 events
        self.transfer = dict(event_name='Transfer',
                             event_class=self.web3_contract_interface.events.Transfer,
                             event_object=self.web3_contract_interface.events.Transfer())
        self.daily_data_update = dict(event_name='DailyDataUpdate',
                                      event_class=self.web3_contract_interface.events.DailyDataUpdate,
                                      event_object=self.web3_contract_interface.events.DailyDataUpdate())
        self.stake_start = dict(event_name='StakeStart',
                                event_class=self.web3_contract_interface.events.StakeStart,
                                event_object=self.web3_contract_interface.events.StakeStart())
        self.stake_good_accounting = dict(event_name='StakeGoodAccounting',
                                          event_class=self.web3_contract_interface.events.StakeGoodAccounting,
                                          event_object=self.web3_contract_interface.events.StakeGoodAccounting())
        self.stake_end = dict(event_name='StakeEnd',
                              event_class=self.web3_contract_interface.events.StakeEnd,
                              event_object=self.web3_contract_interface.events.StakeEnd())
        self.share_rate_change = dict(event_name='ShareRateChange',
                                      event_class=self.web3_contract_interface.events.ShareRateChange,
                                      event_object=self.web3_contract_interface.events.ShareRateChange())
        self.events = [self.transfer, self.stake_end, self.stake_start, self.stake_good_accounting,
                       self.share_rate_change, self.daily_data_update]
