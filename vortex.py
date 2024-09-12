import os
import sys
import random
import shutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

def generate_password(length, chars):
    char_set = ''
    if 'letter' in chars:
        char_set += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if 'number' in chars:
        char_set += '0123456789'
    if 'extra' in chars:
        char_set += '_-'
    password = ''.join(random.choice(char_set) for _ in range(length))
    return password

def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    with open(file_path + '.tmp', 'wb') as f:
        f.write(salt + iv + encrypted_data)
    os.remove(file_path)
    shutil.move(file_path + '.tmp', file_path + '.vrtx')

def decrypt_file(file_path, password):
    if not file_path.endswith('.vrtx'):
        print(Fore.RED + 'Error: File is not encrypted.')
        sys.exit(1)
    temp_file_path = file_path[:-5] + '.tmp'
    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_data = f.read()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    try:
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    except ValueError as e:
        print(Fore.RED + 'Error: Incorrect password.')
        sys.exit(1)
    with open(temp_file_path, 'wb') as f:
        f.write(decrypted_data)
    os.remove(file_path)
    shutil.move(temp_file_path, file_path[:-5])

def save_password(password):
    with open('password.vortex', 'w') as f:
        f.write(password)

def main():
    parser = argparse.ArgumentParser(description='vortex v3.0    by JRDP Team')
    parser.add_argument('-f', '--file', help='File to encrypt/decrypt', required=True)
    parser.add_argument('-l', '--password-length', type=int, help='Length of password')
    parser.add_argument('-t', '--chars', help='Characters to use for password generation (letter, number, extra)', nargs='+')
    parser.add_argument('-c', '--custom-password', help='Use custom password')
    parser.add_argument('-e', '--encrypt', help='Encrypt file', action='store_true')
    parser.add_argument('-d', '--decrypt', help='Decrypt file', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(Fore.RED + 'Error: File {} does not exist.'.format(args.file))
        sys.exit(1)

    if not (args.encrypt or args.decrypt):
        print(Fore.RED + 'Error: You must specify either -e or -d.')
        sys.exit(1)

    if args.custom_password:
        if args.password_length or args.chars:
            print(Fore.RED + 'Error: -c cannot be used with -l or -t.')
            sys.exit(1)
        password = args.custom_password
        save_password(password)
    elif args.encrypt:
        if not args.password_length:
            print(Fore.RED + 'Error: You must specify password length (-l) for encryption.')
            sys.exit(1)
        if not args.chars:
            print(Fore.RED + 'Error: You must specify characters to use for password generation (-t).')
            sys.exit(1)
        password = generate_password(args.password_length, args.chars)
        print(Fore.GREEN + 'Generated password: ' + password)
        save_password(password)
    elif args.decrypt:
        password = input("Enter the password for decryption: ")

    if args.encrypt:
        encrypt_file(args.file, password)
        print(Fore.GREEN + 'File encrypted successfully.')
    elif args.decrypt:
        decrypt_file(args.file, password)
        print(Fore.GREEN + 'File decrypted successfully.')

if __name__ == '__main__':
    main()
