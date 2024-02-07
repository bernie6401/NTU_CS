# Simple Crypto - 0x01(Modular Operation)
###### tags: `CTF` `Crypto` `eductf`

## Background
[『Day 23密碼卷宗現代篇非對稱章 - RSA](https://ithelp.ithome.com.tw/articles/10225768)
[模运算与逆元](https://blog.csdn.net/lion19930924/article/details/61926019)
模運算基本特性:
$$
(a + b) \% p = (a \% p + b \% p) \% p \\
(a - b) \% p = (a \% p - b \% p) \% p \\ 
(a * b) \% p = (a \% p * b \% p) \% p \\
(a ^ b) \% p = ((a \% p) ^ b ) \% p
$$
模運算的结合律：
$$
((a + b) \% p + c) \% p= (a + (b + c) \% p) \% p \\
((a * b) \% p * c) \% p = (a * (b * c) \% p ) \% p
$$
交換律：
$$
(a + b) \% p = (b+a) \% p \\
(a * b) \% p = (b * a) \% p
$$
分配率：
$$
((a +b) \% p * c) \% p = ((a * c) \% p + (b * c) \% p) \% p
$$

[同餘要進行除法時該怎麼處理](https://youtu.be/gKUUI5gQs_k)


基本數學
[What does a|b mean in mathematics?](https://www.quora.com/What-does-a-b-mean-in-mathematics)
## Source Code

### Analysis

## Exploit

## Reference