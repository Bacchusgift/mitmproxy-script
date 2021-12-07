import base64
from binascii import a2b_hex
import hashlib
from Crypto.Cipher import AES


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(timestamp, text):
    secret = a2b_hex(hashlib.sha256(timestamp.encode('utf-8')).hexdigest())
    mode = AES.MODE_CBC
    iv = a2b_hex('00000000000000000000000000000000')
    cipher = AES.new(secret, mode, iv)
    # 16分组数据长度，填充补齐最后一块数据，
    text = base64.b64decode(text)
    decrypt_data = cipher.decrypt(text)
    # 最后一位是\xo6,则删除末尾6个字节
    upad = lambda s: s[0:-(s[-1])]
    decrypt_data = upad(decrypt_data)
    decrypt_data = decrypt_data.decode('utf-8')
    return decrypt_data


def encrypt(timestamp, text):
    secret = a2b_hex(hashlib.sha256(timestamp.encode('utf-8')).hexdigest())
    mode = AES.MODE_CBC
    iv = a2b_hex('00000000000000000000000000000000')
    cipher = AES.new(secret, mode, iv)
    print("text : %s" % text)
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    text = pad(text)
    encrypt_data = cipher.encrypt(text.encode('utf-8'))
    return base64.b64encode(encrypt_data)
