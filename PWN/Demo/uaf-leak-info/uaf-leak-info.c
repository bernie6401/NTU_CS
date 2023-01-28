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