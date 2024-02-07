# Simple PWN - 0x14(Simple HEAP)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04
## HEAP background
[Advanced Binary Exploitation (Pwn) - Heap Exploitation](https://youtu.be/rMqvL9j0QaM)
[SS111-Pwn2](https://youtu.be/Xppj8lA04qQ)
## Allocate a memory
### Original Code
```cpp!=
#include <stdio.h>
#include <stdlib.h>

int main()
{
    void *ptr;
    ptr = malloc(0x30);
    return 0;
}
```
```bash!
$ sudo gcc -o simple_heap simple_heap.c -no-pie
```
### Analyze
* Before executing `malloc`, there is no `heap` space in memory layout
![](https://imgur.com/h9ibSyk.png)
* After...
![](https://imgur.com/mbE6KtK.png)
And the size is `0x21000` that is `135168 bytes = 132 kB` → <font color="FF0000">**main arena(大餅乾)**</font>

* `main arena`
![](https://imgur.com/ApxbFeY.png)
DON'T BE PANIC!!! We have useful tool to parse it automatically → `pwngdb` from [AngelBoy](https://github.com/scwuaptx/Pwngdb)
![](https://imgur.com/792Dyg0.png)


## How about if we free the memory?
### Original Code
```cpp!=
#include <stdio.h>
#include <stdlib.h>

int main()
{
    void *ptr;
    ptr = malloc(0x30);
    free(ptr)
    return 0;
}
```
* Note that `0x30`is for `Tcache bin` size
### Analyze
* Before freeing memory, we can observe the memory that system gave to us.
![](https://imgur.com/8Mt5ZpW.png)
The structure and meaning is as below. Header said we have no previous chunk(the first 8 bytes is `0x0`) and the size of current chunk is `0x40`. In addition, the last byte is `0001` means `p flag` is 1.
Moreover, the data section told us that the system actually gave us a memory with size `0x30`
![](https://imgur.com/gITdipF.png)
* After freeing...You can see that `0x40` has an address that we just free
![](https://imgur.com/ZuA3bIX.png)

## How about we malloc another 0x30 and free it later?
### Original Code
```cpp!
#include <stdio.h>
#include <stdlib.h>

int main()
{
    void *ptr, *ptr2;
    ptr = malloc(0x30);
    ptr2 = malloc(0x30);
    free(ptr2);
    free(ptr);
    return 0;
}
```
### Analyze
* After malloc, before free
![](https://imgur.com/hRyBYRW.png)
* After free..., it's a singly linked list(單向linked list)
![](https://imgur.com/Rd16xup.png)
* Observe the memory we free, the metadata of `ptr` point to the initial data section of `ptr2`
![](https://imgur.com/vwvh6Jc.png)
* In addition, the `PREV_INUSE bit` will maintain 1 even the previous chunk is free.
![](https://imgur.com/3mwYsaY.png)

### tcache_entry
Refer to [lecture - SS111-Pwn2](https://youtu.be/Xppj8lA04qQ?t=2653)
![](https://imgur.com/hiJyQnO.png)
So, we can use `heap` to check the situation
![](https://imgur.com/oazxtmX.png)
![](https://imgur.com/wbvn1Wn.png)
In addition, tcache_entry will point to the data section instead of header like other bin
![](https://imgur.com/JdgAuvp.png)


## Reference
[Advanced Binary Exploitation (Pwn) - Heap Exploitation](https://youtu.be/rMqvL9j0QaM)