import random

from secret import FLAG

state = random.randint(0, 1 << 64)

def getbit():
    global state
    state <<= 1
    if state & (1 << 64):
        state ^= 0x1da785fc480000001
        return 1
    return 0

flag = list(map(int, ''.join(["{:08b}".format(c) for c in FLAG])))
output = []
for _ in range(len(flag) + 70):
    for __ in range(36):
        getbit()
    output.append(getbit())

for i in range(len(flag)):
    output[i] ^= flag[i]

print(output)
