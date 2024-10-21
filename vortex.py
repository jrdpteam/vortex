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

ascii_art = r"""
                  _            
                 | |           
 __   _____  _ __| |_ _____  __
 \ \ / / _ \| '__| __/ _ \ \/ /
  \ V / (_) | |  | ||  __/>  < 
   \_/ \___/|_|   \__\___/_/\_\
"""

def print_ascii_art():
    print(Fore.RED + ascii_art)

def colorful_help():
    print(Fore.YELLOW + "vortex v3.0    " + Fore.MAGENTA + "by JRDP Team 2024")
    print(Fore.CYAN + "\nUsage:")
    print(Fore.GREEN + "  vortex.py [-h] -f FILE [-l PASSWORD_LENGTH] [-t CHARS [CHARS ...]]")
    print(Fore.GREEN + "            [-c CUSTOM_PASSWORD] [-e] [-d]\n")
    print(Fore.CYAN + "Options:")
    print(Fore.BLUE + "  -h, --help               " + Fore.RESET + "Show this help message and exit")
    print(Fore.BLUE + "  -f FILE, --file FILE     " + Fore.RESET + "File to encrypt/decrypt")
    print(Fore.BLUE + "  -l PASSWORD_LENGTH, --password-length PASSWORD_LENGTH" + Fore.RESET + " Length of password")
    print(Fore.BLUE + "  -t CHARS [CHARS ...], --chars CHARS [CHARS ...]" + Fore.RESET + " Characters to use for password generation (letter, number, extra)")
    print(Fore.BLUE + "  -c CUSTOM_PASSWORD, --custom-password CUSTOM_PASSWORD" + Fore.RESET + " Use custom password")
    print(Fore.BLUE + "  -e, --encrypt            " + Fore.RESET + "Encrypt file")
    print(Fore.BLUE + "  -d, --decrypt            " + Fore.RESET + "Decrypt file")
    print(Fore.CYAN + "\nContact: " + Fore.RESET + "https://jrdpteam.netlify.app")
    print(Fore.CYAN + "GitHub:  " + Fore.RESET + "https://github.com/jrdpteam")

print_ascii_art()

def generate_password(length, chars):
    char_set = ''
    if 'letter' in chars:
        char_set += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if 'number' in chars:
        char_set += '0123456789'
    if 'extra' in chars:
        char_set += '_-'
    
    if not char_set:
        print(Fore.RED + 'Error: No valid characters specified for password generation.')
        sys.exit(1)
        
    password = ''.join(random.choice(char_set) for _ in range(length))
    return password

def encrypt_file(file_path, password):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except IOError as e:
        print(Fore.RED + f'Error reading file: {e}')
        sys.exit(1)
    
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
    
    temp_file_path = file_path + '.tmp'
    try:
        with open(temp_file_path, 'wb') as f:
            f.write(salt + iv + encrypted_data)
    except IOError as e:
        print(Fore.RED + f'Error writing encrypted file: {e}')
        sys.exit(1)
    
    os.remove(file_path)
    shutil.move(temp_file_path, file_path + '.vrtx')

def decrypt_file(file_path, password):
    if not file_path.endswith('.vrtx'):
        print(Fore.RED + 'Error: File is not encrypted.')
        sys.exit(1)
    
    temp_file_path = file_path[:-5] + '.tmp'
    try:
        with open(file_path, 'rb') as f:
            salt = f.read(16)
            iv = f.read(16)
            encrypted_data = f.read()
    except IOError as e:
        print(Fore.RED + f'Error reading encrypted file: {e}')
        sys.exit(1)
    
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
    
    try:
        with open(temp_file_path, 'wb') as f:
            f.write(decrypted_data)
    except IOError as e:
        print(Fore.RED + f'Error writing decrypted file: {e}')
        sys.exit(1)
    
    os.remove(file_path)
    shutil.move(temp_file_path, file_path[:-5])

def save_password(password):
    try:
        with open('password.vortex', 'w') as f:
            f.write(password)
    except IOError as e:
        print(Fore.RED + f'Error saving password: {e}')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description=Fore.YELLOW + 'vortex v3.0    ' + Fore.MAGENTA + 'by JRDP Team 2024\n' +
                                     Fore.CYAN + "Contact: " + Fore.RESET + "https://jrdpteam.netlify.app\n" +
                                     Fore.CYAN + "GitHub:  " + Fore.RESET + "https://github.com/jrdpteam", 
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--file', help=Fore.BLUE + 'File to encrypt/decrypt' + Fore.RESET, required=True)
    parser.add_argument('-l', '--password-length', type=int, help=Fore.BLUE + 'Length of password' + Fore.RESET)
    parser.add_argument('-t', '--chars', help=Fore.BLUE + 'Characters to use for password generation (letter, number, extra)' + Fore.RESET, nargs='+')
    parser.add_argument('-c', '--custom-password', help=Fore.BLUE + 'Use custom password' + Fore.RESET)
    parser.add_argument('-e', '--encrypt', help=Fore.BLUE + 'Encrypt file' + Fore.RESET, action='store_true')
    parser.add_argument('-d', '--decrypt', help=Fore.BLUE + 'Decrypt file' + Fore.RESET, action='store_true')
    
    if len(sys.argv) == 1:
        colorful_help()
        sys.exit(1)

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(Fore.RED + f'Error: File {args.file} does not exist.')
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
        password = input(Fore.YELLOW + "Enter the password for decryption: ")

    if args.encrypt:
        encrypt_file(args.file, password)
        print(Fore.GREEN + 'File encrypted successfully.')
    elif args.decrypt:
        decrypt_file(args.file, password)
        print(Fore.GREEN + 'File decrypted successfully.')

if __name__ == '__main__':
    main()
