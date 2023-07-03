first_for_loop = [190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227]

second_for_loop = [239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

enc_flag = [0xE7, 0xE3, 0x72, 0x78, 0xAC, 0x90, 0x90, 0x7C, 0x90, 0xAC, 0xB1, 0xA6, 0xA4, 0x9E, 0xA7, 0xA2, 0xAC, 0x90, 0xB9, 0xB2, 0xBF, 0xBB, 0xBD, 0xB6, 0xAB, 0x90, 0xBA, 0xB4, 0x90, 0xBF, 0xC0, 0xC0, 0xC4, 0xCA, 0x95, 0xED, 0xC0, 0xB2]


FLAG = []

for i in range(38):
    if enc_flag[i] - second_for_loop[i] < 0:
        tmp = hex(first_for_loop[i] ^ (enc_flag[i] - second_for_loop[i] + 0x100))[2:]
    else:
        tmp = hex(first_for_loop[i] ^ (enc_flag[i] - second_for_loop[i]))[2:]


    FLAG.append(bytes.fromhex(tmp).decode('cp437'))

print("".join(FLAG))