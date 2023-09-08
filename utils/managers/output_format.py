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

if __name__ == "__main__":
	while True:
		i = input('*')
		extract_function_args(i)