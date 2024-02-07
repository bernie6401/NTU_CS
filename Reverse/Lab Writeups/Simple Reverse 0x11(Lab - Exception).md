# Simple Reverse 0x11(Lab - Exception)
## Background
[乘法、除法的運用 — 組合語言筆記](https://mycollegenotebook.medium.com/%E4%B9%98%E6%B3%95-%E9%99%A4%E6%B3%95%E7%9A%84%E9%81%8B%E7%94%A8-%E7%B5%84%E5%90%88%E8%AA%9E%E8%A8%80%E7%AD%86%E8%A8%98-638b1eac4696)
[try-except 陳述式](https://learn.microsoft.com/zh-tw/cpp/cpp/try-except-statement?view=msvc-170&viewFallbackFrom=msvc-170%3Fns-enrollment-type%3DCollection&ns-enrollment-id=rdg3b1j45ye486)
>* EXCEPTION_CONTINUE_EXECUTION (-1) 例外狀況已關閉。 在例外狀況發生的位置繼續執行。
>* EXCEPTION_CONTINUE_SEARCH 無法辨識 (0) 例外狀況。 繼續搜尋處理常式的堆疊，先搜尋包含 try-except 語句，然後針對具有下一個最高優先順序的處理常式。
>* EXCEPTION_EXECUTE_HANDLER 辨識 (1) 例外狀況。 藉由執行 __except 複合陳述式將控制權傳送至例外狀況處理常式，然後在 區塊之後 __except 繼續執行。


## Source Code
:::spoiler IDA Psuedo Code
```cpp
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char Str[112]; // [rsp+20h] [rbp+0h] BYREF
  int i; // [rsp+A0h] [rbp+80h]

  printf("Give me flag: ");
  scanf("%s", Str);
  if ( strlen(Str) == 38 )
  {
    for ( i = 0; i < 38; ++i )
    {
      if ( Str[i] != byte_14000A000[i] )
        goto LABEL_7;
    }
    puts("Correct :>");
  }
  else
  {
LABEL_7:
    puts("Wrong :<");
  }
  return 0;
}
```
:::
## Recon
這一題真的頗複雜(應該也還好...)，但有一些陷阱和套路，這一題是有關於exception的結構分析

詳細解析Exception的結構，請看[課程影片](https://www.youtube.com/live/4-hgyiCV3ZA?feature=share&t=1507)


1. 透過上課教的方式找到Exception Handler Address
    有兩種方式
    * 看PE-Bear
        * 首先我們先看IDA反組譯的psuedo code發現和原始的組語有一些出入(反黃的地方)，代表有一些地方沒有翻出來，此時我們就可以先分析一下是不是有甚麼問題，發現在`15DE`的地方有個除法，且除數是零，代表一定會發生exception
        ![](https://hackmd.io/_uploads/BkCEpelKn.png)
        * 此時就可以用PE-Bear看一下相關的資訊，首先`15DE`是包含在`1590-1748`的Scope，所以要找的unwind address就是`9750`
        ![](https://hackmd.io/_uploads/H1UfyWxtn.png)
        * 實際來到`9750`就會像下圖一樣，但基本上還是需要自己create structure並且手動輸入offset
        ![](https://hackmd.io/_uploads/ryWskWlY2.png)

    * 從xref main function去找
        * 首先在IDA中找到main function，用XRef的方式找到其他呼叫main function的地方，再跟進去，基本上後面的address跟進去就會是跟上面的地方一樣，這個方法有可能會失敗
        ![](https://hackmd.io/_uploads/BkGYeblYh.png)

2. 分析整體的exception handler
看了一下code發現有兩個地方會跳exception，一個是前面提到的==15DE==，另外一個是`1660`，看了一下三個handler的exception return value[^exception_return_value]，發現分別是`0, 1, -1`，所以可以先稍微用肉眼跟一下會發生甚麼事
當exception 1發生時，會先看第一條scope發現雖然在範圍內可是return value是零，代表無法辨識要繼續搜尋，可以看到符合第二條scope的範圍且return value是1，此時就會直接跳到==161D==。而當第二個exception發生時，是在==1660==，只有符合第三條指令，但return value是-1，代表他會回復原始的狀態並跳到下一個RIP
    ```
    SCOPE_RECORD <rva loc_1400015D5, rva loc_1400015E2, rva sub_140006170, rva loc_1400015E2>
    SCOPE_RECORD <rva loc_1400015D5, rva loc_14000161D, rva sub_140006183, rva loc_14000161D>
    SCOPE_RECORD <rva loc_140001657, rva loc_140001664, rva sub_140006199, rva loc_140001664>
    ```
3. 用x64dbg看一下整體的流程
    * 首先第一個exception正如我們所說，跳到==161D==，並做一些操作，這邊就要很仔細分析，明顯看到他會跳過一段不重要的code，然後在`1626-1654`的地方形成一個for-loop，主要的操作是把我們輸入的flag和一個東西做XOR，這個東西實際上去看就是`0xBE, 0xBF, 0xC0, 0xC1,...,0xE3`(共38個連續數值)。
    ![](https://hackmd.io/_uploads/Sy_UvWgK3.png)
    * For-loop結束後就會遇到第二個exception，但實際跟上去後會發現它不是跳到我們預期的RIP而是跳到`169F`(不是很清楚為甚麼會這樣)，所以如果盲目的分析中間的第二個loop其實就是浪費時間，因為根本不會執行到，而這一段for-loop在做的事情就是把剛剛第一個exception處理完的結果和一些data相加然後取低位byte，而那些data實際跟上去會是`0xEF, 0xF0, 0xF1,...,0xFF, 0x00, 0x01,...,0x14`，這裡非常重要，因為0xFF再上去不是0x100而是一樣取低位byte，變成從零開始
    ![](https://hackmd.io/_uploads/B1DRuWxK3.png)
    * ==2023/07/03更新：==
    經過助教的說明，已經知道為甚麼他會跳到`169F`，可以看一下上課講義中提到的`_C_specific_handler`，就在`975C`，用IDA跟進去看一下發現他在呼叫`_C_specific_handler`之前有做了一些操作，他把context的RIP改掉了，有一點hook的感覺，原本exception 2發生時要回去的地方應該是`1660`但加上`0x3F`之後就變成`169F`，和我們實際跑的結果相符合
        :::spoiler 上課講義
        ![](https://hackmd.io/_uploads/HyiTqrxYh.png)
        :::
        :::spoiler 額外操作
        ![](https://hackmd.io/_uploads/ryIUoSlYn.png)
        :::
    * 上述兩個exception做完之後就會直接和encrypted flag進行比對，所以我們要做的事情就是倒過來執行這些東西(encrypted flag - `0xEF,...,0x14` + `0x100`) ^ `(0xBE, 0xBF, 0xC0, 0xC1,...,0xE3`) = FLAG

## Exploit
```python=
first_for_loop = [190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227]

second_for_loop = [239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

enc_flag = [0xE7, 0xE3, 0x72, 0x78, 0xAC, 0x90, 0x90, 0x7C, 0x90, 0xAC, 0xB1, 0xA6, 0xA4, 0x9E, 0xA7, 0xA2, 0xAC, 0x90, 0xB9, 0xB2, 0xBF, 0xBB, 0xBD, 0xB6, 0xAB, 0x90, 0xBA, 0xB4, 0x90, 0xBF, 0xC0, 0xC0, 0xC4, 0xCA, 0x95, 0xED, 0xC0, 0xB2]


FLAG = []

for i in range(38):
    # print(hex(flag[i] ^ enc_flag[i])[2:], end="")

    if enc_flag[i] - second_for_loop[i] < 0:
        tmp = hex(first_for_loop[i] ^ (enc_flag[i] - second_for_loop[i] + 0x100))[2:]
    else:
        tmp = hex(first_for_loop[i] ^ (enc_flag[i] - second_for_loop[i]))[2:]


    FLAG.append(bytes.fromhex(tmp).decode('cp437'))

print("".join(FLAG))
```

Flag: `FLAG{__C_specific_handler_is_hooked:O}`
## Reference
[^exception_return_value]:[try-except 陳述式](https://learn.microsoft.com/zh-tw/cpp/cpp/try-except-statement?view=msvc-170&viewFallbackFrom=msvc-170%3Fns-enrollment-type%3DCollection&ns-enrollment-id=rdg3b1j45ye486)