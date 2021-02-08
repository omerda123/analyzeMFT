#!/usr/bin/python

# This is all Willi Ballenthin's. Saved me a lot of headaches


def parse_little_endian_signed_positive(buf):
    ret = 0
    for i, b in enumerate(buf):
        ret += b * (1 << (i * 8))
    return ret


def parse_little_endian_signed_negative(buf):
    ret = 0
    for i, b in enumerate(buf):
        ret += (ord(b) ^ 0xFF) * (1 << (i * 8))
    ret += 1

    ret *= -1
    return ret


def parse_little_endian_signed(buf):
    try:
        print(f"zzz {buf} {type(buf)} {type(buf[-1])}. {buf[-1]}")
        if not buf[-1] & 0b10000000:
            return parse_little_endian_signed_positive(buf)
        else:
            return parse_little_endian_signed_negative(buf)
    except Exception as e:
        # return ''
        raise e
