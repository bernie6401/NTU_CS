# Simple Welcome 0x01(Lab - Let's meet at class)
## Description
Crypto part of homework 0. The key space is $10^{15}$. I used my supercomputer(i5 7th gen) to solve it in about 10 minutes. It's impossible for you guys to enumerate all the keys in 2 weeks, or maybe you can... (Use `pip3 install pycryptodome` to install Crypto)
## Source Code
:::spoiler Source
```python
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
```
:::
:::spoiler
```
p = 92017932396773207330365205210913184771249549355771692523246399384571269833668487945963934319507538171501041280674304304879328757539798699280378034748542218248740777575679398093116579809607067129824965250071416089841516538588253944223235904445546895574651603636188746948921937704060334290364304972412697492577
enc = 87051682992840829567429886737255563980229964191963649650455667117285375334750716083826527488071966389632402954644144719710970265754062176648776448421065665281172133368294041777397049228273163978348132440822019295870429065335674151133125629968366491582233750452365390672536361224322642295053741696809519283644
hint = 112112804524582393858675176460595338484428048338611753655869733059768929120327158352572131172253127933611583356499525126040647290513660017529498493355846656594143774393256151536590212031416153303085867445488047592792290033548349001067687775149867134619114482370143917491889371548968347491490942978508386339813
```
:::
## Recon
這一題也是看了別人的WP[^wp_1]，有了一些想法，其實題目的敘述有一點點玄機(但我當時沒想到)，因為題目有提到key space是$10^{15}$，因為看了一下簡單的source code，他是創了五把key
$$
key_1 \leftarrow Rand(2, 1000)^{65537}\ \% \ p\\
key_2 \leftarrow Rand(1002, 2000)^{65537}\ \% \ p\\
key_3 \leftarrow Rand(2002, 3000)^{65537}\ \% \ p\\
key_4 \leftarrow Rand(3002, 4000)^{65537}\ \% \ p\\
key_5 \leftarrow Rand(4002, 5000)^{65537}\ \% \ p\\
$$
再分別用這五把key進行運算$enc=flag*key\ \%\ p$
乍看之下好像很難，但其實掌握題目講到的縮小key space的角度出發就會有一點概念要用MITM attack，畢竟他還有給$hint=key_1 \oplus  key_2 \oplus key_3 \oplus key_4 \oplus key_5$這個hint
具體來說會變成
$$
hint\oplus key_5\oplus key_4\oplus key_3=key_1\oplus key_2
$$
而TA也有給$key_5=pow(4668, 65537, p)$，代表key space真的減少超多($10^6$)
## Exploit
:::info
不同的寫法所處理的time complexity會不一樣
:::
```python!
from tqdm import trange
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
import numpy as np
import gmpy2

p = 92017932396773207330365205210913184771249549355771692523246399384571269833668487945963934319507538171501041280674304304879328757539798699280378034748542218248740777575679398093116579809607067129824965250071416089841516538588253944223235904445546895574651603636188746948921937704060334290364304972412697492577
enc = 87051682992840829567429886737255563980229964191963649650455667117285375334750716083826527488071966389632402954644144719710970265754062176648776448421065665281172133368294041777397049228273163978348132440822019295870429065335674151133125629968366491582233750452365390672536361224322642295053741696809519283644
hint = 112112804524582393858675176460595338484428048338611753655869733059768929120327158352572131172253127933611583356499525126040647290513660017529498493355846656594143774393256151536590212031416153303085867445488047592792290033548349001067687775149867134619114482370143917491889371548968347491490942978508386339813

key_1 = [pow(i, 65537, p) for i in range(2, 1001)]
key_2 = [pow(i, 65537, p) for i in range(1002, 2001)]
key_3 = [pow(i, 65537, p) for i in range(2002, 3001)]
key_4 = [pow(i, 65537, p) for i in range(3002, 4001)]
key_5 = pow(4668, 65537, p)

first_xor_result = {}
for i in trange(len(key_1)):
    for j in range(len(key_2)):
        first_xor_result[key_1[i] ^ key_2[j]] = [i, j]
 
second_xor_result = {}
tmp = key_5 ^ hint
for i in trange(len(key_3)):
    for j in range(len(key_4)):
        second_xor_result[key_3[i] ^ key_4[j] ^ tmp] = [i, j]
        if key_3[i] ^ key_4[j] ^ tmp in first_xor_result:
            print(f"j = {j}")
            result = key_3[i] ^ key_4[j] ^ tmp
            print(f"result = {result}")
            break

key_1_arg = first_xor_result[result][0]
key_2_arg = first_xor_result[result][1]
key_3_arg = second_xor_result[result][0]
key_4_arg = second_xor_result[result][1]

assert key_1[key_1_arg] ^ key_2[key_2_arg] ^ key_3[key_3_arg] ^ key_4[key_4_arg] ^ key_5 == hint

flag = enc * inverse(key_1[key_1_arg], p) % p
flag = flag * inverse(key_2[key_2_arg], p) % p
flag = flag * inverse(key_3[key_3_arg], p) % p
flag = flag * inverse(key_4[key_4_arg], p) % p
flag = flag * inverse(key_5, p) % p

print(long_to_bytes(flag))
```

Flag: `FLAG{enCrypTIon_wI7H_A_kEy_i5_N0t_secur3_7Hen_h0w_ab0u7_f1ve_Keys}`
## Reference
[^wp_1]:[Write Up from eric070021](https://hackmd.io/@eric070021/r1UnR5KWi)