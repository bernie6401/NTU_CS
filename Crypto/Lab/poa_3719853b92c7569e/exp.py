from pwn import *

r = remote('edu-ctf.zoolab.org', 10101)

ct = r.readline()[:-1].decode()
print(ct)

r.interactive()