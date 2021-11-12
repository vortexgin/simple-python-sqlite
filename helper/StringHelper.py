import random
import string

from math import ceil


def random_string(string_length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def mask_string(string_input, perc=0.6):
    mask_chars = ceil(len(string_input) * perc)
    return f'{string_input[:mask_chars]}{"*" * mask_chars}'
