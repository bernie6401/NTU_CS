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