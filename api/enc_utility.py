from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
from .conf import ENC_KEY

def encrypt_data(plaintext):
    key_bytes = bytes(ENC_KEY, "utf-8")
    aes_cipher = Cipher(algorithms.AES(key_bytes),
                        modes.CBC(bytearray(16)),
                        backend=default_backend())
    aes_encryptor = aes_cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    plaintext_bytes = bytes(plaintext, "utf-8")
    padded_bytes = padder.update(plaintext_bytes) + padder.finalize()
    ciphertext_bytes = aes_encryptor.update(padded_bytes) + aes_encryptor.finalize()
    return ciphertext_bytes.hex()

def decrypt_data(ciphertext):
    key_bytes = bytes(ENC_KEY, "utf-8") 
    aes_cipher = Cipher(algorithms.AES(key_bytes),
                        modes.CBC(bytearray(16)),
                        backend=default_backend())
    aes_decryptor = aes_cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    ciphertext_bytes = bytes.fromhex(ciphertext)
    padded_bytes = aes_decryptor.update(ciphertext_bytes) + aes_decryptor.finalize()
    plaintext_bytes = unpadder.update(padded_bytes) + unpadder.finalize()
    return str(plaintext_bytes, "utf-8")

def encrypt_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password
