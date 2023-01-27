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