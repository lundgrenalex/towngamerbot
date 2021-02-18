import re

def is_word_in_chain(first_word: str, second_word: str) -> bool:
    stop_symbols = ['ы', 'ь', 'ё', 'ъ']
    first_word = first_word.lower()
    second_word = second_word.lower()
    for stsm in stop_symbols:
        first_word = first_word.replace(stsm, '')
    fw_chain = list(first_word)
    sw_chain = list(second_word)
    return fw_chain[-1:][0] == sw_chain[0]

def normalize_city_name(city: str) -> str:
    stop_symbols = ['ы', 'ь', 'ё', 'ъ']
    for stsm in stop_symbols:
        city = city.replace(stsm, '')
    return city

def render_template(template_name: str, *args) -> str:
    with open(f'./templates/{template_name}.md', 'r') as template_file:
        return (template_file.read()).format(*args)

def check_obscenity(text: str) -> bool:
    obscenity_regex = r'(хуй|пизд|ебать|еблан|мудак|блять)'
    return True if re.search(obscenity_regex, text) else False
