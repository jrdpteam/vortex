import os
import time
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system("clear")

def print_ascii_art():
    print(f'''{Fore.RED}
                  _
   {Fore.YELLOW}! INSTALLER !{Fore.RED} | |
 __   _____  _ __| |_ _____  __
 \\ \\ / / _ \\| '__| __/ _ \\ \\/ /
  \\ V / (_) | |  | ||  __/>  <    {Fore.MAGENTA}v3.1{Fore.RED}
   \\_/ \___/|_|   \\__\\___/_/\\_\\
    ''' + Style.RESET_ALL)

def install_vortex():
    clear_screen()
    print_ascii_art()
    print("\nInstalling vortex...")
    time.sleep(0.1)
    os.system("chmod 777 vortex.py")
    os.system("chmod +x vortex.py")
    os.system("mkdir -p /usr/share/vortex")
    os.system("cp vortex.py /usr/share/vortex/vortex.py")

    cmnd = '#! /bin/sh \n exec python3 /usr/share/vortex/vortex.py "$@"'
    with open('/usr/bin/vortex', 'w') as file:
        file.write(cmnd)
    
    os.system("chmod +x /usr/bin/vortex && chmod +x /usr/share/vortex/vortex.py")

    desktop_entry = '''
[Desktop Entry]
Version=1.0
Name=vortex
Comment=vortex
Exec=python3 /usr/share/vortex/vortex.py
Icon=utilities-terminal
Terminal=true
Type=Application
Categories=Utility;
'''

    desktop_file_path = '/usr/share/applications/vortex.desktop'
    with open(desktop_file_path, 'w') as file:
        file.write(desktop_entry)

    os.system(f"chmod +x {desktop_file_path}")

    success_message = "vortex has been installed successfully.\nFrom now on, just type 'vortex -h' in the terminal."
    subprocess.Popen(["zenity", "--info", "--text", success_message, "--title", "Success"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def uninstall_vortex():
    clear_screen()
    print_ascii_art()
    print("\nUninstalling vortex...")
    time.sleep(0.4)

    os.system("rm -r /usr/share/vortex")
    os.system("rm /usr/bin/vortex")

    os.system("rm /usr/share/applications/vortex.desktop")

    success_message = "vortex has been uninstalled successfully."
    subprocess.Popen(["zenity", "--info", "--text", success_message, "--title", "Success"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main_menu():
    clear_screen()
    print_ascii_art()
    print("\nMenu:")
    print("1. Install vortex")
    print("2. Uninstall vortex")
    print("3. Exit")

    choice = input("\nEnter your choice (1/2/3): ")
    return choice

def check_sudo():
    return os.geteuid() == 0

if __name__ == "__main__":
    while True:
        if not check_sudo():
            print("Please run the installer with sudo privileges.")
            break

        choice = main_menu()

        if choice == '1':
            install_vortex()
        elif choice == '2':
            uninstall_vortex()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")
            time.sleep(1)
