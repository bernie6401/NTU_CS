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