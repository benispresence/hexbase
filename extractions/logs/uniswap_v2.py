
def extract_logs(contract, block_number):
    """
    :param contract: The hex smart contract instance. (class UniswapV2Contract)
    :param block_number: The ethereum block number (int).
    :return: A dict of event specific dicts of a dictionary of logs.
    """
    swap_filter = contract.swap['event_class'].createFilter(fromBlock=block_number,
                                                            toBlock=block_number)
    mint_filter = contract.mint['event_class'].createFilter(fromBlock=block_number,
                                                            toBlock=block_number)
    sync_filter = contract.sync['event_class'].createFilter(fromBlock=block_number,
                                                            toBlock=block_number)
    burn_filter = contract.burn['event_class'].createFilter(fromBlock=block_number,
                                                            toBlock=block_number)

    swap_logs = swap_filter.get_all_entries()
    mint_logs = mint_filter.get_all_entries()
    sync_logs = sync_filter.get_all_entries()
    burn_logs = burn_filter.get_all_entries()

    all_logs_dicts = {'Swap': swap_logs,
                      'Mint': mint_logs,
                      'Sync': sync_logs,
                      'Burn': burn_logs}

    return all_logs_dicts
