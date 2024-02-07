# Simple PWN - 0x15(Lab - `heapmath`)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04

## Original Code
:::spoiler code
```cpp!=
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    srand(time(NULL));

    void *tcache_chk[7]                = {0};
    unsigned char tcachebin[3][7]      = {0}; // 0x20, 0x30, 0x40
    unsigned int tcachebin_counts[4]   = {0};
    unsigned long tcache_size[7]       = {0};
    unsigned long tcache_free_order[7] = {0};

    puts("----------- ** tcache chall ** -----------");
    unsigned long tmp = 0;
    for (int i = 0; i < 7; i++) {
        tmp = (rand() % 0x21) + 0x10; // 0x10 ~ 0x30
        tcache_size[i] = tmp;
    }

    for (int i = 0; i < 7; i++) {
    repeat:
        tmp = rand() % 7;
        for (int j = 0; j < i; j++)
            if (tmp == tcache_free_order[j]) goto repeat;
        tcache_free_order[i] = tmp;
    }

    for (int i = 0; i < 7; i++) {
        tcache_chk[i] = malloc( tcache_size[i] );
        printf("char *%c = (char *) malloc(0x%lx);\n", 'A' + i, tcache_size[i]);
    }

    for (int i = 0; i < 7; i++) {
        int idx = tcache_free_order[i];
        free(tcache_chk[ idx ]);
        printf("free(%c);\n", 'A' + (unsigned char) idx);

        tmp = tcache_size[ idx ] - 0x8;
        if (tmp % 0x10)
            tmp = (tmp & ~0xf) + 0x20;
        else
            tmp += 0x10;

        unsigned int binidx = ((tmp - 0x20) / 0x10);
        unsigned int bincnt = tcachebin_counts[ binidx ];
        tcachebin[ binidx ][ bincnt ] = 'A' + (unsigned char) idx;
        tcachebin_counts[ binidx ]++;
    }

    char tmpbuf[0x100]   = {0};
    char ansbuf[3][0x100] = {0};
    for (int i = 0; i < 3; i++) {
        for (int j = 6; j >= 0; j--)
            if (tcachebin[i][j]) {
                sprintf(tmpbuf, "%c --> ", tcachebin[i][j]);
                strcat(ansbuf[i], tmpbuf);
            }
        strcat(ansbuf[i], "NULL");
    }
    puts("");
    for (int i = 0; i < 3; i++) {
        printf("[chunk size] 0x%x: ", (i+2) * 0x10);
        if (i == 0) {
            printf("%s\t(just send \"%s\")\n", ansbuf[i], ansbuf[i]);
        } else {
            printf("?\n> ");
            fgets(tmpbuf, 0x100, stdin);
            if (!strncmp(tmpbuf, ansbuf[i], strlen(ansbuf[i]))) {
                puts("Correct !");
            } else {
                puts("Wrong !");
                printf("Ans: \"%s\"\n", ansbuf[i]);
                exit(0);
            }
        }
    }

    puts("\n----------- ** address chall ** -----------");
    int cmp1 = 0;
    int cmp2 = 0;
    unsigned long ans_addr = 0;

    cmp1 = rand() % 7;
    while ((cmp2 = rand() % 7) == cmp1);
    if (cmp1 > cmp2) {
        tmp = cmp1;
        cmp1 = cmp2;
        cmp2 = tmp;
    }

    printf("assert( %c == %p );\n", 'A' + cmp1, tcache_chk[ cmp1 ]);
    printf("%c == ?\t(send as hex format, e.g. \"%p\")\n> ",
                'A' + cmp2, tcache_chk[ cmp1 ]);
    scanf("%s", tmpbuf);
    ans_addr = strtoul(tmpbuf, NULL, 16);

    if (ans_addr == (unsigned long) tcache_chk[ cmp2 ]) {
        puts("Correct !");
    } else {
        puts("Wrong !");
        printf("Ans: %p\n", tcache_chk[ cmp2 ]);
        exit(0);
    }

    puts("\n----------- ** index chall ** -----------");
    unsigned long *fastbin[2] = {0};
    unsigned long fastbin_size = 0;
    unsigned long secret_idx = 0, result_idx = 0, res = 0;

    fastbin_size = (rand() % 0x31) + 0x40; // 0x40 ~ 0x70
    fastbin_size &= ~0xf;
    fastbin[0] = (unsigned long *) malloc( fastbin_size );
    fastbin[1] = (unsigned long *) malloc( fastbin_size );
    
    printf("unsigned long *%c = (unsigned long *) malloc(0x%lx);\n", 'X', fastbin_size);
    printf("unsigned long *%c = (unsigned long *) malloc(0x%lx);\n", 'Y', fastbin_size);

    secret_idx = rand() % (fastbin_size / 8);
    fastbin[1][ secret_idx ] = 0xdeadbeef;
    result_idx = ((unsigned long)(&fastbin[1][ secret_idx ]) - (unsigned long)(&fastbin[0][0])) / 8;
    
    printf("Y[%lu] = 0xdeadbeef;\n", secret_idx);
    printf("X[?] == 0xdeadbeef\t(just send an integer, e.g. \"8\")\n> ");
    scanf("%lu", &res);

    if (fastbin[0][res] == 0xdeadbeef) {
        puts("Correct !");
    } else {
        puts("Wrong !");
        printf("Ans: %lu\n", result_idx);
        exit(0);
    }

    puts("\n----------- ** tcache fd chall ** -----------");
    free(fastbin[0]);
    free(fastbin[1]);
    printf("free(X);\nfree(Y);\nassert( Y == %p );\n", fastbin[1]);
    printf("fd of Y == ?\t(send as hex format, e.g. \"%p\")\n> ", fastbin[1]);
    scanf("%s", tmpbuf);
    ans_addr = strtoul(tmpbuf, NULL, 16);

    if (ans_addr == *fastbin[1]) {
        puts("Correct !");
    } else {
        puts("Wrong !");
        printf("Ans: 0x%lx\n", *fastbin[1]);
        exit(0);
    }

    puts("\n----------- ** fastbin fd chall (final) ** -----------");
    puts("[*] Restore the chunk to X and Y");
    printf("%c = (unsigned long *) malloc(0x%lx);\n", 'Y', fastbin_size);
    printf("%c = (unsigned long *) malloc(0x%lx);\n", 'X', fastbin_size);
    fastbin[1] = malloc(fastbin_size);
    fastbin[0] = malloc(fastbin_size);
    printf("[*] Do something to fill up 0x%lx tcache\n...\n[*] finish\n", fastbin_size + 0x10);
    void *tmpchk[7];
    for (int i = 0; i < 7; i++)
        tmpchk[i] = malloc(fastbin_size);
    for (int i = 0; i < 7; i++)
        free(tmpchk[i]);
    printf("free(X);\nfree(Y);\nassert( Y == %p );\n", fastbin[1]);
    free(fastbin[0]);
    free(fastbin[1]);
    printf("fd of Y == ?\t(send as hex format, e.g. \"%p\")\n> ", fastbin[1]);
    scanf("%s", tmpbuf);
    ans_addr = strtoul(tmpbuf, NULL, 16);

    if (ans_addr == *fastbin[1]) {
        puts("Correct !");
        memset(tmpbuf, 0, 0x31);
        
        int fd = open("/home/heapmath/flag", O_RDONLY);
        read(fd, tmpbuf, 0x30);
        close(fd);
        printf("Here is your flag: %s\n", tmpbuf);
    } else {
        puts("Wrong !");
        printf("Ans: 0x%lx\n", *fastbin[1]);
        exit(0);
    }
}

```
:::
* It's a test of `tcache and fastbin` background, therefore, just execute it directly!!!


## Questions
1. 
    ```bash!
    ----------- ** tcache chall ** -----------
    char *A = (char *) malloc(0x12);
    char *B = (char *) malloc(0x30);
    char *C = (char *) malloc(0x13);
    char *D = (char *) malloc(0x23);
    char *E = (char *) malloc(0x20);
    char *F = (char *) malloc(0x28);
    char *G = (char *) malloc(0x13);
    free(B);
    free(A);
    free(F);
    free(C);
    free(D);
    free(G);
    free(E);

    [chunk size] 0x20: G --> C --> A --> NULL       (just send "G --> C --> A --> NULL")
    [chunk size] 0x30: ?
    [chunk size] 0x40: ?
    ```
    Sol. 
    First, try to compute every char malloc size
    A → $align(0x12 - 0x8 + 0x10) = 0x20$
    B → $align(0x30 - 0x8 + 0x10) = 0x40$
    C → $align(0x13 - 0x8 + 0x10) = 0x20$
    D → $align(0x23 - 0x8 + 0x10) = 0x30$
    E → $align(0x20 - 0x8 + 0x10) = 0x30$
    F → $align(0x28 - 0x8 + 0x10) = 0x30$
    G → $align(0x13 - 0x8 + 0x10) = 0x20$

    Then, the sequence of the free char is B→A→F→C→D→G→E, according to FILO ruls(stack)
    ![](https://imgur.com/TZhy6b9.png)
    <font color="FF0000">
    The sequence of 0x30: E --> D --> F --> NULL
    The sequence of 0x30: B --> NULL
    </font>
2. 
    ```bash!
    ----------- ** address chall ** -----------
    assert( A == 0x563d3e2b72a0 );
    F == ?  (send as hex format, e.g. "0x563d3e2b72a0")
    ```
    Sol. Just accumulate the size
    A == 0x563d3e2b72a0
    B == A + 0x20 == 0x563d3e2b72c0
    C == B + 0x40 == 0x563d3e2b7300
    D == C + 0x20 == 0x563d3e2b7320
    E == D + 0x30 == 0x563d3e2b7350
    <font color="FF0000">F == E + 0x30 == 0x563d3e2b7380</font>
    G == F + 0x30 == 0x563d3e2b73b0
3. 
    ```bash!
    ----------- ** index chall ** -----------
    unsigned long *X = (unsigned long *) malloc(0x60);
    unsigned long *Y = (unsigned long *) malloc(0x60);
    Y[8] = 0xdeadbeef;
    X[?] == 0xdeadbeef      (just send an integer, e.g. "8")
    ```
    Sol. 
    `X` has $align(0x60 - 0x8 + 0x10) = 0x70$ size of malloc address
    `Y` has $align(0x60 - 0x8 + 0x10) = 0x70$ size of malloc address
    In addition these two memory are connected together
    Thus, `X` has `7*2=14` 8 bytes and `0xdeadbeef` is at the 4th position of Y
    Therefore, the answer is <font color="FF0000">$14+8=22$</font>
    ![](https://imgur.com/H2gp0r4.png)
4. 
    ```bash!
    ----------- ** tcache fd chall ** -----------
    free(X);
    free(Y);
    assert( Y == 0x563d3e2b7440 );
    fd of Y == ?    (send as hex format, e.g. "0x563d3e2b7440")
    ```
    Sol. Just minus the size of Y
    From the last question, we can know that the memory space of `X` and `Y` are connected together, in addition, the `fd` of `Y` point to `X's` data section
    ![](https://imgur.com/AGYaISV.png)
    Thus, the answer is <font color="FF0000">$0x563d3e2b7440 - 0x10 - 0x60 = 0x563d3e2b73d0$</font>
5. 
    ```bash!
    ----------- ** fastbin fd chall (final) ** -----------
    [*] Restore the chunk to X and Y
    Y = (unsigned long *) malloc(0x60);
    X = (unsigned long *) malloc(0x60);
    [*] Do something to fill up 0x70 tcache
    ...
    [*] finish
    free(X);
    free(Y);
    assert( Y == 0x563d3e2b7440 );
    fd of Y == ?    (send as hex format, e.g. "0x563d3e2b7440")
    ```
    Sol. When `tcache` is full, the free chunk will be put into other bin, such as `fastbin`.
    According to the lecture description of `fastbin` structure, the answer is
    <font color="FF0000">$0x563d3e2b7440 - 0x10 - 0x70 = 0x563d3e2b73c0$</font>
    ![](https://imgur.com/nykXyGP.png)

    ![](https://imgur.com/DfWnXT0.png)

## Reference
[SS111-Pwn2](https://youtu.be/00IkLtMWGWA)