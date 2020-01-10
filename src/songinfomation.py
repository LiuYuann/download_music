from Crypto.Cipher import AES
import requests
import base64
import os
import codecs
import json
from pypinyin import lazy_pinyin


class SongInformation():
    def __init__(self):
        # 后三个参数和i的值（随机的十六位字符串）
        self.b = '010001'
        self.c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.d = b'0CoJUm6Qyw8W8jud'

    # 随机的十六位字符串
    def __createSecretKey(self, size):
        return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16].encode('utf-8')

    # AES加密算法
    def __AES_encrypt(self, text, key, iv):
        pad = 16 - len(text) % 16
        if type(text) == type(b''):
            text = str(text, encoding='utf-8')
        text = text + str(pad * chr(pad))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = encryptor.encrypt(text.encode('utf-8'))
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    # 得到第一个加密参数
    def __Getparams(self, a, SecretKey):
        # 0102030405060708是偏移量，固定值
        iv = b'0102030405060708'
        h_encText = self.__AES_encrypt(a, self.d, iv)
        h_encText = self.__AES_encrypt(h_encText, SecretKey, iv)
        return h_encText

    # 得到第二个加密参数
    def __GetSecKey(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text, 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    # 得到表单的两个参数
    def __GetFormData(self, a):
        SecretKey = self.__createSecretKey(16)
        params = self.__Getparams(a, SecretKey)
        enSecKey = self.__GetSecKey(SecretKey, self.b, self.c)
        data = {
            "params": str(params, encoding='utf-8'),
            "encSecKey": enSecKey
        }
        return data

    def get_info(self, input, offset=0):
        # 查询id的url
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        # 伪装头部
        head = {
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }
        keyword = ''.join(lazy_pinyin(input))
        key = '{hlpretag:"",hlposttag:"</span>",s:"' + keyword + '",type:"1",csrf_token:"",limit:"30",total:"true",offset:"' + str(
            offset) + '"}'
        FormData = self.__GetFormData(key)
        html = requests.post(url, headers=head, data=FormData)
        result = json.loads(html.text)
        return result['result']
