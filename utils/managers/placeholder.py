import re
import json

from json.decoder import JSONDecodeError

def Match(text):
    try:
        text = text.replace("'", '"')
        pattern = r'\{(?:[^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'  # Regular expression pattern to match nested curly braces
        matches = re.findall(pattern, text)

        results = []
        for match in matches:
            data = json.loads(match)
            for key, value in data.items():
                return key, dict(value)

        return None

    except JSONDecodeError:
        raise ValueError("""Unable to parse json format, expecting "{'Function_name': {'Args': 'Args_text'}}"! """)
    except Exception as e:
        raise ValueError('Unable to parse json format: '+str(e))

def Replace(text, replacement):
    new_text = re.sub(r'\{.*?\}\}', replacement, text)
    return new_text

if __name__ == "__main__":
    print(Match(input('*')))