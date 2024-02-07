# Simple PWN 0x17(UAF - leak information)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04

## UAF backgroud
[SS111-Pwn2](https://youtu.be/MwjSNFQIx0c)
[Advanced Binary Exploitation (Pwn) - Heap Exploitation](https://youtu.be/rMqvL9j0QaM?t=3009)
![](https://imgur.com/nFDhGiC.png)


## Original Code
```cpp!=
#include <stdio.h>
#include <stdlib.h>

int main()
{
    void *p1, *p2;
    p1 = malloc(0x30);
    p2 = malloc(0x30);

    free(p1);
    free(p2);

    puts(p2);
}
```
If we set the pointer to `NULL` after it was freed, then we can get some vital info. from this chunk.

## Analyze
* After malloc all pointer
![](https://imgur.com/HkEOJF0.png)
* After free `p1`
![](https://imgur.com/YqiGVeJ.png)
* After free `p2`, the data section will transfer to store metadata, and `fd` store the address of `p1` header
![](https://imgur.com/7XHGDdj.png)
![](https://imgur.com/lPuRywc.png)
* Thus, we print out the value of `p2`, we will leak something if it wasn't set `NULL` after it was freed
![](https://imgur.com/Sbw4brI.png)