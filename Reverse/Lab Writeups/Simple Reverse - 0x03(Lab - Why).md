# Simple Reverse - 0x03(Lab - Why)
## Background
* [What is function pointer?](https://chenhh.gitbooks.io/parallel_processing/content/cython/function_pointer.html)
* [Lecture Vid.](https://www.youtube.com/live/IJlYPH1ljIY?feature=share&t=9587)
![](https://hackmd.io/_uploads/BJlVKMiO2.png)

## Source Code
:::spoiler IDA main function
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+Ch] [rbp-4h]

  printf("Give me flag: ");
  __isoc99_scanf("%25s", buf);
  for ( i = 0; i <= 24; ++i )
  {
    if ( buf[i] - 10 != enc_flag[i] )
      return 0;
  }
  pass = 1;
  return 0;
}
```
:::

:::spoiler `.init_array` & `.fini_array` Byte Code
```
.init_array:0000000000003DB0   __frame_dummy_init_array_entry dq offset frame_dummy
.init_array:0000000000003DB0                                           ; DATA XREF: LOAD:0000000000000168↑o
.init_array:0000000000003DB0                                           ; LOAD:00000000000002F0↑o
.init_array:0000000000003DB0                                           ; __libc_csu_init+2↑o
.init_array:0000000000003DB0                                           ; __libc_csu_init+41↑r
.init_array:0000000000003DB0                                           ; Alternative name is '__init_array_start'
.init_array:0000000000003DB8   dq offset _sub_1169
.init_array:0000000000003DC0   dq offset _sub_119d
.init_array:0000000000003DC8   dq offset _sub_10d8
.init_array:0000000000003DC8   _init_array ends
.init_array:0000000000003DC8
.fini_array:0000000000003DD0   ; ELF Termination Function Table
.fini_array:0000000000003DD0   ; ===========================================================================
.fini_array:0000000000003DD0
.fini_array:0000000000003DD0   ; Segment type: Pure data
.fini_array:0000000000003DD0   ; Segment permissions: Read/Write
.fini_array:0000000000003DD0   _fini_array segment qword public 'DATA' use64
.fini_array:0000000000003DD0   assume cs:_fini_array
.fini_array:0000000000003DD0   ;org 3DD0h
.fini_array:0000000000003DD0   __do_global_dtors_aux_fini_array_entry dq offset __do_global_dtors_aux
.fini_array:0000000000003DD0                                           ; DATA XREF: __libc_csu_init+19↑o
.fini_array:0000000000003DD0                                           ; Alternative name is '__init_array_end'
.fini_array:0000000000003DD8   dq offset _sub_11f8
.fini_array:0000000000003DD8   _fini_array ends
```
:::

:::spoiler IDA Disassembly `sub_11f8`
```
int sub_11f8()
{
  if ( pass )
    return puts("Correct :)");
  else
    return puts("Wrong :(");
}
```
:::
## Recon
這一題如果以解題的觀點來說的話，其實很簡單，但他想要傳達的概念很重要，也就是.init和.fini的事情
1. 先執行看看，發現有兩種字串可以先注意，一個是`Give me flag: `和`Wrong :(`
    ```bash
    $ ./why_be9d4253a27b1d44
    Give me flag: 123456
    Wrong :(
    ```

2. 再用IDA看一下整體的架構(如上)
可以發現整體的流程很簡單，他就是叫user輸入25個char，然後每次取一個位元減10再和env_flag的相對字元比較，如果都是對的，`pass = 1;`，但看起來這一段程式並沒有剛剛提到的`Wrong :(`，所以我們用Strings Windows和Xrefs跟一下誰用了這個data，並擷取出code如上(第二和第三的source code)

3. 繼續往上追一下
會發現sub_11f8這個function是定義在.fini_array的區段，代表是在main function結束的時候才會執行的

## Exploit
```python
>>> flag = [0x50, 0x56, 0x4B, 0x51, 0x85, 0x73, 0x78, 0x73, 0x7E, 0x69, 0x70, 0x73, 0x78, 0x73, 0x69, 0x77, 0x7A, 0x7C, 0x79, 0x7E, 0x6F, 0x6D, 0x7E, 0x2B, 0x87]
>>> for i in range(len(flag)):
...     flag[i] -= 10
...
>>> FLAG = []
>>> for i in range(len(flag)):
...     FLAG.append(bytes.fromhex('{:x}'.format(flag[i])).decode('cp437'))
...
>>> "".join(FLAG)
'FLAG{init_fini_mprotect!}'
>>> exit()
$ ./why_be9d4253a27b1d44
Give me flag: FLAG{init_fini_mprotect!}
Correct :)
```