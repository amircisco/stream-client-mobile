from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256, HMAC
from hmac import compare_digest


class encrypt_cisco:
    def __init__(self,key):
        self.key=key
        self.BLOCK_SIZE=16
        self.pad=lambda s: s+((self.BLOCK_SIZE-len(s)%self.BLOCK_SIZE)*chr(self.BLOCK_SIZE-len(s)%self.BLOCK_SIZE)).encode()
        self.unpad = lambda s : s[:-ord(s[len(s)-1:])]

    def str2key(self,str):
        return SHA256.new(str.encode()).digest()[:self.BLOCK_SIZE]

    def get_key(self):
        return self.key

    def set_key(self,key):
        self.key=key
    def encrypt(self,data):

        if not len(data):
            print('no data to encrypt!')
            return None
        if not len(self.key):
            print('no encryption key!')
            return None

        key=self.str2key(self.key)

        data=self.pad(data)
        iv=Random.new().read(self.BLOCK_SIZE)
        aes=AES.new(key, AES.MODE_CBC, iv)

        ct=iv+aes.encrypt(data)

        key2=SHA256.new(key).digest()

        return HMAC.new(key2, ct, SHA256).digest()+ct

    def decrypt(self,data):

        if not len(data):
            print('no data to decrypt!')
            return None
        if not len(self.key):
            print('no decryption key!')
            return None

        key=self.str2key(self.key)

        hmac1=data[:32]
        ct=data[32:]

        key2=SHA256.new(key).digest()

        if not compare_digest(HMAC.new(key2, ct, SHA256).digest(), hmac1):
            #print('hmac verification failed!')
            return None

        iv=ct[:self.BLOCK_SIZE]
        aes=AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(aes.decrypt(ct[self.BLOCK_SIZE:]))


