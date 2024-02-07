# Simple Reverse 0x13(Lab - Meow)
## Background
[課程影片 - Process Injection](https://www.youtube.com/live/4-hgyiCV3ZA?feature=share&t=7028)
一開始看真的看不太懂，只知道大概的邏輯，簡單來說應該是在原有的process中插入其他的process使其被執行，有以下幾種
* DLL Injection
* APC Injection
* Early Bird APC Injection
* Process Hollowing
* Reflective DLL Injection


## Recon
其實這一題如果沒有TA先破哏，基本上我是直接放棄的，解題之前可以先看[破哏教學](https://www.youtube.com/live/4-hgyiCV3ZA?feature=share&t=10348)
簡單來說這整支程式就是先把預先藏好的code解密出來，然後利用Process Hollowing的方式inject到原本的程式，而這支外插進來的code就會對我們輸入的flag進行一些操作，然後再跟他原本的encrypted flag進行比較。當我們知道這些事情之後，就可以開始分析了

1. 先在IDA中找到隱藏的code解密的function
我是直接看TA教學的部分，不然我應該也找不出來，除非用x64dbg慢慢跟，具體來說是在main function中if statement的第二個function
![](https://hackmd.io/_uploads/S1DtpV-K3.png)
跟進去後的sub_401550()
![](https://hackmd.io/_uploads/Sy3R6Vbth.png)
    :::spoiler Decrypt Hidden Code
    ```cpp
    __int64 sub_401550()
    {
      __int64 result; // rax
      unsigned int i; // [rsp+Ch] [rbp-4h]

      for ( i = 0; ; ++i )
      {
        result = i;
        if ( i > 0x3FFF )
          break;
        *(dword_404040 + i) += i % 7;
        *(dword_404040 + i) ^= byte_404020[i & 7];
      }
      return result;
    }
    ```
    :::
2. 利用Scylla把memory(也就是隱藏的執行檔)dump出來
我們知道他在做甚麼之後，就可以用x64dbg的plugin(Scylla)把整支程式dump下來，要做到這件事情就需要知道他的位置在哪邊以及要dump多少的memory。透過上面的code我們可以在他return之前的address記錄下來然後在x64dbg下斷點(0x4015FE)，然後觀察她前面的code把decrypt的code放在哪邊
    ![](https://hackmd.io/_uploads/H1dGJBZth.png)
    透過上圖，應該不難看出他是東西放在0x404040，跟進去發現是MZ開頭的magic header就是我們要找的起始位置，而具體來說要dump多大的記憶體呢?可以從IDA分析的source code發現他在counter大於0x3fff的時候就會跳出迴圈，那也就是說大小應該是0x4000才對
    ![](https://hackmd.io/_uploads/BJEIyS-Kh.png)
    ![](https://hackmd.io/_uploads/ByoTyrWt3.png)

3. 有了隱藏的code之後就來分析一下他對我們輸入的flag做了甚麼操作
用IDA看了一下，簡單來說這支隱藏程式就像是meow.exe的server side，下圖是兩者的對照，做邊是隱藏的code，右邊是meow.exe(被inject的victim)，可以看到右邊的meow.exe在我們輸入了flag後就把flag寫在某個記憶體中(==WriteFile==)，而左邊的程式就會去該地址撈flag(==ReadFile==)，然後在下面有一個sub_401550(flag)的function然後flag被傳入，看起來就是要對flag做一些操作(source code如下)，操作完後就會再把enc_flag寫到某個memory中，而右面的meow.exe就會再到記憶體中撈資料進行後續的比對
    ![](https://hackmd.io/_uploads/HJ4ClHbth.png)
    :::spoiler Encrypted Flag Source Code
    ```cpp
    __int64 __fastcall sub_401550(char *flag)
    {
      int v1; // r8d
      __int64 result; // rax
      int i; // [rsp+Ch] [rbp-4h]

      for ( i = 0; i <= 38; ++i )
      {
        flag[i] ^= key[i % 0xBui64];
        v1 = flag[i];
        result = (v1 + 2 * (i % 3));
        flag[i] = v1 + 2 * (i % 3);
      }
      return result;
    }
    ```
    :::
4. 整體的流程大概就是這樣，所以如果專注在解題的話其實只需要注意輸入的flag如何被加密就好，再開寫script
## Exploit
```python
enc_flag = [0x24, 0x1D, 0x1B, 0x31, 0x21, 0x0B, 0x4F, 0x0F, 0xE8, 0x50, 0x37, 0x5B, 0x08, 0x40, 0x4A, 0x08, 0x1D, 0x11, 0x4A, 0xB8, 0x11, 0x67, 0x3F, 0x67, 0x38, 0x14, 0x3F, 0x19, 0x0B, 0x54, 0xB4, 0x09, 0x63, 0x12, 0x68, 0x2A, 0x45, 0x53, 0x0E]
key = [0x62, 0x57, 0x56, 0x76, 0x64, 0x77, 0x3D, 0x3D, 0x87, 0x63, 0x0]

FLAG = []
for i in range(39):
    enc_flag[i] -= (2 * (i % 3))
    enc_flag[i] ^= key[i % 11]
    FLAG.append(bytes.fromhex(hex(enc_flag[i])[2:]).decode('cp437'))
print("".join(FLAG))
```

Flag: `FLAG{pr0c355_h0ll0w1ng_4nd_n4m3d_p1p35}`