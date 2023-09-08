import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import sys
import json

import utils.logging as logging

with open('data/configs.json', 'r') as k:
    configs = json.load(k)
    k.close()

_path = configs['paths']['model_path']
configs = configs['model_configs']['vad_streaming']

'''This script processes audio input from the microphone and displays the transcribed text.'''
    
# list all audio devices known to your system
#print("Display input/output devices")
#print(sd.query_devices())


device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
logging.info("Default device number:{} description: \n{}".format(sd.default.device[0], device_info), wait=False)

# setup queue and callback function
q = queue.Queue()

def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
# build the model and recognizer objects.
logging.info("Building stt model and recognizer objects", wait=False)
model = Model(rf"{_path}/{configs['model']}")
recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)

def translate_KaldiRecognizer():
    data = q.get()        
    if recognizer.AcceptWaveform(data):
        recognizerResult = recognizer.Result()
        # convert the recognizerResult string into a dictionary  
        resultDict = json.loads(recognizerResult)
        if not resultDict.get("text", "") == "":
            result = resultDict['text']
            if result.startswith('the '):
                result = result.replace('the ', '', 1)
            return result
        else:
            raise ValueError('no input sound')
    return None

def Listen():
    q.queue.clear()
    logging.info('Listening', wait=False)
    with sd.RawInputStream(dtype=configs['dtype'],
                            channels=1,
                            callback=recordCallback):
        while True:
            text = translate_KaldiRecognizer()
            if text != None: return text

if __name__ == "__main__":
    while True: print(Listen())