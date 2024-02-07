# Simple Reverse 0x12(Lab - TLSCallback)
## Background
[課程相關影片](https://www.youtube.com/live/4-hgyiCV3ZA?feature=share&t=6624)
[[C語言] function pointer的應用[四]: function pointer array](https://medium.com/@racktar7743/c語言-function-pointer的應用-四-function-pointer-array-d0d624db8406)

## Source Code
:::spoiler IDA main function
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rbx
  int v4; // edi
  __int64 v5; // r14
  char *v6; // rsi
  __int64 v7; // rax
  const char *v8; // rcx

  printf("Give me flag: ");
  scanf("%58s");
  v3 = 0i64;
  v4 = 0;
  v5 = 0i64;
  v6 = flag;
  do
  {
    (funcs_140001156[v4 % 3u])(&flag[v5]);
    ++v6;
    v7 = v5 & 3;
    ++v4;
    ++v5;
    *(v6 - 1) += key_140004050[v7];
  }
  while ( v4 < 58 );
  while ( flag[v3] == byte_1400022B8[v3] )
  {
    if ( ++v3 >= 58 )
    {
      v8 = "Correct!";
      goto LABEL_7;
    }
  }
  v8 = "Wrong QAO";
LABEL_7:
  puts(v8);
  return 0;
}
```
:::
## Recon
這一題也蠻簡單的，只要有耐心分析一下就可以了
1. 首先執行一下這隻程式，發現沒啥特別的，就和之前的題目一樣
![](https://hackmd.io/_uploads/ryT1QMbKh.png)
2. 用IDA看一下，可以發現也蠻單純的，就用function pointer array然後傳入我們輸入的flag進行一些事情再加上一個數值(來自某一個array)
3. 仔細看一下有哪些function然後分別做了甚麼事
    ![](https://hackmd.io/_uploads/SkDpNGbYh.png)
    1. xor 0x87
        :::spoiler source
        ```
        void __fastcall do_xor(_BYTE *a1)
        {
          *a1 ^= 0x87u;
        }
        ```
        :::
    2. xor 0xff
        :::spoiler source
        ```
        void __fastcall do_inverse(_BYTE *a1)
        {
          *a1 = ~*a1;
        }
        ```
        :::
    3. xor 0x63
        :::spoiler source
        ```
        void __fastcall do_xor_2(_BYTE *a1)
        {
          *a1 ^= 0x63u;
        }
        ```
        :::
4. <font color="FF0000">陷阱</font>
如果直接分析這樣的code會做白工，因為這一題有tls callback function在搞事，這件事情IDA和x64dbg都有分析出來，或者是也可以用PE-Bear看一下，所以我們就朝這個方向分析一下，看起來兩者都沒有很複雜，tlscallback function 2就只是把剛剛前面的function pointer array的順序置換一下，而tlscallback function 1也只是用置換過後的function pointer array把key的數值做一些操作而已，如果看psuedo code看不太懂得話可以直接用x64dbg用肉眼跟一下(我就這樣XDD)，應該也是可以很直觀的猜出這些事情
:::spoiler TLS Callback function 1 & 2
![](https://hackmd.io/_uploads/SJ4tvzZF2.png)
![](https://hackmd.io/_uploads/BkN5wfWK3.png)
:::
5. 用x64dbg直接動態跟code，以下的screenshot我都有加上一些comment幫助理解
    * TLSCallback相關的code
    ![](https://hackmd.io/_uploads/S1b9FzWth.png)
    * 三個Function pointer
    ![](https://hackmd.io/_uploads/BkW1qGbKn.png)
    * main function
    ![](https://hackmd.io/_uploads/SJwm5zbF3.png)
6. 結論
在function pointer的順序是xor 0x63 $\to$ xor 0x87 $\to$ xor 0xff
在key的部分是0x21 $\to$ 0xce $\to$ 0x39 $\to$ 0x40
    ```asm
    xor 0x63 + 0x21
    xor 0x87 + 0xce
    xor 0xff + 0x39
    xor 0x63 + 0x40
    xor 0x87 + 0x21
    xor 0xff + 0xce
    xor 0x63 + 0x39
    ...
    ```
    :::info
    Note: 相加的部分最後只會取==低位byte==喔，所以如果減回去發現是負的，就要在加0x100導正回來
    :::
7. 開寫script
## Exploit
```python=
key = [0x21, 0xCE, 0x39, 0x40]

enc_flag = [0x46, 0x99, 0xF7, 0x64, 0x1D, 0x79, 0x44, 0x22, 0xC1, 0xD3, 0x27, 0xCD, 0x31, 0xC1, 0xD9, 0x77, 0xEC, 0x7A, 0x75, 0x24, 0xBF, 0xDD, 0x24, 0xDD, 0x23, 0xB2, 0xCD, 0x7C, 0x02, 0x58, 0x46, 0x24, 0xAC, 0xD8, 0x21, 0xD1, 0x5D, 0xBC, 0xC5, 0x7C, 0x05, 0x6C, 0x48, 0x2B, 0xBB, 0xD5, 0x11, 0xCB, 0x35, 0xB6, 0xD9, 0x57, 0x0F, 0x60, 0x3F, 0x34, 0xFF, 0xEC]

def xor(index, val):
    if index % 3 == 0:
        return val ^ 0x63
    elif index % 3 == 1:
        return val ^ 0x87
    else:
        return val ^ 0xff

FLAG = []
for i in range(len(enc_flag)):

    tmp = enc_flag[i] - key[i % 4]
    if tmp < 0:
        tmp += 0x100
    tmp = xor(i, tmp)
    FLAG.append(bytes.fromhex(hex(tmp)[2:]).decode('utf-8'))

print("".join(FLAG))
```

Flag: `FLAG{The_first_TLS_callback_function_is_called_two_times!}`