
def extract_logs(contract, block_number):
    """
    :param contract: The hex smart contract instance. (class HexContract)
    :param block_number: The ethereum block number (int).
    :return: A dict of event specific dicts of a dictionary of logs.
    """
    transfer_filter = contract.transfer['event_class'].createFilter(fromBlock=block_number,
                                                                    toBlock=block_number)
    daily_data_update_filter = contract.daily_data_update['event_class'].createFilter(fromBlock=block_number,
                                                                                      toBlock=block_number)
    stake_start_filter = contract.stake_start['event_class'].createFilter(fromBlock=block_number,
                                                                          toBlock=block_number)
    stake_good_accounting_filter = contract.stake_good_accounting['event_class'].createFilter(fromBlock=block_number,
                                                                                              toBlock=block_number)
    stake_end_filter = contract.stake_end['event_class'].createFilter(fromBlock=block_number,
                                                                      toBlock=block_number)
    share_rate_change_filter = contract.share_rate_change['event_class'].createFilter(fromBlock=block_number,
                                                                                      toBlock=block_number)

    transfer_logs = transfer_filter.get_all_entries()
    daily_data_update_logs = daily_data_update_filter.get_all_entries()
    stake_start_logs = stake_start_filter.get_all_entries()
    stake_good_accounting_logs = stake_good_accounting_filter.get_all_entries()
    stake_end_logs = stake_end_filter.get_all_entries()
    share_rate_change_logs = share_rate_change_filter.get_all_entries()
    all_logs_dicts = {'Transfer': transfer_logs,
                      'DailyDataUpdate': daily_data_update_logs,
                      'StakeStart': stake_start_logs,
                      'StakeGoodAccounting': stake_good_accounting_logs,
                      'StakeEnd': stake_end_logs,
                      'ShareRateChange': share_rate_change_logs}

    return all_logs_dicts
