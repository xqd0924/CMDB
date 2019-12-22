from Crypto.Cipher import AES
from lib.conf.config import setting


def encrypt(message):
    key = setting.KEY_STR
    cipher = AES.new(key, AES.MODE_CBC, key)
    ba_data = bytearray(message,encoding='utf-8')
    v1 = len(ba_data)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):
        ba_data.append(v3)
    final_data = ba_data
    msg = cipher.encrypt(final_data) # 要加密的字符串，必须是16个字节或16个字节的倍数
    return msg