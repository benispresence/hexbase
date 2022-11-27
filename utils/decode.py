import sys
from eth_utils import to_hex

import json
from configs.web3 import get_local_node_conn

web3 = get_local_node_conn()


def decode_tuple(t, target_field):
    output = dict()
    for i in range(len(t)):
        if isinstance(t[i], (bytes, bytearray)):
            output[target_field[i]['name']] = to_hex(t[i])
        elif isinstance(t[i], tuple):
            output[target_field[i]['name']] = decode_tuple(t[i], target_field[i]['components'])
        else:
            output[target_field[i]['name']] = t[i]
    return output


def decode_list_tuple(l, target_field):
    output = l
    for i in range(len(l)):
        output[i] = decode_tuple(l[i], target_field)
    return output


def decode_list(l):
    output = l
    for i in range(len(l)):
        if isinstance(l[i], (bytes, bytearray)):
            output[i] = to_hex(l[i])
        else:
            output[i] = l[i]
    return output


def convert_to_hex(arg, target_schema):
    """
    utility function to convert byte codes into human-readable and json serializable data structures
    """
    output = dict()
    for k in arg:
        if isinstance(arg[k], (bytes, bytearray)):
            output[k] = to_hex(arg[k])
        elif isinstance(arg[k], list) and len(arg[k]) > 0:
            target = [a for a in target_schema if 'name' in a and a['name'] == k][0]
            if target['type'] == 'tuple[]':
                target_field = target['components']
                output[k] = decode_list_tuple(arg[k], target_field)
            else:
                output[k] = decode_list(arg[k])
        elif isinstance(arg[k], tuple):
            target_field = [a['components'] for a in target_schema if 'name' in a and a['name'] == k][0]
            output[k] = decode_tuple(arg[k], target_field)
        else:
            output[k] = arg[k]
    return output


def decode_tx(address, input_data, abi, web3_contract):
    if abi is not None:
        try:
            if isinstance(abi, str):
                abi = json.loads(abi)
            func_obj, func_params = web3_contract.decode_function_input(input_data)
            target_schema = [a['inputs'] for a in abi if 'name' in a and a['name'] == func_obj.fn_name][0]
            decoded_func_params = convert_to_hex(func_params, target_schema)
            return func_obj.fn_name, json.dumps(decoded_func_params), json.dumps(target_schema)
        except:
            e = sys.exc_info()[0]
            return 'decode error', repr(e), None
    else:
        return 'no matching abi', None, None


def decode_contract_input(abi, contract_address, contract_input, web3_contract):
    function_details = decode_tx(contract_address, contract_input, abi, web3_contract)
    try:
        function = function_details[0]
        args = json.loads(function_details[1])
    except json.decoder.JSONDecodeError as error:
        function = 'Null'
        args = 'Null'
        print(f'json.decoder.JSONDecodeError: {error}')
        print('Transaction Input was replaced with the string value "Null".')
    return function, args
