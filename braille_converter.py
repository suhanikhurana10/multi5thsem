
BRAILLE_MAP = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    '0': '⠚', '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑', '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊',
    ',': '⠂', ';': '⠆', ':': '⠒', '.': '⠲', '!': '⠖', '(': '⠐⠣', ')': '⠐⠜', '?': '⠦',
    '/': '⠌', '#': '⠼', '-': '⠤',
    ' ': ' '
}

def to_braille(text):
    result = []
    is_number = False

    for char in text:
        if char.isdigit():
            if not is_number:
                result.append('⠼') # Number indicator
                is_number = True
            result.append(BRAILLE_MAP.get(char, char))
        elif char.isalpha():
            is_number = False
            if char.isupper():
                result.append('⠠') # Capital indicator
            result.append(BRAILLE_MAP.get(char.lower(), char))
        else:
            is_number = False
            result.append(BRAILLE_MAP.get(char, char))
    
    return "".join(result)
