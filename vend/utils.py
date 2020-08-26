#!/usr/bin/python3
import sys
import random
from .models import Transaction


def get_sec_normal():
    trans = Transaction.objects.all().last()
    if trans is None:
        new_seq = 1
        return "0" + str(new_seq)
    else:
        sequence = int(trans.seq)
        sequence += 1
        if len(str(sequence)) == 1:
            new_seq = "0000" + str(sequence)
        elif len(str(sequence)) == 2:
            new_seq = "000" + str(sequence)
        elif len(str(sequence)) == 3:
            new_seq = "00" + str(sequence)
        elif len(str(sequence)) == 4:
            new_seq = "0" + str(sequence)
        elif len(str(sequence)) == 5 and sequence == 99999:
            new_seq = "00001"
    return new_seq


def get_rand():
    ref = random.randint(100000000000, 999999999999)
    return ref


def wrap(msg):
    msg_len = len(msg)
    if msg_len > 65535:
        return "Message exceeds 65535 bytes."
    my_list = []
    first_byte = msg_len >> 8
    second_byte = msg_len
    my_list.append(first_byte % 256)
    my_list.append(second_byte % 256)

    # create an empty bytearray
    data_frame = bytearray([x for x in my_list])
    data_frame.extend(msg)
    return data_frame


def un_wrap(data):
    print("---un_wrap", data)
    if check_byte_length(data) >= 1452:
        message = data.decode('utf-8', 'backslashreplace')
        print("un_wrapped_", message[5:])
        return message[5:]
    else:
        message = data.decode('utf-8', 'backslashreplace')
        print("un__wrapped", message[2:])
        return message[2:]


def check_byte_length(data):
    return sys.getsizeof(data)

