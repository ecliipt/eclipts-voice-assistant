import datetime
from colorama import Fore, Style, init
init()
import json
import re

with open('data/configs.json', 'r') as k:
    configs    = json.load(k)
    k.close()

verbose = configs["inference"]["verbose"]

global queue
queue = []
# here we wait for the model to finnish generating it's response and only than release the
# loggins with the correct timings.

def time():
    return str(datetime.datetime.now().strftime('%H:%M:%S'))

def Flush():
    global queue
    print()
    for i in queue:
        print(i)
    queue = []

def user_vad_query(text, role):
    text = '\x1b[A'+time()+f' | {role}{text}'
    print(text)


def info(text, wait=True):
    text = text.replace('\n', '\n'+' '*17)
    text = time()+' | INFO: '+re.sub(r'[^\x00-\x7F]+', '_NON-ASCII_', text)
    queue.append(text) if wait else print (text)

def debug(text):
    if verbose:
        text = text.replace('\n', '\n'+' '*17)
        text = time()+' | DEBUG: '+re.sub(r'[^\x00-\x7F]+', '_NON-ASCII_', text)
        queue.append(text)

def fail(text, wait=True, signal=True):
    if not wait: signal=False
    text = str(text)
    text = text.replace('\n', '\n'+' '*17)
    text = time()+f' |{Fore.LIGHTRED_EX} FAIL: '+re.sub(r'[^\x00-\x7F]+', '_NON-ASCII_', text)+Fore.RESET
    queue.append(text) if wait else print (text)
    print(f'{Fore.LIGHTRED_EX} * {Fore.RESET}', end="", flush=True) if signal else None

def warn(text, wait=True, signal=True):
    if not wait: signal=False
    text = text.replace('\n', '\n'+' '*17)
    text = time()+f' |{Fore.YELLOW} WARNING: '+re.sub(r'[^\x00-\x7F]+', '_NON-ASCII_', text)+Fore.RESET
    queue.append(text) if wait else print (text)
    print(f'{Fore.YELLOW} * {Fore.RESET}', end="", flush=True) if signal else None

def sys(text, exception='', fail=False, warn=False):
    text = re.sub(r'[^\x00-\x7F]+', '_NON-ASCII_', text)
    text = text.replace('\n', '\n'+' '*19)
    exception = str(exception)
    if fail and warn: raise ValueError("Both 'fail' and 'warn' args are active at the same time!")
    if warn: text = time()+f' | {Fore.YELLOW}SYSTEM: '+ text + exception + Fore.RESET
    elif fail: text = time()+f' | {Fore.LIGHTRED_EX}SYSTEM: '+ text + exception + Fore.RESET
    else: text = time()+' | SYSTEM: '+ text
    
    queue.append(text)

def critical(text, wait=True, signal=True, kill=False):
    if not wait: signal=False
    if kill: signal, wait = False # , False
    text = str(text)
    text = text.replace('\n', '\n'+' '*21)
    text = time()+f' |{Fore.RED} CRITICAL: '+re.sub(r'[^\x00-\x7F]+', '_NON-ASCII_', text)+Fore.RESET
    queue.append(text) if wait else print (text)
    print(f'{Fore.RED} * {Fore.RESET}', end="", flush=True) if signal else None
    exit(0) if kill else None