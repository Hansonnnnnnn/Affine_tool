import random

ALPHABET_SIZE = 26
COPRIME_WITH_26 = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)

def is_valid_a(a: int) -> bool:
    return a in COPRIME_WITH_26

def random_key():
    a = random.choice(COPRIME_WITH_26)
    b = random.randint(0, 25)
    return a, b

def _egcd(a: int, b: int):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = _egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a: int, m: int) -> int:
    g, x, _ = _egcd(a, m)
    if g != 1:
        raise ValueError("no modular inverse")
    return x % m

def encrypt(text: str, a: int, b: int) -> str:
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            x = ord(ch) - ord('A')
            y = (a * x + b) % ALPHABET_SIZE
            out.append(chr(y + ord('A')))
        elif 'a' <= ch <= 'z':
            x = ord(ch) - ord('a')
            y = (a * x + b) % ALPHABET_SIZE
            out.append(chr(y + ord('a')))
        else:
            out.append(ch)
    return ''.join(out)

def decrypt(text: str, a: int, b: int) -> str:
    a_inv = modinv(a, ALPHABET_SIZE)
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            y = ord(ch) - ord('A')
            x = (a_inv * (y - b)) % ALPHABET_SIZE
            out.append(chr(x + ord('A')))
        elif 'a' <= ch <= 'z':
            y = ord(ch) - ord('a')
            x = (a_inv * (y - b)) % ALPHABET_SIZE
            out.append(chr(x + ord('a')))
        else:
            out.append(ch)
    return ''.join(out)
