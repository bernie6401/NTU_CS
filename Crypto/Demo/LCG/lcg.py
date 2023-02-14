import random
from Crypto.Util.number import inverse
import math

# Encrypt something
class LCG():
    def __init__(self, seed) -> None:
        self.state = seed
        self.m = 2**32
        self.A = random.getrandbits(32) | 1
        self.B = random.getrandbits(32) | 1
    
    def getbits(self):
        self.clock()
        return self.state

    def clock(self):
        # self.tmp = (self.A * self.state + self.B) // self.m
        self.state = (self.A * self.state + self.B) % self.m
        # print('tmp = ', self.tmp)

rng = LCG(6401)
print('A = ', rng.A, 'B = ', rng.B, 'm = ', rng.m)

S = []
for i in range(3):
    S.append(rng.getbits())

print('S = ', S)

# Exploit it
# A
A = (S[1] - S[2]) * inverse((S[0] - S[1]), rng.m) % rng.m
print('Exploit A = ', A)

# B
B = (S[2] - A * S[1]) % rng.m
print('Exploit B = ', B)

# m
# m = math.gcd()