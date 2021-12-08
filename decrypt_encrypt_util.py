# -*- coding:utf-8 -*-
# !usr/bin/python3

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

if __name__ == '__main__':
    # time = "1638869162839"
    # ext_info = "uQpI75bPzA4Ifq8mlt9l+mMNiIC+HYERZpF3G66Q1Yg8eiUa/bhPb/hk+qENdmTaTW8cJpDzB81/2BrAaLEUSzga87oaJLGqlVsaaoNZjeCjaNxepIbJqlNsQBcmOLbEK8SL0KRvVJEBCmxuT2gvL3T5GiRbp6Y+HifeD2fxvHgCT6gE40xKfjEBhEjiq+w8uZ1+2/hPnLFz3/4yVZZl0OVcsNWn0aa9smHbo1C5I/PtISCehpXJ7NnDiNJKprwnJFObRYZ8x8Z7QCkNmteUCwfQNKG1x+bRGUXe153G0Ug+WLskJTk0J2q0UYVSYNx/fdDK9ZupQUykmHkqEr2zl4qH+JmXX2f99QtFEXAnJ/xBYdhl8tktENljEHPy9Jd6WqpiP+H7IIwYJ/PKzlf8WcnRf8pXg9wJT21bR/+mxLptJygQfhdiR6i8WpFKjY59m6bMkq9tIj67a/7G9wZB9T6jWESeHFAkgLJ8pAI3fENITNRzikMTbolwQ8dkhkydxcbwgSN7K7LaeluZRH25NCBvOXe6ZOzS+EqeTCMgxD6P1/wYt1/ovOWpj8n0WvwgMIbb8mqU8ZfvNJRldUUkz6obL+JOln5YChWyfhRGj8Y="
    # text = "oazMZr4R05wAZ48n2DC0dWhgE6+4Bvz5+uQHX30C9O2dsasZluK9N36FmWECexv4UvsWJuV9jpEdgCNWZDlc95eefxbq4CsIDee8AcYZJPE="
    # ext_info_decrypt = decrypt(time, ext_info)
    # print(ext_info_decrypt)
    # t = decrypt(ext_info_decrypt, text)
    # print(t)

    time2 = "1638870519005"
    access_token = "9A80ZmvCY+vF4wq8ZTY9PfqxhR7aA/LBwYX+qYT2hbfHfvdMEErDMyit8wOv2aAo"
    text2 = "ghTOEBemcwC7zQOHDebBpkiVeRlEBQTxUKH0W2DbQY8XtT8FjHj/vZsfBxoj6lvZLVzp/bYck3j7ANmfa2JLPDiGS ZqJVTMjwuphzsvujN228RBPzplHRbVwxZDZ/KBK/cAY7BYCHItl2TBxemM79k9WUWHFvEta2m4gu73J bRWgUv7QdlKq3SLfKxQ/wQWSsOCUY/WN1Y9TMCH3BhsW1dajDSTcEnVM/a/n4ZlBduCwW oQV/kDU4GHzn279NV1rijU1FjkQD1ddD43y3FgsX9fPlI4xNMrTQ8V5GDxg"
    access_token_decrypt = decrypt(time2, access_token)
    print(access_token_decrypt)
    t = decrypt(access_token_decrypt, text2)
    print(t)

