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
        raise ValueError("无模逆")
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

def derive_key_from_first_letter(ciphertext: str, first_plain_letter: str):
    """
    根据密文和已知的第一个明文字母反推密钥 (a, b)
    返回 (a, b) 或 None（如果无法确定）
    """
    # 找到密文中第一个字母字符
    cipher_first = None
    for ch in ciphertext:
        if 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            cipher_first = ch
            break
    
    if cipher_first is None:
        return None
    
    # 确保第一个明文字母是有效的
    if len(first_plain_letter) == 0:
        return None
    plain_first = first_plain_letter[0]
    if not ('A' <= plain_first <= 'Z' or 'a' <= plain_first <= 'z'):
        return None
    
    # 转换为小写进行计算（保持大小写一致性）
    cipher_is_upper = 'A' <= cipher_first <= 'Z'
    plain_is_upper = 'A' <= plain_first <= 'Z'
    
    cipher_x = ord(cipher_first.upper()) - ord('A')
    plain_x = ord(plain_first.upper()) - ord('A')
    
    # 遍历所有可能的 a，计算对应的 b
    # 加密公式：cipher_x = (a * plain_x + b) % 26
    # 所以：b = (cipher_x - a * plain_x) % 26
    for a in COPRIME_WITH_26:
        b = (cipher_x - a * plain_x) % ALPHABET_SIZE
        # 验证：用这个密钥解密，检查第一个字母字符是否匹配
        decrypted = decrypt(ciphertext, a, b)
        # 找到解密后文本中第一个字母字符
        for decrypted_ch in decrypted:
            if 'A' <= decrypted_ch <= 'Z' or 'a' <= decrypted_ch <= 'z':
                if decrypted_ch.upper() == plain_first.upper():
                    return a, b
                break
    
    return None
