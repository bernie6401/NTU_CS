# Simple Reverse 0x08(Lab - GetProcAddress)
## Background
[GetModuleFileNameA 函式](https://learn.microsoft.com/zh-tw/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamea?ns-enrollment-type=Collection&ns-enrollment-id=rdg3b1j45ye486)
[createFileA 函式](https://learn.microsoft.com/zh-tw/windows/win32/api/fileapi/nf-fileapi-createfilea)
[setFilePointer 函式](https://learn.microsoft.com/zh-tw/windows/win32/api/fileapi/nf-fileapi-setfilepointer?ns-enrollment-type=Collection&ns-enrollment-id=rdg3b1j45ye486)
[ReadFile 函式](https://learn.microsoft.com/zh-tw/windows/win32/api/fileapi/nf-fileapi-readfile)

## Source Code
:::spoiler IDA main function
```cpp!
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char *v3; // rdi
  __int64 i; // rcx
  char v6[32]; // [rsp+0h] [rbp-40h] BYREF
  char v7; // [rsp+40h] [rbp+0h] BYREF
  char lpFilename[304]; // [rsp+50h] [rbp+10h] BYREF
  char lpBuffer[136]; // [rsp+180h] [rbp+140h] BYREF
  char flag[64]; // [rsp+208h] [rbp+1C8h] BYREF
  __int64 File_HANDLE_VALUE; // [rsp+248h] [rbp+208h]
  int j; // [rsp+264h] [rbp+224h]

  v3 = &v7;
  for ( i = 146i64; i; --i )
  {
    *v3 = 0xCCCCCCCC;
    v3 += 4;
  }
  sub_140011375(&unk_1400230B5);
  sub_1400113AC();
  printf("Give me flag: ");
  scanf("%39s", flag);
  (GetModuleFileNameA_0)(0i64, lpFilename, 260i64);
  File_HANDLE_VALUE = (CreateFileA)(
                        lpFilename,
                        0x80000000i64,
                        FILE_SHARE_READ,
                        0i64,
                        OPEN_EXISTING,
                        FILE_ATTRIBUTE_NORMAL,
                        0i64);
  if ( File_HANDLE_VALUE == -1
    || ((SetFilePointer)(File_HANDLE_VALUE, 0x4Ei64, 0i64, FILE_BEGIN),
        !(ReadFile)(File_HANDLE_VALUE, lpBuffer, 39i64, 0i64, 0i64)) )
  {
LABEL_11:
    puts("Wrong...");
  }
  else
  {
    for ( j = 0; j < 39; ++j )
    {
      if ( (flag[j] ^ lpBuffer[j]) != byte_14001E000[8 * j] )
        goto LABEL_11;
    }
    puts("Correct!!!");
  }
  sub_140011311(v6, &unk_14001BB18);
  return 0;
}
```
:::
## Recon
這一題一樣，如果是以解題為目的話，其實很簡單，但還是想要提到重要的主題也就是PEB，但我覺得與其用IDA一個一個分析，不如直接用x64dbg幫你跑好就可以直接知道哪個API在哪個address，會比較方便，雖然不排除會有一些方式可以繞過或是混淆，但...有遇到在說吧，反正之後在還債吧!

1. 先執行看看，看有沒有甚麼string可以在IDA中trace
2. 找到main function後轉而用x64dbg，並且找到main function entry address，然後設定breakpoint，並且trace code
3. 如果遇到x64dbg中顯示一些import dll function，可以對照IDA並且rename，這樣大概就可以用IDA的反組譯的方式查看整體的流程
4. 看到main function最下面的else$\to$if statement，在看回去x64dbg就可以知道byte_14001e000的那些char是哪些
5. 開寫script
## Exploit
```python=
str1 = [0x12, 0x24, 0x28, 0x34, 0x5B, 0x3A, 0x07, 0x1C, 0x13, 0x2D, 0x00, 0x32, 0x43, 0x16, 0x12, 0x1A, 0x01, 0x02, 0x1D, 0x5A, 0x07, 0x01, 0x7F, 0x35, 0x10, 0x1A, 0x70, 0x1B, 0x01, 0x43, 0x05, 0x2B, 0x37, 0x52, 0x08, 0x1C, 0x17, 0x44, 0x53]
str2 = [0x54, 0x68, 0x69, 0x73, 0x20, 0x70, 0x72, 0x6F, 0x67, 0x72, 0x61, 0x6D, 0x20, 0x63, 0x61, 0x6E, 0x6E, 0x6F, 0x74, 0x20, 0x62, 0x65, 0x20, 0x72, 0x75, 0x6E, 0x20, 0x69, 0x6E, 0x20, 0x44, 0x4F, 0x53, 0x20, 0x6D, 0x6F, 0x64, 0x65, 0x2E]


FLAG = []

for i in range(39):
    tmp = str1[i] ^ str2[i]
    FLAG.append(bytes.fromhex('{:x}'.format(tmp)).decode('utf-8'))

print("".join(FLAG))
```

Flag: `FLAG{Just_a_customized_GetProcAddress!}`