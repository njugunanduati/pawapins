#!/usr/bin/python3
import sys
import random
from .models import Token, Reversal


def get_sec_normal():
    token = Token.objects.order_by('seq', '-created').distinct('seq').first()
    if token is None:
        new_seq = 1
        return "0000" + str(new_seq)
    else:
        sequence = int(token.seq)
        sequence += 1
        return str(sequence)


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

