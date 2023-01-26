#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

char name[0x80];

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    mprotect(0x403000, 0x1000, PROT_READ|PROT_WRITE|PROT_EXEC);

    char s[0x10];

    printf("Give me your name: ");
    read(0, name, 0x80);

    printf("Give me your ROP: ");
    read(0, s, 0x20);

    return 0;
}
