import pvporcupine
from pvrecorder import PvRecorder
import sys
import time
import threading

global wake_exit_flag
wake_exit_flag = threading.Event()

anim_threads = []

def animation_thread():
    global wake_exit_flag
    while not wake_exit_flag.is_set():
        for char in ['|', '/', '-', '\\',]:
            if wake_exit_flag.is_set(): break
            sys.stdout.write(f'\r{char}')
            sys.stdout.flush()
            time.sleep(0.2)

def kill_threads():
    #alarm_exit_flag = threading.Event()
    wake_exit_flag.set()
    for thread in anim_threads:
        thread.join()
    return True


def Recognize():
    global wake_exit_flag
    wake_exit_flag.clear()
    animation = threading.Thread(target=animation_thread)

    porcupine = pvporcupine.create(
        access_key='1JbZAcd6BfuAaGBpFw9nFzLcPVPWJq3GuaUe98cRwqnwkyrHyS2/Bw==',
        keyword_paths=['./models/Hey-Eva_en_windows_v2_2_0.ppn'])
    
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

    animation.start()
    anim_threads.append(animation)
    
    try:
        recorder.start()
        while True:
            keyword_index = porcupine.process(recorder.read())
            if keyword_index >= 0:
                wake_exit_flag.set()
                print(f"\r[Detected]")
                break
        recorder.stop()
        for thread in anim_threads:
            thread.join()
        return True
    except Exception as e:
        wake_exit_flag.set()
        for thread in anim_threads:
            thread.join()
        recorder.stop()
        # idk what to do here
        raise ValueError(e)
    finally:
        porcupine.delete()
        recorder.delete()
