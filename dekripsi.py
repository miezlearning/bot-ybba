import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def encrypt_message(message, key):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_message).decode('utf-8')

AES_KEY = b'rahasia_nihkak_hehe_maafya_KAKA!'[:32]

def decrypt_message(encrypted_message, key):
    backend = default_backend()
    decoded_encrypted_message = base64.b64decode(encrypted_message)
    iv = decoded_encrypted_message[:16]
    ciphertext = decoded_encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    
    return unpadded_data.decode('utf-8')

while True:
    try:
        encrypted_message = input("Masukkan enkripsi kode: ")
        if not encrypted_message:
            raise ValueError("Pesan terenkripsi tidak boleh kosong.")
        
        print("Pesan terenkripsi:", encrypted_message)
        decrypted = decrypt_message(encrypted_message, AES_KEY)
        print("Pesan terdekripsi:", decrypted)
        break
    except ValueError as e:
        print(f"Error: {e}")
    except (base64.binascii.Error, TypeError) as e:
        print("Pesan terenkripsi tidak valid atau rusak.")
    except padding.PaddingError:
        print("Kunci AES tidak cocok atau pesan terenkripsi rusak.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

