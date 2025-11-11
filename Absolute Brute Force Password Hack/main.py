import time
import itertools

chars = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
    "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    " ", "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
    "-", "_", "=", "+",
    "[", "]", "{", "}", "\\", "|",
    ";", ":", "'", "\"",
    ",", ".", "<", ">", "/", "?"
]


def crack_password(real_password):
    start = time.time()

    # Try increasing lengths until we reach the password length
    for length in range(1, len(real_password) + 1):
        for attempt in itertools.product(chars, repeat=length):
            guess = ''.join(attempt)
            if guess == real_password:
                end = time.time()
                print(f"Password cracked! '{guess}' found in {end - start:.2f} seconds.")
                return guess


# Example usage:
crack_password("password")