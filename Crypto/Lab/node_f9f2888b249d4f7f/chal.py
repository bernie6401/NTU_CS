#! /usr/bin/python3
# some code is from CryptoHack's Elliptic Nodes
from Crypto.Util.number import inverse, bytes_to_long, isPrime
from collections import namedtuple
import random
import os

from secret import FLAG

p = 143934749405770267808039109533241671783161568136679499142376907171125336784176335731782823029409453622696871327278373730914810500964540833790836471525295291332255885782612535793955727295077649715977839675098393245636668277194569964284391085500147264756136769461365057766454689540925417898489465044267493955801
a = -3
b = 2

Point = namedtuple("Point", "x y")
O = 'Origin'

def check_point(P):
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p

def point_inverse(P):
    if P == O:
        return P
    return Point(P.x, -P.y % p)

def point_addition(P, Q):
    assert check_point(P)
    assert check_point(Q)
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*inverse(2*P.y, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * inverse((Q.x - P.x), p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    assert check_point(R)
    return R

def double_and_add(G, k):
    P = G
    R = O
    while k > 0:
        if k % 2 == 1:
            R = point_addition(R, P)
        P = point_addition(P, P)
        k = k // 2
    assert check_point(R)
    return R

flag = bytes_to_long(FLAG + os.urandom(120 - len(FLAG)))
x, y = 101806057140780850544714530443644783825785167075147195900696966628348944447492085252540090679241301721340985975519224144331425477628386574016040358648752353263802400527250163297781189749285392087154377684890287451078937692380556192126971669069015673662635561425735593795743852141232711066181542250670387203333, 21070877061047140448223994337863615306499412743288524847405886929295212764999318872250771845966630538832460153205159221566590942573559588219757767072634072564645999959084653451405037079311490089767010764955418929624276491280034578150363584012913337588035080509421139229710578342261017441353044437092977119013
G = Point(x, y)
F = double_and_add(G, flag)
print(F.x, F.y)