import binascii

enc_flag = [0xB5, 0xE5, 0x8D, 0xBD, 0x5C, 0x46, 0x36, 0x4E, 0x4E, 0x1E, 0x0E, 0x26, 0xA4, 0x1E, 0x0E, 0x4E, 0x46, 0x06, 0x16, 0xAC, 0xB4, 0x3E, 0x4E, 0x16, 0x94, 0x3E, 0x94, 0x8C, 0x94, 0x8C, 0x9C, 0x4E, 0xA4, 0x8C, 0x2E, 0x46, 0x8C, 0x6C]

def pad(m):
    length = 0
    if len(m) % 8 != 0:
        length = 8-len(m) % 8
    return '0' * length + m

FLAG = []
for i in range(len(enc_flag)):
    enc_flag[i] ^= 0x87
    tmp = pad(bin(enc_flag[i])[2:])
    tmp = hex(int(tmp[-3:] + tmp[:-3], 2))
    FLAG.append(binascii.unhexlify(tmp[2:]).decode())

print("".join(FLAG))