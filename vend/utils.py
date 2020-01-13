#!/usr/bin/python3
import random
from .models import Token, Reversal


def get_sec_normal():
    token = Token.objects.order_by('seq', '-created').distinct('seq').first()
    if token is None:
        new_seq = "00001"
        return new_seq
    else:
        sequence = int(token.seq)
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
    message = data.decode('utf-8', 'backslashreplace')
    return message[2:]


def un_wrap_reverse(data):
    message = data.decode('utf-8', 'backslashreplace')
    return message[2:]
