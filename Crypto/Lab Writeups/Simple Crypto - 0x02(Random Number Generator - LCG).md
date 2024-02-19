# Simple Crypto - 0x02(Random Number Generator - LCG)
###### tags: `CTF` `Crypto` `eductf`

## Background
Linear Congruential Generator:
![](https://i.imgur.com/pCTWEcO.png)

## Analysis
LCG Formula
$$
\begin{aligned}
Unknown: S_0&=Seed,\  A,\  B,\  m = 2^{32} \\
Given: S_1&,\  S_2,\  S_3\\
S_1 &\equiv (AS_0\ +\ B)\ \%\ m\\
S_2 &\equiv (AS_1\ +\ B)\ \%\ m\\
S_3 &\equiv (AS_2\ +\ B)\ \%\ m\\
\end{aligned}
$$

Derived A
$$
\begin{aligned}
&\left\{ 
  \begin{array}{c}
    S_2 &\equiv (AS_1\ +\ B)\ \%\ m\\
    S_3 &\equiv (AS_2\ +\ B)\ \%\ m
  \end{array}
\right.
\ \ \ \ \ \ minus \ two \ formula\ \\
&\to (S_2-S_3) \equiv (AS_1\ +\ B)\ \%\ m-(AS_2\ +\ B)\ \%\ m \\
&\to (S_2-S_3)\ \% \ m\equiv [(AS_1\ +\ B)\ \%\ m-(AS_2\ +\ B)\ \%\ m]\ \%\ m \\
&\to (S_2-S_3)\ \% \ m\equiv [(AS_1\ +\ B)-(AS_2\ +\ B)]\ \%\ m \\
&\to (S_2-S_3)\ \% \ m\equiv \ A\ (S_1-S_2)\ \ \%\ m =(S_2-S_3)\\
A&=((S_2-S_3)(S_1-S_2)^{-1})\ \%\ m
\end{aligned}
$$

Note
$$
\begin{aligned}
a\ \%\ m&=\ b \\
a\ \%\ m&=\ b \ \%\ m= \ b\\
\end{aligned}
$$

Derive B
$$
B=(S_2\ -\ AS_1)\ \%\ m
$$

Derive m
$$
m=gcd((t_{n+1}t_{n-1}-t_n^2),(t_nt_{n-2}-t_{n-1}^2))
$$
## Implement Code
```python=
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
```

## Exploit
[密码学——LCG算法 公式2](https://goodapple.top/archives/404)
```python=30
# Exploit it
# A
A = (S[1] - S[2]) * inverse((S[0] - S[1]), rng.m) % rng.m
print('Exploit A = ', A)

# B
B = (S[2] - A * S[1]) % rng.m
print('Exploit B = ', B)
```

## Reference
[getrandbits method](https://www.w3schools.com/python/ref_random_getrandbits.asp)