# E.V.A project v5.0
The EVA series is a project i've been workin on in the past years. Originally it was only a nlp computer program, but as the time went on I made it into a full voice/virtual assistant and with the new llama cpp from meta I could finally run LLMs as the main component of the project.

It works by giving the LLM a prompt at the start with a few rules (it's persona and how to use placeholders) and than the session with the user starts. Once there the model just follows the instructions and uses the placeholders to form sentences with real time information and without using a complex and reasource expensive method. output ex: 'the current time in London is {'Time': {'place': 'London'}}' where Time is the function name to be called and place is the argument we give to that function, after that we simply replace the placeholder with the function's return text. It's not a very good method of getting a model to provide responses with real time info, but it was the easiest one i could find, as I'm very new to AI stuff.

![image (1)](https://github.com/ecliipt/llm_eva/assets/137305099/0bb8dfc0-a87a-4317-b51f-cdf9c7bc3cf0)
*in this image, we have the replace placeholder feature on, that's why some placeholders are not complete and some not even showed; the placeholder text is replaced by result of the action.

Premade actions: Time, Date/Day, Weather, News, Alarm, Timer, Music player, Look (radar to look for places in a region), Search

### install

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


