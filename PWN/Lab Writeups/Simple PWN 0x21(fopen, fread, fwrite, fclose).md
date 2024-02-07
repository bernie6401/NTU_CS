# Simple PWN 0x21(fopen, fread, fwrite, fclose)
###### tags: `CTF` `PWN` `eductf`

Version: Ubuntu 20.04

## Original Code
:::spoiler fopen
```cpp=
#include <fcntl.h>
#include <stdio.h>

int main()
{
    FILE *fp;
    fp = fopen("./test", "r");
    fclose(fp);

    return 0;
}
```
:::

:::spoiler fread
```cpp=
#include <fcntl.h>
#include <stdio.h>

int main()
{
    FILE *fp;
    char buf[0x10];

    fp = fopen("./test", "r");
    fread(buf, 0x1, 0x10, fp);
    fclose(fp);

    return 0;
}
```
:::

:::spoiler fwrite
```cpp=
#include <fcntl.h>
#include <stdio.h>

int main()
{
    FILE *fp;
    char buf[0x10] = "TEST!!";

    fp = fopen("./test_write", "r");
    fread(buf, 0x1, 0x10, fp);
    fclose(fp);

    return 0;
}
```
:::

:::spoiler fclose
```cpp=

```
:::

## Analyze
### fopen
* Flow chart
    ![](https://i.imgur.com/CZgCWFL.png)
1. `fopen` - main()
    ```baah!
    ...
    <main+26>    call   fopen@plt    <fopen@plt>
    pwndbg> si
    ```
2. `malloc` - `iofopen.c`
    ```bash!
    <__fopen_internal+26>    call   malloc@plt	<malloc@plt> # Size: 0x1d8
    pwndbg> heap
    ...
    Allocated chunk | PREV_INUSE
    Addr: 0x555555559290
    Size: 0x1e1
    ...
    ```
    :::spoiler `new_f`
    ```bash!
    pwndbg> p *new_f
    $2 = {
      fp = {
        file = {
          _flags = 0,
          _IO_read_ptr = 0x0,
          _IO_read_end = 0x0,
          _IO_read_base = 0x0,
          _IO_write_base = 0x0,
          _IO_write_ptr = 0x0,
          _IO_write_end = 0x0,
          _IO_buf_base = 0x0,
          _IO_buf_end = 0x0,
          _IO_save_base = 0x0,
          _IO_backup_base = 0x0,
          _IO_save_end = 0x0,
          _markers = 0x0,
          _chain = 0x0,
          _fileno = 0,
          _flags2 = 0,
          _old_offset = 0,
          _cur_column = 0,
          _vtable_offset = 0 '\000',
          _shortbuf = "",
          _lock = 0x0,
          _offset = 0,
          _codecvt = 0x0,
          _wide_data = 0x0,
          _freeres_list = 0x0,
          _freeres_buf = 0x0,
          __pad5 = 0,
          _mode = 0,
          _unused2 = '\000' <repeats 19 times>
        },
        vtable = 0x0
      },
      lock = {
        lock = 0,
        cnt = 0,
        owner = 0x0
      },
      wd = {
        _IO_read_ptr = 0x0,
        _IO_read_end = 0x0,
        _IO_read_base = 0x0,
        _IO_write_base = 0x0,
        _IO_write_ptr = 0x0,
        _IO_write_end = 0x0,
        _IO_buf_base = 0x0,
        _IO_buf_end = 0x0,
        _IO_save_base = 0x0,
        _IO_backup_base = 0x0,
        _IO_save_end = 0x0,
        _IO_state = {
          __count = 0,
          __value = {
            __wch = 0,
            __wchb = "\000\000\000"
          }
        },
        _IO_last_state = {
          __count = 0,
          __value = {
            __wch = 0,
            __wchb = "\000\000\000"
          }
        },
        _codecvt = {
          __cd_in = {
            step = 0x0,
            step_data = {
              __outbuf = 0x0,
              __outbufend = 0x0,
              __flags = 0,
              __invocation_counter = 0,
              __internal_use = 0,
              __statep = 0x0,
              __state = {
                __count = 0,
                __value = {
                  __wch = 0,
                  __wchb = "\000\000\000"
                }
              }
            }
          },
          __cd_out = {
            step = 0x0,
            step_data = {
              __outbuf = 0x0,
              __outbufend = 0x0,
              __flags = 0,
              __invocation_counter = 0,
              __internal_use = 0,
              __statep = 0x0,
              __state = {
                __count = 0,
                __value = {
                  __wch = 0,
                  __wchb = "\000\000\000"
                }
              }
            }
          }
        },
        _shortbuf = L"",
        _wide_vtable = 0x0
      }
    }
    ```
    :::
3. Initialize - `iofopen.c`
    ```cpp!
    ...
    _IO_no_init (&new_f->fp.file, 0, 0, &new_f->wd, &_IO_wfile_jumps);
    _IO_JUMPS (&new_f->fp) = &_IO_file_jumps;
    _IO_new_file_init_internal (&new_f->fp);
    ...
    ```
    :::spoiler `_IO_file_jumps`
    ```bash!
    pwndbg> p _IO_file_jumps
    $3 = {
      __dummy = 0,
      __dummy2 = 0,
      __finish = 0x7ffff7e87ff0 <_IO_new_file_finish>,
      __overflow = 0x7ffff7e88a00 <_IO_new_file_overflow>,
      __underflow = 0x7ffff7e886b0 <_IO_new_file_underflow>,
      __uflow = 0x7ffff7e899c0 <__GI__IO_default_uflow>,
      __pbackfail = 0x7ffff7e8ad40 <__GI__IO_default_pbackfail>,
      __xsputn = 0x7ffff7e87be0 <_IO_new_file_xsputn>,
      __xsgetn = 0x7ffff7e877a0 <__GI__IO_file_xsgetn>,
      __seekoff = 0x7ffff7e87010 <_IO_new_file_seekoff>,
      __seekpos = 0x7ffff7e89d60 <_IO_default_seekpos>,
      __setbuf = 0x7ffff7e868f0 <_IO_new_file_setbuf>,
      __sync = 0x7ffff7e86780 <_IO_new_file_sync>,
      __doallocate = 0x7ffff7e7b3b0 <__GI__IO_file_doallocate>,
      __read = 0x7ffff7e87bb0 <__GI__IO_file_read>,
      __write = 0x7ffff7e875f0 <_IO_new_file_write>,
      __seek = 0x7ffff7e86d70 <__GI__IO_file_seek>,
      __close = 0x7ffff7e868e0 <__GI__IO_file_close>,
      __stat = 0x7ffff7e875d0 <__GI__IO_file_stat>,
      __showmanyc = 0x7ffff7e8aed0 <_IO_default_showmanyc>,
      __imbue = 0x7ffff7e8aee0 <_IO_default_imbue>
    }
    ```
    :::
    * parse mode in [`fileops.c` - `_IO_new_file_fopen()`](https://elixir.bootlin.com/glibc/glibc-2.31/source/libio/fileops.c)
4. `__GI__IO_file_fopen` - `iofopen.c`
    ```bash!
    ...
    <__fopen_internal+120>             call   __GI__IO_file_fopen	<__GI__IO_file_fopen>
    	rdi: 0x5555555592a0 ◂— 0xfbad248c
        rsi: 0x555555556006 ◂— 0x747365742f2e /* './test' */
        rdx: 0x555555556004 ◂— 0x747365742f2e0072 /* 'r' */
        rcx: 0x1
    ```
5. `_IO_file_open` - `fileops.c`
    ```bash!
    <__GI__IO_file_fopen+188>    call   _IO_file_open	<_IO_file_open>
        rdi: 0x5555555592a0 ◂— 0xfbad248c
        rsi: 0x555555556006 ◂— 0x747365742f2e /* './test' */
        rdx: 0x0
        rcx: 0x1b6
    ```
6. `sys_open` - `open64.c`
    ```bash!
    <_IO_file_open+33>    call   open64	<open64>	# It'll return file number(fd)
        file: 0x555555556006 ◂— 0x747365742f2e /* './test' */
        oflag: 0x0 	# read only mode
        vararg: 0x1b6
        ...
        <open64+73>    syscall  <SYS_openat>
            fd: 0xffffff9c
            file: 0x555555556006 ◂— 0x747365742f2e /* './test' */
            oflag: 0x0
            vararg: 0x0
    ```
* Whole work flow
    :::spoiler work flow
    ```bash!
    <main+26>    call   fopen@plt	<fopen@plt>
        ...
        <__fopen_internal+26>    call   malloc@plt	<malloc@plt>
            size: 0x1d8
        ...
        <__fopen_internal+81>    call   _IO_no_init	<_IO_no_init>
        ...
        <__fopen_internal+103>    call   _IO_new_file_init_internal	<_IO_new_file_init_internal>
            rdi: 0x5555555592a0 ◂— 0xfbad0000
            ...
            <_IO_new_file_init_internal+25>    call   _IO_link_in	<_IO_link_in>
                rdi: 0x5555555592a0 ◂— 0xfbad240c
                rsi: 0xfbad0000
                rdx: 0x0
                rcx: 0x555555559390 ◂— 0x0
            ...
        <__fopen_internal+120>             call   __GI__IO_file_fopen	<__GI__IO_file_fopen>
            rdi: 0x5555555592a0 ◂— 0xfbad248c
            rsi: 0x555555556006 ◂— 0x747365742f2e /* './test' */
            rdx: 0x555555556004 ◂— 0x747365742f2e0072 /* 'r' */
            rcx: 0x1
            ...
        <__GI__IO_file_fopen+188>    call   _IO_file_open	<_IO_file_open>
            rdi: 0x5555555592a0 ◂— 0xfbad248c
            rsi: 0x555555556006 ◂— 0x747365742f2e /* './test' */
            rdx: 0x0
            rcx: 0x1b6
                ...
                <_IO_file_open+33>    call   open64	<open64>	# It'll return file number(fd)
                    file: 0x555555556006 ◂— 0x747365742f2e /* './test' */
                    oflag: 0x0 	# read only mode
                    vararg: 0x1b6
                    ...
                    <open64+73>    syscall  <SYS_openat>
                        fd: 0xffffff9c
                        file: 0x555555556006 ◂— 0x747365742f2e /* './test' */
                        oflag: 0x0
                        vararg: 0x0


    ```
    :::
    :::spoiler `*fp`
    ```bash!
    pwndbg> p *fp
    $4 = {
      _flags = -72539000,
      _IO_read_ptr = 0x0,
      _IO_read_end = 0x0,
      _IO_read_base = 0x0,
      _IO_write_base = 0x0,
      _IO_write_ptr = 0x0,
      _IO_write_end = 0x0,
      _IO_buf_base = 0x0,
      _IO_buf_end = 0x0,
      _IO_save_base = 0x0,
      _IO_backup_base = 0x0,
      _IO_save_end = 0x0,
      _markers = 0x0,
      _chain = 0x7ffff7fc45c0 <_IO_2_1_stderr_>,
      _fileno = 3,
      _flags2 = 0,
      _old_offset = 0,
      _cur_column = 0,
      _vtable_offset = 0 '\000',
      _shortbuf = "",
      _lock = 0x555555559380,
      _offset = -1,
      _codecvt = 0x0,
      _wide_data = 0x555555559390,
      _freeres_list = 0x0,
      _freeres_buf = 0x0,
      __pad5 = 0,
      _mode = 0,
      _unused2 = '\000' <repeats 19 times>
    }
    ```
    :::
### fread
* Flow chart
    ![](https://i.imgur.com/gESVUEE.png)

### fwrite
* Flow chart
    ![](https://i.imgur.com/IF94XNU.png)

### fclose
* Flow chart
    ![](https://i.imgur.com/nOpUw3e.png)
