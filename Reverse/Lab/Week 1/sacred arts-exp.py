fake_flag = ["8D909984B8BEBAB3", "8D9A929E98D18B92", "D0888BD19290D29C", "8C9DC08F978FBDD1", "D9C7C7CCCDCB92C2", "C8CFC7CEC2BE8D91", "FFFFFFFFFFFFCF82"]
BIG_NUM = 1<<64
FLAG = []
for i in fake_flag:
	tmp = i[:12] + i[14:16] + i[12:14]
	print(tmp)
	tmp = BIG_NUM - int(tmp, 16)
	FLAG.append(bytes.fromhex(hex(tmp)[2:]).decode('utf-8')[::-1])

print("".join(FLAG))