#! /usr/bin/python3
from Crypto.Cipher import AES
import os

# from secret import FLAG
FLAG = b'abcdefg'


def pad(data, block_size):
    data += bytes([0x80] + [0x00] * (15 - len(data) % block_size))
    return data # b'abcdefg\x80\x00\x00\x00\x00\x00\x00\x00\x00'

def unpad(data, block_size):
    if len(data) % block_size:  # block_size == 16
        raise ValueError

    padding_len = 0
    # Now, data == b'abcdefg\x80\x00\x00\x00\x00\x00\x00\x00\x00'
    for i in range(1, len(data) + 1):
        if data[-i] == 0x80:
            padding_len = i
            break
        elif data[-i] != 0x00:
            raise ValueError
    else:
        raise ValueError

    return data[:-padding_len]  # b'abcdefg'

key = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC)
ct = cipher.encrypt(pad(FLAG, AES.block_size))
iv = cipher.iv
print((iv + ct).hex())

while True:
    try:
        inp = bytes.fromhex(input().strip())
        iv, ct = inp[:16], inp[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        print("Well received :)")
    except ValueError:
        print("Something went wrong :(")
