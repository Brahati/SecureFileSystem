from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class AESHandler:

    @staticmethod
    def encrypt(data: bytes):
        key = get_random_bytes(32)  # 256-bit

        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return key, cipher.nonce, tag, ciphertext

    @staticmethod
    def decrypt(key, nonce, tag, ciphertext):
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        return data