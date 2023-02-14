import random

# from secret import FLAG

FLAG = b'00001111'

class LFSR:
    def __init__(self, tap, state):
        self._tap = tap
        self._state = state

    def getbit(self):
        # f is the new bit that append in last position
        f = sum([self._state[i] for i in self._tap]) & 1

        # x is the output bit
        x = self._state[0]
        
        # self._state is a new state
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
# These are the state of lfsr1, lfsr2, and lfsr3
A = [random.randrange(2) for _ in range(27)]
B = [random.randrange(2) for _ in range(23)]
C = [random.randrange(2) for _ in range(25)]
print(A, B, C)

# tap is a filter that decide the last bit is 1 or 0
tap1 = [0, 13, 16, 26]
tap2 = [0, 5, 7, 22]
tap3 = [0, 17, 19, 24]

lfsr1 = LFSR(tap1, A)
lfsr2 = LFSR(tap2, B)
lfsr3 = LFSR(tap3, C)
cipher = triLFSR(lfsr1, lfsr2, lfsr3)

# Transfer the flag to ascii code and expressed in binary
# e.g. FLAG = '00001111' → '3030303031313131' → '001100000011000000110000...00110001'(64 bits)
flag = map(int, ''.join(["{:08b}".format(c) for c in FLAG]))

output = []

for b in flag:
    # print(b)
    output.append(cipher.getbit() ^ b)

for _ in range(200):
    output.append(cipher.getbit())

# print(output)