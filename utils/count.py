infura_request_counter = 0


def counter_up():
    global infura_request_counter
    infura_request_counter += 1
    if infura_request_counter == 2:
        print(f'Infura service was requested for the {infura_request_counter}nd time')
    elif infura_request_counter == 3:
        print(f'Infura service was requested for the {infura_request_counter}rd time')
    elif str(infura_request_counter)[-1] == '1':
        print(f'Infura service was requested for the {infura_request_counter}st time')
    else:
        print(f'Infura service was requested for the {infura_request_counter}th time')
