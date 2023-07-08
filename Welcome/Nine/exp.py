import base64

enc_flag = "LwcvGwPze6PKg9eLY6/Lk7P7Y8+/m89jO2O/m8eLY5tjz7+7p4Njh6PXY9+bp5Obs4vT6"
enc_flag = enc_flag[1:]

enc_flag = base64.b64decode(enc_flag)
flag = ""
for i in enc_flag:
    flag += hex(i ^ 135)[2:]

print(bytes.fromhex(flag).decode('utf-8'))