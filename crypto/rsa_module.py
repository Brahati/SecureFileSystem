from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSAHandler:

    @staticmethod
    def generate_keys():
        key = RSA.generate(2048)
        return key, key.publickey()

    @staticmethod
    def encrypt(public_key, data):
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(data)

    @staticmethod
    def decrypt(private_key, encrypted_data):
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(encrypted_data)