# vortex

vortex is a file encryption and decryption tool that uses AES-256. It provides strong password generation and management, with a simple command-line interface.

## Installation

1. Clone or download the source code to your local machine.
2. Install the required libraries:

       pip3 install cryptography colorama


## Usage

### Encrypting a File

To encrypt a file, use the `-e` option. You must specify the password length (`-l`) and the character set (`-t`) for password generation.


    python3 vortex.py -f <file_path> -e -l <password_length> -t <chars>

**Options:**

- `-f`, `--file`: Path to the file to encrypt.
- `-l`, `--password-length`: Length of the generated password.
- `-t`, `--chars`: Character set to use for the password. Options: `letter`, `number`, `extra`.
- `-c`, `--custom-password`: Use a custom password (if using this option, do not specify `-l` and `-t`).

Example:

    python3 vortex.py -f example.txt -e -l 12 -t letter number extra


### Decrypting a File

To decrypt a file, use the `-d` option. You will be prompted to enter the password.

    python3 vortex.py -f <file_path> -d


**Options:**

- `-f`, `--file`: Path to the encrypted file (`.vrtx` extension).
- `-d`, `--decrypt`: Decrypt the file.

Example:

    ```bash
    python3 vortex.py -f example.txt.vrtx -d
    ```

## Contact

For any questions or issues, please open an issue on GitHub or contact the project maintainers.
