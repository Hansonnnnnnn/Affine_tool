from pathlib import Path
import re
from colors import warning, error

BASE_COMMON_WORDS = {
    "the","and","to","of","a","in","is","it","you","that","he","was","for","on",
    "are","as","with","his","they","i","at","be","this","have","from","or","one",
    "had","by","but","not","what","all","were","we","when","your","can","said",
    "there","use","an","each","which","she","do","how","their","if","will","up",
    "other","about","out","many","then","them","these","so","some","her","would",
    "make","like","him","into","time","has","look","two","more","go","see","no",
    "way","could","people","my","than","first","been","who","now","down","day",
    "did","get","come","made","may","part","over","new","after","work","most",
    "even","any","good","want","because","those","very","just","also","back",
    "here","think","only","take","know","year","our"
}

EXTRA_PATH = Path("data/extra_words.txt")
_WORD_RE = re.compile(r"[A-Za-z]+")

def load_extra_words(path: str = "data/extra_words.txt"):
    p = Path(path)
    if not p.exists():
        return set()

    words = set()
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            w = line.strip().lower()
            if not w:
                continue
            if w.startswith("#"):
                continue
            words.add(w)
    except (IOError, OSError, UnicodeDecodeError) as e:
        print(warning(f"Warning: Failed to load extra words from {path}: {e}"))
        return set()
    return words

def get_dictionary_words():
    return BASE_COMMON_WORDS | load_extra_words()

def extract_candidate_words(text: str, min_len: int = 4):
    tokens = _WORD_RE.findall(text.lower())
    out = set()
    for w in tokens:
        if len(w) < min_len:
            continue
        if w in BASE_COMMON_WORDS:
            continue
        out.add(w)
    return out

def append_extra_words(words: set[str]):
    if not words:
        return []

    try:
        existing = load_extra_words(str(EXTRA_PATH))
        new_words = sorted(w for w in words if w not in existing)

        if not new_words:
            return []

        EXTRA_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not EXTRA_PATH.exists():
            EXTRA_PATH.write_text(
                "# Add new common words here (one word per line) to improve brute-force accuracy over time.\n",
                encoding="utf-8",
            )

        with EXTRA_PATH.open("a", encoding="utf-8") as f:
            for w in new_words:
                f.write(w + "\n")

        return new_words
    except (IOError, OSError, PermissionError) as e:
        print(error(f"Error: Failed to append words to {EXTRA_PATH}: {e}"))
        return []
