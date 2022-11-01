from loads.database import insert_into_pg


def load_swaps(database_cursor, event_dict):
    swaps_dict = event_dict['Swap']
    for swap_id in swaps_dict:
        insert_into_pg(schema='uniswap_v2',
                       table='swaps',
                       columns='id,'
                               'hex_sold,'
                               'usdc_sold,'
                               'hex_bought,'
                               'usdc_bought,'
                               'address,'
                               'transaction_hash,'
                               'log_index',
                       values=(swaps_dict[swap_id].transaction_hash.hex()
                               + '_'
                               + str(swaps_dict[swap_id].log_index),
                               swaps_dict[swap_id].args['amount0In']/100000000,
                               swaps_dict[swap_id].args['amount1In']/1000000,
                               swaps_dict[swap_id].args['amount0Out'] / 100000000,
                               swaps_dict[swap_id].args['amount1Out'] / 1000000,
                               swaps_dict[swap_id].args['to'],
                               swaps_dict[swap_id].transaction_hash.hex(),
                               str(swaps_dict[swap_id].log_index)),
                       database_cursor=database_cursor)
