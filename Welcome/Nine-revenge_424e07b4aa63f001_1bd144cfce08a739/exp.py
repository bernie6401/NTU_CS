import base64

enc_flag = "LwcvGwpuiPzT7+LY9PPo6eLpuiY7vTY6ejz2OH1pui5uDu6+LY5unpui+6uj14qmpuipqfo="
enc_flag = enc_flag.replace("pui", "")[1:]

enc_flag = base64.b64decode(enc_flag)
flag = ""
for i in enc_flag:
    flag += hex(i ^ 135)[2:]

print(bytes.fromhex(flag).decode('utf-8'))