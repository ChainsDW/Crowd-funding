from Crypto.Cipher import AES
import Crypto.Random
import base64
from binascii import b2a_hex, a2b_hex,b2a_base64,a2b_base64
#使用的库需要通过pip3 install pycryptodome安装（python3.6版本），安装前需卸载原有的库，否则会报错。


class prpcrypt:
    """
    三种加密解密方法
    """
    def __init__(self):
        self.key =[]
        self.content = []
        self.x = []


    def auto_fill(self,x):
        print(len(x))
        if len(x) <= 32:
            while len(x) not in [16, 24, 32]:
                x += " "
            return x.encode()
        else:
            raise print('请控制你的密钥小于32位')

    def encoding_AES_ECB(self,key,text):
        x = Crypto.Cipher.AES.new(self.auto_fill(key), Crypto.Cipher.AES.MODE_ECB)
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        b = x.encrypt(text)#ESB加密数据
        a = base64.encodebytes(b)#ESB加密数据
        print(a)
        return a

    def decoding_AES_ECB(self,key,content):
        x = Crypto.Cipher.AES.new(self.auto_fill(key), Crypto.Cipher.AES.MODE_ECB)
        b = x.decrypt(base64.decodebytes(content))#ESB解密数据
        return b


    def encoding_base64(self,key,content):
        x = Crypto.Cipher.AES.new(self.auto_fill(key), Crypto.Cipher.AES.MODE_ECB)
        a = b2a_base64(x.encrypt(self.auto_fill(content)))
        return a


    def decoding_base64(self,key,content):
        x = Crypto.Cipher.AES.new(self.auto_fill(key), Crypto.Cipher.AES.MODE_ECB)
        b = x.decrypt(a2b_base64(content))
        return b


    def encoding_AES_CBC(self,key,content):
        #返回的IV值为随机产生，c为加密后的数据
        iv = Crypto.Random.new().read(16)
        y = Crypto.Cipher.AES.new(self.auto_fill(key), Crypto.Cipher.AES.MODE_CBC, iv)
        c = b2a_base64(y.encrypt(self.auto_fill(content)))#加密后的内容
        return c,iv

    def decoding_AES_CBC(self,key,content,iv):
        z = Crypto.Cipher.AES.new(self.auto_fill(key), Crypto.Cipher.AES.MODE_CBC, iv)
        d = z.decrypt(a2b_base64(content))
        return d


from binascii import b2a_hex, a2b_hex


class PrpCrypt(object):

    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    def encrypt(self, text):
        if isinstance(text, str):
            text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        # 这里密钥key 长度必须为16（AES-128）,
        # 24（AES-192）,或者32 （AES-256）Bytes 长度
        # 目前AES-128 足够目前使用
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            # \0 backspace
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            # text = text + ('\0' * add)
            text = text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        plain_list = '{}'.format(plain_text).split('\'')
        plain_list[1].rstrip('\x00')
        plain_text = '\''.join(plain_list)
        return eval(plain_text)



if __name__ == '__main__':
    code = PrpCrypt('keyskeyskeyskey2')
    a='ashiuhiu在hoi j0ijojpkd'
    e = code.encrypt(a)
    d = code.decrypt(e)
    plain_list = '{}'.format(d).split('\'')
    plain_list[1].rstrip('\x00')
    plain_text = '\''.join(plain_list)
    print(type(plain_text),type(eval(plain_text)))
    print(a,e,d)
    #b'ashiuhiu\xe5\x9c\xa8hoijoijojpkd\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    # dd = '{}'.format(d)
    # print(dd)
    # aa = dd.split('\'')
    # print(type(eval(dd)))
    a = b'\x00'
    print(str(a, 'utf8'),'-')