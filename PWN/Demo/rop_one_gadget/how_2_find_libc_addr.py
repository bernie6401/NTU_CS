from pwn import *

libc = ELF("/usr/lib/gcc/x86_64-linux-gnu/11/../../../x86_64-linux-gnu/libc.a")
libc_binsh=libc.search("/bin/sh\x00").next()
