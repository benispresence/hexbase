from datetime import datetime

from loads.database import insert_into_pg


def load_transactions(database_cursor, block_instance, schema, table, txn_dict, txn_receipts_dict, contract):
    for txn_hash in txn_dict:
        transaction = txn_dict[txn_hash]
        receipt = txn_receipts_dict[txn_hash]
        function_called, arguments = \
            transaction.get_function_arguments(abi=contract.abi,
                                               address=contract.address,
                                               web3_contract=contract.web3_contract_interface)
        if transaction.to_address is None:
            to_address = 'Null'
        else:
            to_address = transaction.to_address

        if function_called == 'Null':
            insert_into_pg(schema=schema,
                           table=table,
                           columns='transaction_hash,'
                                   'block_number,'
                                   'created_at,'
                                   'block_gas_limit,'
                                   'block_gas_used,'
                                   'from_address,'
                                   'to_address,'
                                   'transaction_fee,'
                                   'gas,'
                                   'gas_price,'
                                   'cumulative_gas_used,'
                                   'effective_gas_price,'
                                   'gas_used, '
                                   'nonce,'
                                   'transaction_index,'
                                   'transaction_type,'
                                   'eth_amount,'
                                   'has_succeeded',
                           values=(transaction.txn_hash.hex(),
                                   int(block_instance.number),
                                   datetime.utcfromtimestamp(int(block_instance.timestamp))
                                   .strftime("%Y-%m-%d %H:%M:%S.%f"),
                                   int(block_instance.gas_limit),
                                   int(block_instance.gas_used),
                                   transaction.from_address,
                                   to_address,
                                   float(receipt.effective_gas_price)/1000000000000000000*int(receipt.gas_used),
                                   int(transaction.gas),
                                   float(transaction.gas_price)/1000000000000000000,
                                   int(receipt.cumulative_gas_used),
                                   float(receipt.effective_gas_price)/1000000000000000000,
                                   int(receipt.gas_used),
                                   int(transaction.nonce),
                                   int(transaction.transaction_index),
                                   transaction.type,
                                   float(transaction.value)/1000000000000000000,
                                   bool(receipt.status)),
                           database_cursor=database_cursor)
        else:
            insert_into_pg(schema=schema,
                           table=table,
                           columns='transaction_hash,'
                                   'block_number,'
                                   'created_at,'
                                   'block_gas_limit,'
                                   'block_gas_used, '
                                   'from_address,'
                                   'to_address,'
                                   'transaction_fee,'
                                   'gas,'
                                   'gas_price,'
                                   'cumulative_gas_used,'
                                   'effective_gas_price,'
                                   'gas_used,'
                                   'nonce,'
                                   'transaction_index,'
                                   'transaction_type,'
                                   'eth_amount,'
                                   'function_called,'
                                   'arguments,'
                                   'has_succeeded',
                           values=(transaction.txn_hash.hex(),
                                   int(block_instance.number),
                                   datetime.utcfromtimestamp(int(block_instance.timestamp))
                                   .strftime("%Y-%m-%d %H:%M:%S.%f"),
                                   int(block_instance.gas_limit),
                                   int(block_instance.gas_used),
                                   transaction.from_address,
                                   transaction.to_address,
                                   float(receipt.effective_gas_price) / 1000000000000000000 * int(receipt.gas_used),
                                   int(transaction.gas),
                                   float(transaction.gas_price)/1000000000000000000,
                                   int(receipt.cumulative_gas_used),
                                   float(receipt.effective_gas_price)/1000000000000000000,
                                   int(receipt.gas_used),
                                   int(transaction.nonce),
                                   int(transaction.transaction_index),
                                   transaction.type,
                                   float(transaction.value)/1000000000000000000,
                                   function_called,
                                   str(arguments).replace("'", '"'),
                                   bool(receipt.status)),
                           database_cursor=database_cursor)
