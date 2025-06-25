from colorama import Fore, Style, init
from os import path
from sys import exit

init(autoreset=True)

def error(fp, ln, msg, hint=None):
    if not path.exists(fp):
        print(f"{Fore.RED} Error → {Style.RESET_ALL}File '{fp}' not found.")
        exit(1)

    with open(fp, 'r') as f: lines = f.readlines()

    if ln < 1 or ln > len(lines):
        print(f"{Fore.RED} Error → {Style.RESET_ALL}Line '{ln}' is out of range.")
        exit(1)

    line = lines[ln - 1].rstrip('\n')
    pointer = f"{Style.BRIGHT}{Fore.RED}{'^' * len(line)}{Style.RESET_ALL}"

    print(f"{Style.BRIGHT}{Fore.RED}Error:{Style.RESET_ALL} {msg}")
    print(f"{Fore.CYAN} → File \"{fp}\", Line {ln}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{str(ln).rjust(4)} |{Style.RESET_ALL} {line}")
    print(f"     | {pointer}")
    if hint:
        print(f"{Fore.MAGENTA}Hint:{Style.RESET_ALL} {hint}")

    exit(1)

error('.gitignore', 41, 'This is a test error message.', 'Check your syntax.')