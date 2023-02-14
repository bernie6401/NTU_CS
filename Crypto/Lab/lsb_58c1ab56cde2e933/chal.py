#! /usr/bin/python3
from Crypto.Util.number import bytes_to_long, getPrime
import os

from secret import FLAG

p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

m = bytes_to_long(FLAG + os.urandom(256 - len(FLAG)))
assert m < n
enc = pow(m, e, n)
print(n)
print(e)
print(enc)
while True:
    inp = int(input().strip())
    pt = pow(inp, d, n)
    print(pt % 3)