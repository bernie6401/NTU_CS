# Simple Buffer Overflow - 0x00
###### tags: `CTF` `PWN`

## Original Code
```cpp!
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    char buf[0x10];
    read(0, buf, 0x30); // It'll read the value that you input and store in buf with length=0x30
    system("pause");
    return 0;
}
```

* Note that you can check [this page](https://www.dotcpp.com/course/460) to know more about `read` function


## Dynamic Analysis - `x32dbg`
* This is the original entry point of this program.
![](https://imgur.com/DWOL9Hy.png)

* `0x00404185` is the `read` function that will catch the input string we entered. So, we step into this function and continued executing until `0x7655BFE5`.
![](https://imgur.com/8rZnZvV.png)

* <font color="FF0000">The most important part</font>
In order to trigger buffer overflow, we must enter the string that size is over 16 to overlap `ebp` and `eip` register.
![](https://imgur.com/3t5cfcB.png)

* If we enter a normal length string such as `aaaaaaaaaaaaaaaa`, the `eip` register will store `0x0040148A` and finish the program normally.
![](https://imgur.com/RECKqeR.png)

* How about we enter 32 `a` characters?
The `ebp` and `eip` register will be overlapped by `0x61616161`(`aaaaaaaaa`) so that we can control the program flow by overlapping a specific address.
![](https://imgur.com/Kwly9MZ.png)

## Reference
[PWN basic](https://youtu.be/8zO47WDUdIk)
