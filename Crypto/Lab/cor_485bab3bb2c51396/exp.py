import random
from tqdm import trange
import base64

def initialize():
    # Import output file(our cipher flag)
    File_path = "//wsl.localhost/Ubuntu-20.04/home/sbk6401/NTUCS/Crypto/Lab/cor_485bab3bb2c51396/output.txt"
    f = open(File_path, "r")
    f = f.read().split(',')

    # The first 232 is flag with encrypted
    cipher_text = []
    cipher_flag = []
    for i in range(len(f)):
        if i < 232:
            cipher_flag.append(int(f[i]))
        else:
            cipher_text.append(int(f[i]))
    # print(cipher_flag, cipher_text)
    return cipher_flag, cipher_text

def cal_correlation(a, b):
    count = 0
    for i in range(200):
        if a[i] == b[i]:
            count += 1
    return count / 200

def decimalToBinary(n):
    return bin(n).replace("0b", "")

class LFSR:
    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        f = sum([self._state[i] for i in self._tap]) & 1
        x = self._state[0]
        self._state = self._state[1:] + [f]
        return x

class triLFSR:
    def __init__(self, lfsr1, lfsr2, lfsr3):
        self.lfsr1 = lfsr1
        self.lfsr2 = lfsr2
        self.lfsr3 = lfsr3

    def getbit(self):
        x1 = self.lfsr1.getbit()
        x2 = self.lfsr2.getbit()
        x3 = self.lfsr3.getbit()
        return x2 if x1 else x3

def guess_state(state_size_pow, tap, cipher_text):
    guess_state = [0 for _ in range(state_size_pow)]  # Initial guess state
    result = []

    for state in trange(2**state_size_pow):
        guess_text = []
        lfsr = LFSR(tap, guess_state)

        for _ in range(232):
            lfsr.getbit()

        for _ in range(200):
            guess_text.append(lfsr.getbit())
            
        acc = cal_correlation(guess_text, cipher_text)
        if acc >= 0.70:
            # print(guess_state)
            result.append(guess_state)

        tmp = decimalToBinary(state + 1 + 3187671)
        guess_state = [0 for i in range(state_size_pow - len(tmp))] + [int(tmp[i]) for i in range(len(tmp))]

    return result

def final_guess(state_size_pow, tap, cipher_text, b_guess_state, c_guess_state):
    guess_state = [0 for _ in range(state_size_pow)]  # Initial guess state

    for state in trange(2**state_size_pow):
        guess_text = []
        lfsr1 = LFSR(tap[0], guess_state)
        lfsr2 = LFSR(tap[1], b_guess_state)
        lfsr3 = LFSR(tap[2], c_guess_state)
        cipher = triLFSR(lfsr1, lfsr2, lfsr3)

        for _ in range(232):
            cipher.getbit()

        for _ in range(200):
            guess_text.append(cipher.getbit())
            
        acc = cal_correlation(guess_text, cipher_text)
        if acc == 1:
            print(guess_state)
            return guess_state

        tmp = decimalToBinary(state + 1 + 13421773 * 8)
        guess_state = [0 for i in range(state_size_pow - len(tmp))] + [int(tmp[i]) for i in range(len(tmp))]

def binToHexa(n):
    bnum = int(n)
    temp = 0
    mul = 1
     
    # counter to check group of 4
    count = 1
     
    # char array to store hexadecimal number
    hexaDeciNum = ['0'] * 100
     
    # counter for hexadecimal number array
    i = 0
    while bnum != 0:
        rem = bnum % 10
        temp = temp + (rem*mul)
         
        # check if group of 4 completed
        if count % 4 == 0:
           
            # check if temp < 10
            if temp < 10:
                hexaDeciNum[i] = chr(temp+48)
            else:
                hexaDeciNum[i] = chr(temp+55)
            mul = 1
            temp = 0
            count = 1
            i = i+1
             
        # group of 4 is not completed
        else:
            mul = mul*2
            count = count+1
        bnum = int(bnum/10)
         
    # check if at end the group of 4 is not
    # completed
    if count != 1:
        hexaDeciNum[i] = chr(temp+48)
         
    # check at end the group of 4 is completed
    if count == 1:
        i = i-1
         
    # printing hexadecimal number
    # array in reverse order
    # print("\n Hexadecimal equivalent of {}:  ".format(n), end="")
    hex_string = ''
    while i >= 0:
        # print(end=hexaDeciNum[i])
        # print(hexaDeciNum[i])
        hex_string += hexaDeciNum[i]
        # print(base64.b64decode(hexaDeciNum[i]))
        i = i-1
    return hex_string

if __name__ == '__main__':
    cipher_flag, cipher_text = initialize()

    tap = [[0, 13, 16, 26], [0, 5, 7, 22], [0, 17, 19, 24]]
    B_guess_state = guess_state(23, tap[1], cipher_text)    # [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
    C_guess_state = guess_state(25, tap[2], cipher_text)  # [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0]
    A_guess_state = final_guess(27, tap, cipher_text, B_guess_state[0], C_guess_state[0]) # [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0]
    # B_guess_state = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
    # C_guess_state = [0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0]
    # A_guess_state = [1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0]


    lfsr1 = LFSR(tap[0], A_guess_state)
    lfsr2 = LFSR(tap[1], B_guess_state)
    lfsr3 = LFSR(tap[2], C_guess_state)
    cipher = triLFSR(lfsr1, lfsr2, lfsr3)

    output = []
    plaintext_bin = ''
    plaintext_hex = ''

    for i, b in enumerate(cipher_flag):
        plaintext_bin += str(cipher.getbit() ^ b)

        if (i+1) % 8 == 0:
            plaintext_hex += binToHexa(plaintext_bin)
            plaintext_bin = ''
    print(bytes.fromhex(plaintext_hex).decode())