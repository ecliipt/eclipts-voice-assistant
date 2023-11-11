import re

def extract_function_args(text):
    function_str = match.group(1)
    if ";" not in function_str:
        return function_str, None
    parts = function_str.split('; ')
    func_name = parts[0].strip()
    args = {}
    for part in parts[1:][0].split(', '):
        key, value = part.strip().split('=')
        args[key.strip()] = value.strip()
    return func_name, args

def custom_split(input_string):
    result, current_word, inside_colon = [], '', False

    for char in input_string:
        current_word += char
        if char == ':':
            inside_colon = True
        elif char == ' ' and not inside_colon:
            result.append(current_word.strip())
            current_word = ''
        elif char != ':':
            inside_colon = False

    result.append(current_word.strip())
    return result

def replace_for_punct_error(input_string, exceptions_list = [': ', ', ', '{', '}', '}}', ',', ':']):
    try:
        for word in custom_split(input_string):
            found_exception = False
            for exception in exceptions_list:
                if exception in word:
                    found_exception = True
                    break
            if not found_exception:
                input_string = input_string.replace(word, word.replace("'", ""))
    except: pass
    return input_string

if __name__ == "__main__":
    while True:
        i = input('*')
        extract_function_args(i)
