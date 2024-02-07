# Simple PWN 0x16(simple_smallbin)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04
## Background
![](https://imgur.com/teWNhbh.png)

![](https://imgur.com/kCTN7cs.png)
## Original Code
:::spoiler code
```cpp!=
#include <stdio.h>
#include <stdlib.h>

int main()
{
    void *ptrs[7];
    void *smallbin;
    int i;

    for (i = 0; i < 7; i++)
        ptrs[i] = malloc(0x108); // 0x110 chunk size

    smallbin = malloc(0x108);
    malloc(0x18);

    // aim to fill up tcache
    while(i)
        free(ptrs[--i]);
    
    free(smallbin);
    // trigger unsorted bin dispatch
    malloc(0x870);

    return 0;
}
```
:::
### Description & Analyze
* First things first, the program will call malloc to get `0x108`*8(`0x110 chunk size`)
![](https://imgur.com/dW8WU8v.png)
* Then free the all chunks
When `tcache` is fill and chunk size > `0x80`, it'll be put into `Unsorted bin`
![](https://imgur.com/QNS1mao.png)
![](https://imgur.com/oBCkql8.png)
* And now, if we malloc a new space with size equal `0x870`
According to the flow chart, when the malloc size over `0x410`, it'll find `Unsorted bin` first, and now, `Unsorted bin` has no suitable chunk, thus find `large bin` further. Unfortunately, it still has no suitable chunk for the user, split the memory from `top chunk`
```bash!
>pwndbg heap
...
Allocated chunk | PREV_INUSE
Addr: 0x555555559b30
Size: 0x881

Top chunk | PREV_INUSE
Addr: 0x55555555a3b0
Size: 0x1fc51
```
* <font color="FF0000">**Note that**</font>, the interesting thing is when we free `smallbin`, the process put it in `Unsorted bin`. And when we malloc `0x870`, the process found that `Unsorted bin` has no suitable chunk for the user, then it'll put `smallbin(0x110)` to where it should be → `smallbins`
    * Before malloc `0x870` and after free `smallbin(0x110)`
    ![](https://imgur.com/S1mQQ0X.png)
    * After malloc `0x870`
    ![](https://imgur.com/54D3JnE.png)