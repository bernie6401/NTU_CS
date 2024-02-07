# Simple Reverse 0x06(Lab - AMessageBox)
## Background
[組合語言ROL和RCL的區別](https://www.796t.com/content/1550025925.html)

## Recon
這一題其實以逆向的角度來說很簡單
1. 先用DIE看一些資訊
![](https://hackmd.io/_uploads/BkFoZ06u3.png)
發現有加UPX的殼，這件事情可以透過IDA更加確定
![](https://hackmd.io/_uploads/ryG0-Aau3.png)
可以看到Function Name只有start然後反組譯的地方看起來很噁心，那應該就是在拆殼的步驟
2. 先執行看看
![](https://hackmd.io/_uploads/HktlXCaun.png)
需要輸入flag然後用一個message box噴錯
3. 用x64-dbg
透過TA的講解，可以知道這一題不需要解殼，只需要用動態debugger看一下就可以了
    1. 我們知道題目有使用到message box的API，所以我們可以先鎖定該API在哪邊呼叫，再往回trace出他的判斷
    我們可以利用符號的視窗看到這支程式有用到那些API Module(.dll)，而message box的API是在`user32.dll`，用下面的搜尋可以縮小範圍，但這個多種類的messagebox，具體來說是用哪一個也不知道，所以可以全選後都設立中斷點
    ![](https://hackmd.io/_uploads/S18CNR6_h.png)
    2. 剩下的就是跟一般debugger差不多的操作，當追到call messagebox之前的break point時，可以看一下call stack(呼叫堆疊)往前trace是誰呼叫了API，發現是`00C7110B`，點進去看一下可以明顯看到Correct/Wrong的字樣，所以可以判斷應該是這一段程式在判斷我們輸入的東西
    ![](https://hackmd.io/_uploads/r1E7LAad3.png)
    ![](https://hackmd.io/_uploads/Syt_8Cadh.png)
    ![](https://hackmd.io/_uploads/BkixvRTOn.png)
    3. 分析判斷的程式
    這裡就是要考驗耐心和不斷的觀察register的變化，認真看大概花個半小時就可以知道這一段在幹嘛(我就菜QAQ)
    ![](https://hackmd.io/_uploads/S10aORTd2.png)
    4. 結論是中間的那些==重要的操作==其實就是左旋轉+XOR `0x87`這樣而已，所以我們就可以開寫腳本了，把東西反著作回去就好了

## Exploit
```python=
import binascii

enc_flag = [0xB5, 0xE5, 0x8D, 0xBD, 0x5C, 0x46, 0x36, 0x4E, 0x4E, 0x1E, 0x0E, 0x26, 0xA4, 0x1E, 0x0E, 0x4E, 0x46, 0x06, 0x16, 0xAC, 0xB4, 0x3E, 0x4E, 0x16, 0x94, 0x3E, 0x94, 0x8C, 0x94, 0x8C, 0x9C, 0x4E, 0xA4, 0x8C, 0x2E, 0x46, 0x8C, 0x6C]

def pad(m):
    length = 0
    if len(m) % 8 != 0:
        length = 8-len(m) % 8
    return '0' * length + m

FLAG = []
for i in range(len(enc_flag)):
    enc_flag[i] ^= 0x87
    tmp = pad(bin(enc_flag[i])[2:])
    tmp = hex(int(tmp[-3:] + tmp[:-3], 2))
    FLAG.append(binascii.unhexlify(tmp[2:]).decode())

print("".join(FLAG))
```

Flag: `FLAG{8699314d319802ef792b7babac9da58a}`