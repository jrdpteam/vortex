# vortex

Vortex is a file encryption and decryption tool using the AES algorithm, created by the JRDP team. It allows for generating passwords of specified length and characters, as well as using custom passwords.

## Requirements

- Python 3.x
- Modules:
  - cryptography
  - colorama

## Installation

To install the required modules, run:

    pip3 install cryptography colorama

## Usage

Encrypting a File

To encrypt a file, use the following command:

    python3 vortex.py -f <file_path> -e -l <password_length> -t <chars_to_use>

Example:

    python3 vortex.py -f document.txt -e -l 16 -t letter number extra

Decrypting a File

To decrypt a file, use the following command:

    python3 vortex.py -f <encrypted_file_path> -d

When you run the decryption command, the program will prompt you to enter the password used for encryption.

Example:

    python3 vortex.py -f document.txt.vrtx -d

Using a Custom Password

To encrypt a file using a custom password, use:

    python3 vortex.py -f <file_path> -e -c <password>

Example:

    python3 vortex.py -f document.txt -e -c my_custom_password

Options

    -f, --file: Path to the file to be encrypted/decrypted (required)
    -l, --password-length: Length of the generated password (required for encryption if -c is not used)
    -t, --chars: Characters to use for password generation (options: letter, number, extra)
    -c, --custom-password: Use a custom password
    -e, --encrypt: Encrypt the file
    -d, --decrypt: Decrypt the file

Example Commands
Encrypting with Generated Password

    python3 vortex.py -f example.txt -e -l 16 -t letter number

Encrypting with Custom Password

    python3 vortex.py -f example.txt -e -c my_secure_password

Decrypting a File

    python3 vortex.py -f example.txt.vrtx -d
