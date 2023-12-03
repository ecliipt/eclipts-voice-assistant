from llama_cpp import Llama
from datetime import datetime
import inspect
import json
import copy
import utils.engines._importdir as importdir
import utils.logging as _logging
import time
import sys
import re
import os

old_time = time.time()

def reload(path='utils', items=[], unloaded=[]):
    importdir.do(path, globals())
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('_'):
                try: 
                    importdir.do(dirpath, globals())
                    items.append(filename.replace('.py', ''))
                except Exception as e: 
                    _logging.fail(f"Failed to load libraries from {filename}; {e}", wait=False)
                    unloaded.append(filename)
                    #exit(0)
    _logging.fail(f"Unable to load {len(unloaded)} modules. Please check for updates.\nIf the program was not able to load a certain module form a utils folder,\nthe program will FAIL to load any of the scripts inside that folder/dir!",
        wait=False) if len(unloaded) >= 1 else None
    return items

#####################################################################################

#configs
#model = "Wizard-Vicuna-7B-Uncensored.ggmlv3.q5_0.bin"

with open('data/configs.json', 'r') as k:
	configs    = json.load(k)
	k.close()

_model_configs     = configs["model_configs"]
_inference         = configs["inference"]
_path              = configs["paths"]

roles              = _model_configs['llm_model']['roles']
process_keys       = _model_configs['llm_model']['process_keys']

model              = _model_configs['llm_model']['model']
model_path         = _path["model_path"] +"/" + model

with open('data/model_card.json', 'r') as f:
    LLMconfigs     = json.load(f)[model]
    f.close()

internal_model_configs = LLMconfigs["model_configs"]
completion_configs = LLMconfigs["completion_configs"]
#model 

try: llm = Llama(model_path=model_path, **internal_model_configs)
except AttributeError as llama_model_unreachable: _logging.critical(
    'main ggml model file is out of reach or does not exist!', kill=True)
except Exception as llama_model_load_fail: _logging.critical(llama_model_load_fail, kill=True)

util_modules = reload() # it wont "re"-load shit, i just liked the name :P
task_modules = [mod for mod in util_modules if mod[0].isupper()]
logging.info(f'Loaded {len(task_modules)} task modules from {len(util_modules)} total imported utils.', wait=False)

import utils.logging as logging
#import utils.engines._listen as listen

system_msg = []

def prepare(_input, _goal, n=0):
    logging.info(f'Reading prompt & examples from {sys.getsizeof("".join(prompt))} bites of training data.', wait=False)
    _input = 'USER: '+_input+'. AGENT: '
    old_time_prepare = time.time()
    output_text=[]
    while _goal not in ''.join(output_text):
        output_text=[]
        stream = llm(
            " ".join(prompt)+_input,
            stream = True,
            **completion_configs
        )

        #print(datetime.now().strftime("%H:%M:%S |"), roles[1], end="", flush=True)
        for output in stream:
            completionFragment = copy.deepcopy(output)
            output = (completionFragment["choices"][0]["text"]).replace('\n', '')
            #print(output, end="", flush=True)
            output_text.append(output)
        n+=1
        print(n, "".join(output_text))
    eval_time=(time.time() - old_time_prepare) * 1000
    logging.info(f'Took {eval_time} ms and {n} tries to get acceptable placeholder result.', wait=False)
    if eval_time >= 200000: logging.warn('Took more than expected to prepare. Check VRAM & cpu memory for better preformance!', wait=False)
    if n >= 7: logging.warn('Too many tries to get acceptable placeholder result!\nCheck model weights and prompt length!', wait=False)
    return eval_time, n, _goal

def completion_manager(config_name, new_value):
    completion_configs[config_name] = float(new_value)
    return config_name, completion_configs[config_name]

def kill(value=0):
    logging.debug('Closing thread sessions...')
    for mod in util_modules:
        try: 
            function = globals()[mod].kill_threads
            logging.info(function())
        except: pass
    logging.critical(' Goodbye :-(', wait=False)
    exit(value)

def reset_prompt(value=1):
    prompt=prompt_manager.remove_history(
        prompt, value, n_examples)
    return prompt


def key_strip(output_text, sentence_keys, placeholder_call=False):
    text = "".join(output_text)
    if '{' in text and not '}' in text: return output_text
    for key in sentence_keys:
        if key in output_text[-1]:
            output_complete.append(text)
            if any(mod in text for mod in task_modules) and '}}' in text:
                placeholder_call = True
                text = output_format.replace_for_punct_error(input_string=text)
                function_name = None
                try: 
                    function_name, args = placeholder.Match(text)
                    RAW_result = invoke(function_name, args)
                    highlighter.Replace(text, RAW_result, visuals=_inference['extra_visuals'])
                    text = placeholder.Replace(text, RAW_result)
                except ValueError as placeholder_call_fail:
                    text = placeholder.Replace(text, 'Error, '+str(placeholder_call_fail))
                    highlighter.error(text, visuals=_inference['extra_visuals'])
                    error_output = f"Error calling {function_name}: {placeholder_call_fail}."
                    system_msg.append(error_output)
                    logging.sys(error_output, fail=True)
                    pass
                except Exception as placeholder_general_fail:
                    text = placeholder.Replace(text, 'Error, '+str(placeholder_general_fail))
                    highlighter.error(text, visuals=_inference['extra_visuals'])
                    error_output = f"Internal error occured while calling {function_name}."
                    system_msg.append(error_output)
                    logging.sys(error_output, exception=placeholder_general_fail, fail=True)
                    pass
            speaker.tts(text, placeholder=placeholder_call)
            output_text = []
            return []
    return output_text


def invoke(function_name, args):
    try: function = globals()[function_name].main
    except: raise ValueError(f"function '{function_name}' is out of reach or does not exist!") 
    if 'input' in args: args["_input_"] = args.pop("input")  # we do this for features like search
    if 'type' in args: args["_type_"] = args.pop("type")
    #valid_args = function.__annotations__.keys()
    signature = inspect.signature(function)
    valid_args = list(signature.parameters.keys())
    valid_args_values = {arg: value for arg, value in args.items() if arg in valid_args}
    logging.debug(
        f'({function_name}) of the {len(args)} provided args, {len(valid_args_values)} got passed as valid.'
        ) if len(args) > len(valid_args_values) else None
    try: return function(**valid_args_values)
    except Exception as task_internal_fail: raise ValueError(str(task_internal_fail))

prompt, n_examples = prompt_manager.load_prompt(_path["prompt_path"])
output_text     = []
output_complete = []

prepare('what is the time', _goal='}}') if _inference['load_weights_before_inference'] else None

logging.info(f'Took {str((time.time() - old_time) * 1000)} ms to load (total).', wait=False)

def vad_listen():
    try: 
        wakeword.Recognize()
        Music.kill_threads() # stop current music to listen correctly
        query = listen.Listen()
        logging.user_vad_query(query, roles[0])
        return query
    except KeyboardInterrupt:
        kill()
    except Exception as e: 
        logging.fail(e, wait=False)
        speaker.tts(f'Error while attempting to translate speech to text: {e}')
    return None

while True:
    logging.Flush()
    query = input(datetime.now().strftime("\n%H:%M:%S | "
        ) + roles[0]) if not _model_configs['vad_streaming']['active'] else vad_listen()
    if query == None: continue
    if query.startswith('.'):
        # .Module_name.function_name arg1=arg1 arg2=some-text-with-spaces
        # .function_name arg1=arg1 arg2=some-text-with-spaces
        module_name = False
        try:
            query = query.replace('.', '', 1).split(' ')
            function_name = query[0]
            if '.' in function_name:
                function_name = function_name.split('.')
                module_name   = function_name[0]
                function_name = function_name[1]
            query.pop(0)
            function_args = dict(arg.split('=') for arg in query)
            for f_key, f_value in function_args.items():
                 function_args[f_key] = f_value.replace("-", " ")
        except Exception as e: 
            logging.fail(f"Invalid format: {e}", wait=False)
            logging.Flush()
            continue
        try:
            if module_name:
                module = __import__(module_name)
                function = getattr(module, function_name)
            else: function = globals()[function_name]
            print(function(**function_args))
        except KeyError as invoke_fail: print(f'function {function_name} out of reach :', invoke_fail)
        except Exception as invoke_fail: print(invoke_fail)
        logging.Flush()
        continue
    prompt = prompt_manager.rearrange_examples(
        prompt=prompt,
        mods=task_modules,
        query=query,
        n_examples=n_examples
        ) if _model_configs['llm_model']['prompt_manager']['example_rearrange'] else prompt
    if not query.endswith(('.', '!', '?')):
        query = query+'.' # idk why but model preforms better with ponctuation at the end
    _input = roles[0]+query+' '+roles[1]
    print(datetime.now().strftime("%H:%M:%S |"), roles[1], end="", flush=True)
    for n_try in range(
        int(_model_configs['llm_model']['prompt_manager']['none_type_output_n_tries'])):
        stream = llm(
            " ".join(prompt)+' '+_input,
            stream = True,
            **completion_configs
        )

        for output in stream:
            completionFragment = copy.deepcopy(output)
            output = (completionFragment["choices"][0]["text"]).replace('\n', ' ')
            print(output, end="", flush=True)
            output_text.append(output)
            output_text = key_strip(output_text, process_keys)
        if "".join(output_complete) != "":
            break
        #logging.debug('None type output encountered! Retrying until acceptable response...')
    prompt.append(_input+"".join(output_complete))
    prompt=prompt_manager.remove_history(prompt, _model_configs['llm_model']['prompt_manager']['history_context_size']+1, n_examples)
    output_complete = []
    if system_msg != []:
        prompt.append(roles[2]+" ".join(system_msg))
        system_msg = []
    logging.Flush()
    #print(" ".join(prompt))
