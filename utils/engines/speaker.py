import torch
from utils.engines.utils.tools import prepare_text
#except: from utils.tools import prepare_text
from scipy.io.wavfile import write
from threading import Thread

import re
import time
from sys import modules as mod

import json
with open('data/configs.json', 'r') as k:
    configs = json.load(k)
    k.close()
_path   = configs['paths']
configs = configs['model_configs']['speaker_tts']
_active_ = configs['active']

try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    os.environ['PHONEMIZER_ESPEAK_LIBRARY'] = _path['speaker_tts']['PHONEMIZER_ESPEAK_LIBRARY'] #'C:\Program Files\eSpeak NG\libespeak-ng.dll'
    os.environ['PHONEMIZER_ESPEAK_PATH'] = _path['speaker_tts']['PHONEMIZER_ESPEAK_PATH'] #'C:\Program Files\eSpeak NG\espeak-ng.exe'
except ImportError:
    from subprocess import call
from pygame import mixer
mixer.init()

# Select the device
if torch.is_vulkan_available(): device = 'vulkan'
if torch.cuda.is_available(): device = 'cuda'
else: device = 'cpu'

# Load models
glados = torch.jit.load(_path['model_path']+'/'+configs['models']['main'])  #('models/glados.pt')
vocoder = torch.jit.load(_path['model_path']+'/'+configs['models']['vocoder'], map_location=device) # 'models/vocoder-gpu.pt'

#global n
global queue
queue_n = 0
queue = {}


# Prepare models in RAM
for i in range(2):
    init = glados.generate_jit(prepare_text(str(i)))
    init_mel = init['mel_post'].to(device)
    init_vo = vocoder(init_mel)

def big_text_manager(text):
    text = text.replace('\n', '')
    #text = re.split(r'[.!?:]', text)
    text = re.split(r'(?<=[0-9])[.!?:](?=[0-9])|(?<=[0-9])[.,](?=[0-9])', text)
    text = [q.strip() for q in text if q.strip()]
    return text

def tts(text):
    if not _active_: return None
    global queue_n
    #print('<s>'+text+'</s>')
    if len(text) >= 150:
        for i in big_text_manager(text):
            queue[queue_n] = i
            onWaitThread = Thread(target=speech_wait, args=(queue_n,))
            onWaitThread.start()
            queue_n+=1
    else:
        queue[queue_n] = text.replace('\n', '')
        onWaitThread = Thread(target=speech_wait, args=(queue_n,))
        onWaitThread.start()
        queue_n+=1

def speech_wait(numb):
    while True:
        if numb in queue and list(queue.keys())[0] == numb:
            synthesize = Thread(target=synthesizer, args=(queue[numb], numb))
            synthesize.start()
            break

def playsound(name, _dir='./sounds/'):
    sound = mixer.Sound(_dir+name)
    sound.play()
    return sound.get_length()+0.1


def synthesizer(text, numb):
    x = prepare_text(text).to('cpu')

    with torch.no_grad():

        # Generate generic TTS-output
        old_time = time.time()
        tts_output = glados.generate_jit(x)
        #print("Forward Tacotron took " + str((time.time() - old_time) * 1000) + "ms")

        # Use HiFiGAN as vocoder to make output sound like GLaDOS
        old_time = time.time()
        mel = tts_output['mel_post'].to(device)
        audio = vocoder(mel)
        #print("HiFiGAN took " + str((time.time() - old_time) * 1000) + "ms")
        
        # Normalize audio to fit in wav-file
        audio = audio.squeeze()
        audio = audio * 32768.0
        audio = audio.cpu().numpy().astype('int16')
        output_file = (configs['output_file'])
        
        write(output_file, 22050, audio)

        #print(numb, queue, queue_n)

        time.sleep(playsound(output_file, './'))
        queue.pop(numb, None)


if __name__ == "__main__":
    while True:
        tts(input('*'))