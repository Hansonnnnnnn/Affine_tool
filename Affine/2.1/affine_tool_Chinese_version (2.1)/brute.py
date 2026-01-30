import re
from affine import COPRIME_WITH_26, decrypt
from wordlist import get_dictionary_words

_WORD_RE = re.compile(r"[A-Za-z]+")

def score_by_dictionary(text: str, dictionary_words: set[str]) -> int:
    words = _WORD_RE.findall(text.lower())
    if not words:
        return 0
    hits = 0
    for w in words:
        if w in dictionary_words:
            hits += 1
    return hits

def brute_force_topk(ciphertext: str, top_k: int = 5):
    dictionary_words = get_dictionary_words()
    candidates = []

    for a in COPRIME_WITH_26:
        for b in range(26):
            plain = decrypt(ciphertext, a, b)
            s = score_by_dictionary(plain, dictionary_words)
            candidates.append((s, a, b, plain))

    candidates.sort(key=lambda t: t[0], reverse=True)

    out = []
    for s, a, b, plain in candidates[:top_k]:
        out.append({"score": s, "a": a, "b": b, "plain": plain})
    return out
