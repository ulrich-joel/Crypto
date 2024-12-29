import os
import sys
import getpass
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Dérive une clé à partir d'un mot de passe et d'un sel donné à l'aide de PBKDF2 avec SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(filename: str, key: bytes):
    """
    Chiffre un fichier avec AES en mode CFB et enregistre le fichier chiffré.
    """
    salt = os.urandom(16)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(filename, 'rb') as original_file:
        original_data = original_file.read()
        encrypted_data = encryptor.update(original_data) + encryptor.finalize()
    
    encrypted_filename = f'{filename}.CRL'
    with open(encrypted_filename, 'wb') as encrypted_file:
        encrypted_file.write(salt + iv + encrypted_data)
    
    print(f"Fichier '{filename}' chiffré en '{encrypted_filename}'.")

def process_directory(directory: str, password: str):
    """
    Parcourt tous les fichiers dans un répertoire et les chiffre un par un.
    """
    salt = os.urandom(16)  # Générer un sel aléatoire pour chaque session
    key = derive_key(password, salt)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            encrypt_file(full_path, key)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python crl.py <encrypt/decrypt> <file/directory_path>")
        sys.exit(1)

    action = sys.argv[1]
    path = sys.argv[2]

    if action == "encrypt":
        password = getpass.getpass(prompt="Entrez votre phrase secrète : ")

        if os.path.isdir(path):
            process_directory(path, password)
        elif os.path.isfile(path):
            # Si c'est un fichier unique
            salt = os.urandom(16)  # Générer un sel aléatoire pour chaque session
            key = derive_key(password, salt)
            encrypt_file(path, key)
        else:
            print("Le chemin spécifié n'est ni un fichier ni un dossier.")
