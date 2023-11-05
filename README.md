# E.V.A project v5.0
The EVA series is a project i've been workin on in the past years. Originally it was only a nlp computer program, but as the time went on I made it into a full voice/virtual assistant and with the new llama cpp from meta I could finally run LLMs as the main component of the project.

It works by giving the LLM a prompt at the start with a few rules (it's persona and how to use placeholders) and than the session with the user starts. Once there the model just follows the instructions and uses the placeholders to form sentences with real time information and without using a complex and reasource expensive method. output ex: 'the current time in London is {'Time': {'place': 'London'}}' where Time is the function name to be called and place is the argument we give to that function, after that we simply replace the placeholder with the function's return text. It's not a very good method of getting a model to provide responses with real time info, but it was the easiest one i could find, as I'm very new to AI stuff.

### Why use a LLM?
In order to make the responses more generative and human-like and also give them reason, I concluded that using a large language model, like what we do here, can lead to better natural language understanding of the user's intent, so you don't have to code an assistant with a lot of nlp techniques that might not work accordingly, it provides reasoning to it's answers and can also casually chat with the user while still providing information by placeholders. It is also much easier to try to manipulate the models answers using context history data than it is to train nlp models and code an entire assistant made out of nlp techniques (i've tried to do it before aswell).
Even though LLMs might not always be 100% reliable with the usage of these placeholders and correct information, I believe the upsides of using one ultrapass the downsides.

![image (1)](https://github.com/ecliipt/llm_eva/assets/137305099/0bb8dfc0-a87a-4317-b51f-cdf9c7bc3cf0)
*in this image, we have the replace placeholder feature on, that's why some placeholders are not complete and some not even showed; the placeholder text is replaced by result of the action.*

Premade actions: Time, Date/Day, Weather, News, Alarm, Timer, Music player, Look (radar to look for places in a region), Search

## install

run 'pip install -r requirements.txt' to install needed requirements.

tested on: python 3.8.2, Windows 11 x64

download the following models and place them in a new folder named 'models':

  (for the llama choose the q5_0 version)

  main llama : https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GGML/tree/main
  
  wakeword   : https://www.mediafire.com/file/o7xvgrvvvor2twr/Hey-Eva_en_windows_v2_2_0.ppn/file
  
  vosk models:
  - https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
  - https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip
  
  tts modes:
  - https://www.mediafire.com/file/j9yktrcg687tmdr/glados.pt/file
  - https://www.mediafire.com/file/stfxpjc8zaxih4w/vocoder-cpu-hq.pt/file
  - https://www.mediafire.com/file/o7xvgrvvvor2twr/Hey-Eva_en_windows_v2_2_0.ppn/file
  - https://www.mediafire.com/file/yfj085rxn2ggnng/vocoder-gpu.pt/file

<details>
<summary>How to add actions</summary>
<br>
How to add actions:
  
- go to `data/prompt/examples` and add a new text file with an example of the usage of your function for the model to real. Keep it as short and simple as possible.
- go to `utils/task` and create a new python script with the name that you've set in your example's placeholder.
- in your new script, you are free to execute all the code you need, however a main function is required with all the arguments you've set on your example, so the program can call the action, and you must also return some text in that same function, to replace the placeholder with something. (please check already made action scripts for better understanding).
- there is no need to import your action script in the main script as it already does so auto.
- next, test if the model is able to use the placeholder accurately, if not so, try:
  - reducing the temperature at `data/model_card.json`.
  - make your example file more simple and clear.
  - try reducing your example length to as small as possible.
  - if none of the above work, you can always sacrifice another example you might not like as much ¯\_(ツ)_/¯  
</details>

## Possible errors you might get
* please remember this repo was only tested in win10 and win11 machines.

<details>
<summary>pafy youtube-dl not found</summary>
<br>
Error: "pafy: youtube-dl not found; you can use the internal backend by setting the environmental variable PAFY_BACKEND to "internal". It is not enabled by default because it is not as well maintained as the youtube-dl backend."

Solution:
- open pafy's "backend_youtube_dll.py" script at libs
- replace "import youtube_dl" with "import yt_dlp as youtube_dl"
- pip install youtube-dl
</details>
<details>
<summary>Could not find module (...)libvlc.dll - vlc error </summary>
<br>
Error: "Could not find module 'C:\Users\USERNAME\Desktop\eclipts-voice-assistant\libvlc.dll' (or one of its dependencies). Try using the full path with constructor syntax."

Solution:
- install the vlc program from https://www.videolan.org/
- in the installer, make sure to copy the destination folder path (ex: C:\Program Files\VideoLAN\VLC) and replace the default path in "os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')" at utils/task/Music.py with your path.
- NOTE: if your python is 64bits, your vlc must be 64bits aswell.
</details>
