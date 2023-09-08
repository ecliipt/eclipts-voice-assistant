import os
import utils.logging as logging

def load_prompt(prompt_path, load_examples_config=True, n=1):
    prompt = []
    with open(prompt_path+'/persona.txt', 'r') as f:
        prompt.append(f.read())
        f.close()
    if load_examples_config:
        file_list = os.listdir(prompt_path+'/examples')
        examples = [file for file in file_list if file.endswith(".txt")]
        for example in examples:
            file_path = f'./{prompt_path}/examples/'+example
            with open(file_path, "r") as file:
                content = file.read().replace('\n', ' ')
                prompt.append(content)
                file.close()
            n+=1
    logging.info(f'loaded {n} examples from prompt', wait=False)
    return prompt, n

def remove_history(prompt, value, n_examples):
    while (len(prompt)-n_examples) >= value:
        prompt.pop(n_examples)
    return prompt

def get_word_frequency(text, word):
    return text.lower().split().count(word.lower())

def test(hello):
	return hello

def rearrange_examples(prompt, mods, query, n_examples):
    # replace prompt examples by best match for feature in query
    # we do this to increase the model preformance when building placeholders from the examples
    i_indexes = []
    k_indexes = []
    persona = prompt[0]
    prompt.pop(0)
    flagged_words = [word for word in reversed(mods) if word.lower() in query.lower()]

    if flagged_words:
        flagged_words.sort(key=lambda word: get_word_frequency(query, word), reverse=True)
        for word in flagged_words:
            matching_elements = [elem for elem in prompt if word.lower() in elem.lower()]
            matching_elements.sort(key=lambda elem: elem.lower().count(word.lower()), reverse=True)

            for elem in matching_elements:
                i_indexes.append(str(prompt.index(elem)))
                prompt.remove(elem)
                prompt.insert(n_examples-2, elem) # idk why 2 again, just works ig
                k_indexes.append(str(prompt.index(elem)))
    prompt.insert(0, persona)
    logging.debug(f"Rearranged {', '.join(i_indexes)} examples to {', '.join(k_indexes)}") #if k_indexes !=[] else None
    return prompt