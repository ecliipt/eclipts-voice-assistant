import json
import os

import threading
import datetime
import time
import pygame

import utils.nlp.parse as parse
import utils.logging as logging

global alarm_threads
alarm_threads = []

with open('data/configs.json', 'r') as k:
    alarm_configs = json.load(k)
    alarm_sound_path = alarm_configs['paths']['sounds']['alarm_sound_path']
    n_advance_days   = alarm_configs['inference']['util_features']['alarm_advance_day_limit']
    n_repeat_times   = alarm_configs['inference']['util_features']['alarm_sound_repeat']
    k.close()
global alarm_exit_flag
alarm_exit_flag = threading.Event()

def load_alarms():
    with open('data/cache/alarms.txt', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()

        for alarm_time_str in lines:
            try:
                alarm_time = datetime.datetime.strptime(alarm_time_str.strip(), "%Y-%m-%d %H:%M:%S")
                current_time = datetime.datetime.now()
                time_difference = alarm_time - current_time
                time_difference = time_difference.total_seconds()

                _time = (time_difference, alarm_time)

                if time_difference > 0:
                    alarm_thread = threading.Thread(target=wait_and_play_alarm, args=(_time,))
                    alarm_thread.start()
                    alarm_threads.append(alarm_thread)
                    logging.info(f"loaded alarm '{threading.current_thread().name}', \ntime as {alarm_time}, \n{time_difference} secs.", wait=False)
                else:
                    logging.info(f"Alarm '{threading.current_thread().name}' already elapsed: '{alarm_time}'", wait=False)

                # Write back the alarm_time_str only if it should not be removed.
                f.write(alarm_time_str) if time_difference > 0 else None
            except Exception as e:
                logging.fail(f"Exception in '{threading.current_thread().name}' while loading alarms: '{e}'", wait=False)
        f.close()




def main(schedule=None):
    if schedule == None: raise ValueError('Could not parse schedule, the argument was not provided.')
    datetime_schedule = str(parse.Time(schedule))
    logging.debug(f"parsed time from '{schedule}' to '{datetime_schedule}'")
    set_alarm(datetime_schedule)
    return ''


def play_alarm_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(alarm_sound_path) 
    for _ in range(n_repeat_times):
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

def is_within_time_range(date_str):

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Set the time to 4:00:00 for both current and next day
    current_day_start = current_datetime.replace(hour=4, minute=0, second=0, microsecond=0)
    next_day_start = current_day_start + datetime.timedelta(days=1)

    # Check if the input datetime is within the specified range
    if current_day_start <= date_str < next_day_start:
        return True
    return False

def delete_alarm_savings(string_to_delete, file_path='data/cache/alarms.txt'):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if string_to_delete not in line:
                    file.write(line)
    except Exception as e:
        logging.fail(f"Exception while removing alarm from savings: {e}", wait=False)


def set_alarm(alarm_time_str):
    try:
        # Remove any fractional seconds if present
        alarm_time_str = alarm_time_str.split('.')[0]
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logging.fail("Invalid datetime format. Use '%Y-%m-%d %H:%M:%S'")
        raise ValueError('Could not parse the requested alarm schedule time. Aborting...')

    current_time = datetime.datetime.now()
    time_difference = alarm_time - current_time
    time_difference = time_difference.total_seconds()

    # Check if the alarm is within 5 days from the current time
    #if is_within_time_range(alarm_time):
    if time_difference >= 0 and time_difference <= n_advance_days * 24 * 3600:
        #print(f"Setting alarm for {alarm_time}")
        if time_difference <= 0: raise ValueError('Failed to set alarm: the scheduled time is negative or zero.')
        try:
            _time = (time_difference, alarm_time)
            alarm_thread = threading.Thread(target=wait_and_play_alarm, args=(_time,))
            alarm_thread.start()
            alarm_threads.append(alarm_thread)
            with open('data/cache/alarms.txt', 'w') as f:
                f.write('\n'+str(alarm_time))
                f.close()
        except: raise ValueError('Failed to run the Alarm function. If this keeps happening, contact Eclipt to fix the code.')
    else:
        raise ValueError(f"Alarm can only be set for up to {n_advance_days} days in advance.")

"""def wait_and_play_alarm(time_difference):
    # Wait for the specified time before playing the alarm
    time.sleep(time_difference)
    play_alarm_sound()
    logging.debug(f"Alarm thread '{threading.current_thread().name}' finished successefully.")"""

def wait_and_play_alarm(time_difference):
    global alarm_exit_flag
    alarm_time = str(time_difference[1])
    time_difference = time_difference[0]
    
    time_elapsed = 0
    while time_elapsed < time_difference:
        global alarm_exit_flag
        if alarm_exit_flag.is_set():
            logging.info(f"Alarm thread '{threading.current_thread().name}' exiting due to exit signal.", wait=False)
            return  # Exit gracefully if the flag is set
        time.sleep(1)  # Sleep for 1 second
        time_elapsed += 1

    if not alarm_exit_flag.is_set():
        play_alarm_sound()
        delete_alarm_savings(alarm_time)
        logging.debug(f"Alarm thread '{threading.current_thread().name}' finished successfully.")


def kill_threads(n=0):
    #alarm_exit_flag = threading.Event()
    alarm_exit_flag.set()
    for thread in alarm_threads:
        thread.join()
        n+=1
    return f'(Alarm) killed {n} threads'

load_alarms()