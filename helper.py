import time
import random

TIME_INTERVAL = 60 * 60 * 1 # 1h
BLK_INTERVAL = 6

def little_endian_to_int(b):
    '''little_endian_to_int takes byte sequence as a little-endian number. Returns an integer'''
    return int.from_bytes(b, 'little')

def int_to_little_endian(n, length):
    '''endian_to_little_endian takes an integer and returns the little-endian byte sequence of length'''
    return  n.to_bytes(length, 'little')

def current_milli_time(): # get unix timestamp
    return int(round(time.time() * 1000))

def current_sec_time(): # get unix timestamp
    return int(round(time.time()))

def bits_to_target(bits):
    expoent = bits[-1]
    coefficient = little_endian_to_int(bits[:-1])
    return coefficient * 256 ** (expoent - 3)

def target_to_bits(target):
    '''Turns a target integer back into bits'''
    raw_bytes = target.to_bytes(32, 'big')
    raw_bytes = raw_bytes.lstrip(b'\x00')
    if raw_bytes[0] > 0x7f:
        exponent = len(raw_bytes) + 1
        coefficient = b'\x00' + raw_bytes[:2]
    else:
        exponent = len(raw_bytes)
        coefficient = raw_bytes[:3]
    new_bits = coefficient[::-1] + bytes([exponent])
    return new_bits

def calculate_new_bits(previous_bits, time_diff):
    if time_diff > TIME_INTERVAL * 4:
        time_diff = TIME_INTERVAL * 4
    if time_diff < TIME_INTERVAL // 4:
        time_diff = TIME_INTERVAL // 4
    new_target = bits_to_target(previous_bits) * time_diff // TIME_INTERVAL
    return target_to_bits(new_target)

def calc_difficulty(difficulty):
    lowest = 0xffff * 256**(0x1d - 3)
    target = round(lowest / difficulty)
    return target_to_bits(target)

def random_hexstring(length):
    result = bytes()
    for i in range(length):
        result += random.randint(0, 255).to_bytes(1, 'little')
    return result