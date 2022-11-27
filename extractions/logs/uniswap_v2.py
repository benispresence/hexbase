
def extract_logs(contract, block_number):
    """
    :param contract: The hex smart contract instance. (class UniswapV2Contract)
    :param block_number: The ethereum block number (int).
    :return: A dict of event specific dicts of a dictionary of logs.
    """
    swap_filter = contract.swap['event_class'].createFilter(fromBlock=block_number,
                                                            toBlock=block_number)

    swap_logs = swap_filter.get_all_entries()

    all_logs_dicts = {'Swap': swap_logs}

    return all_logs_dicts
