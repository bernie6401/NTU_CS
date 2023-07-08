#! /usr/bin/python3
from hashlib import sha256
from Crypto.Util.number import bytes_to_long
from sage.all import EllipticCurve, Zmod
import random
import os

from secret import FLAG

# NIST P-256
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
E = EllipticCurve(Zmod(p), [a, b])

G = E(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
n = G.order()
d = bytes_to_long(FLAG + os.urandom(31 - len(FLAG)))
assert d < n
P = d * G

def sign(m):
    h = bytes_to_long(sha256(m).digest())
    k = random.randint(0, 1 << 120)
    x = (k * G).xy()[0]
    r = int(x) % n
    s = pow(k, -1, n) * (h + d * r) % n
    return r, s

msg = [b"Hello, hacker!", b"Try to get my private key!!"]
print(p, a, b)
print(n)
print(G.xy())
print(P.xy())
print(sign(msg[0]))
print(sign(msg[1]))