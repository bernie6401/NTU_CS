from Crypto.Util.number import bytes_to_long, getPrime
import random
import math
import os

from secret import FLAG

FLAG += os.urandom(128 - len(FLAG))
flag = bytes_to_long(FLAG)
p = getPrime(1024)
keys = [pow(random.randint(1000 * i + 2, 1000 * (i+1) ), 65537, p) for i in range(5)]
enc = flag
for i in range(5):
    enc = enc * keys[i] % p

hint = keys[0] ^ keys[1] ^ keys[2] ^ keys[3] ^ keys[4]

print('p =', p)
print('enc =', enc)
print('hint =', hint)