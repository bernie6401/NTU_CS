# Simple Welcome 0x02 & 0x05(Lab - Nine & Nine-Revenge)
## Background
[Convert.FromBase64String(String) Method in C#](https://www.tutorialspoint.com/convert-frombase64string-string-method-in-chash#)
[String.Substring 方法](https://learn.microsoft.com/zh-tw/dotnet/api/system.string.substring?view=net-7.0)

## Source Code
:::spoiler C# From dnSpy
```csharp
// Nine.Stage
// Token: 0x0600000D RID: 13 RVA: 0x00002694 File Offset: 0x00000894
private void Flag()
{
	this.font = new Font(this.fontFamily, 35f, FontStyle.Regular);
	byte[] array = Convert.FromBase64String("LwcvGwpuiPzT7+LY9PPo6eLpuiY7vTY6ejz2OH1pui5uDu6+LY5unpui+6uj14qmpuipqfo=".Replace("pui", "").Substring(1));
	for (int i = 0; i < array.Length; i++)
	{
		array[i] ^= 135;
	}
	this.SetMessageBox(Encoding.UTF8.GetString(array));
}
```
:::

## Recon
1. 起手式一定用DIE或其他檢測tool看一下是用哪種東西編譯或有沒有加殼
![](https://hackmd.io/_uploads/SksyjD8K3.png)
我一開始以為可以用IDA之類的東西反編譯他，但是顯然IDA沒辦法解析.NET file，這一題也是看了別人的WP[^wp_1]才知道有[dnSpy](https://github.com/dnSpy/dnSpy/releases)這東西可以用
![](https://hackmd.io/_uploads/rkiIiwUK3.png)
2. 執行程式
實際執行起來會發現它就是個小遊戲，可以用方向鍵操控人移動或是移開石頭，重點是要拿到鑰匙並開鎖拿到旗子，玩了好久都沒成功，所以想說可以用dnSpy看一下可以用的東西
![](https://hackmd.io/_uploads/rkR8cPIt2.png)
3. 用dnSpy看source code
在`/Nine/Nine.exe/Nine/Stage@02000004/Flag()`以及`/Nine-revenge/Nine-revenge.exe/Nine/Stage@02000004/Flag()`都可以直接看到flag function怎麼寫的，所以其實這一題只要知道dnSpy這東西，其實就過於簡單
    :::spoiler Function Path Screenshot
    ![](https://hackmd.io/_uploads/HkHxLuUYh.png)
    ![](https://hackmd.io/_uploads/SyW-8OUK3.png)
    :::
## Exploit
也是可以直接用C#的線上editor，不過如果不會寫的話就可以直接看source code然後用熟悉的語言寫script
* Nine Exp
    ```python
    import base64

    enc_flag = "LwcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6"
    enc_flag = enc_flag[1:]

    enc_flag = base64.b64decode(enc_flag)
    flag = ""
    for i in enc_flag:
        flag += hex(i ^ 135)[2:]

    print(bytes.fromhex(flag).decode('utf-8'))
    ```
* Nine-Revenge Exp
    ```python=
    import base64

    enc_flag = "LwcvGwpuiPzT7+LY9PPo6eLpuiY7vTY6ejz2OH1pui5uDu6+LY5unpui+6uj14qmpuipqfo="
    enc_flag = enc_flag.replace("pui", "")[1:]

    enc_flag = base64.b64decode(enc_flag)
    flag = ""
    for i in enc_flag:
        flag += hex(i ^ 135)[2:]

    print(bytes.fromhex(flag).decode('utf-8'))
    ```
## Reference
[^wp_1]:[Write Up from eric070021](https://hackmd.io/@eric070021/r1UnR5KWi)