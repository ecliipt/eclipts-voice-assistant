import sys
from colorama import Fore, Style, init
init()

def error(output_text, visuals=True):
    if not visuals: return None
    #output_text = "".join(output_text)
    sys.stdout.write("\b" * int(len(output_text)+3)) # idk why 3 but it works
    sys.stdout.write(" " * len(output_text))  # Replace the word with spaces
    sys.stdout.write("\b" * len(output_text))
    print(f"\033[91m{output_text}\033[0m", end=" ", flush=True)

def Replace(output_text, replacement, visuals=True):
    if not visuals: return None
    output_text = output_text.split('{')
    #print(output_text)
    output_text.pop(0)
    output_text = '{'+"".join(output_text)
    sys.stdout.write("\b" * int(len(output_text)+1))
    sys.stdout.write(" " * len(output_text))
    sys.stdout.write("\b" * len(output_text))
    print(f"{Fore.WHITE}{replacement}{Fore.RESET}"+' '*(len(output_text)-len(replacement)+2), end="", flush=True)
    sys.stdout.write("\b" * (len(output_text)-len(replacement)+2))

if __name__ == '__main__':
    print(" {'Weather': {'place': 'here'}}", end="", flush=True)
    Replace(" {'Weather': {'place': 'here'}}", 'WEATHER CHECK OKKKKKKKKKKKKKKKKKKK! here None')