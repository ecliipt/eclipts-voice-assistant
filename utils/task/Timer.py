import pygame
import threading
import datetime
import time

import utils.nlp.parse as parse
#import utils.nlp.numbers as numbers
import utils.logging as logging

global timer_threads
timer_threads = []
global timer_exit_flag
timer_exit_flag = threading.Event()

def play_alarm_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('data/sounds/alarm.wav') 
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def main(time=None):
    if time  == None: raise ValueError('No time was provided for the timer!')
    if not time.startswith('in'): time = 'in '+time
    try:
        timer_time = parse.Time(time)
        #print(timer_time)
        if timer_time == []: raise ValueError(
            'Unable to parse given schedule time. The time parser returned None-type object.'
            ) # if this happends, the time parser could just not parse shit
        current_time = datetime.datetime.now()
        time_difference = timer_time - current_time
        time_difference = time_difference.total_seconds()
        if time_difference <= 0: raise ValueError('Failed to set Timer: the scheduled time is negative or zero.')
    except Exception as e: raise ValueError(f'Could not parse timer schedule : {e}')
    try:
        timer_thread = threading.Thread(target=wait_and_ring, args=(time_difference,))
        timer_thread.start()
        timer_threads.append(timer_thread)
    except Exception as e: raise ValueError(f'Failed to run timer thread spawner: {e}')
    return ''

def wait_and_ring(time_difference):
    global timer_exit_flag
    #print(time_difference)
    
    time_elapsed = 0
    while time_elapsed < time_difference:
        global timer_exit_flag
        if timer_exit_flag.is_set():
            logging.info(f"Timer thread '{threading.current_thread().name}' exiting due to exit signal.", wait=False)
            return  # Exit gracefully if the flag is set
        time.sleep(1)  # Sleep for 1 second
        time_elapsed += 1

    if not timer_exit_flag.is_set():
        play_alarm_sound()
        logging.debug(f"Timer thread '{threading.current_thread().name}' finished successfully.")

def kill_threads(n=0):
    timer_exit_flag.set()
    for thread in timer_threads:
        thread.join()
        n+=1
    return f'killed {n} threads'