from pathlib import Path

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
    "here","think","only","take","know","year","our","use","used","using",
    "problem","answer","cipher","decrypt","encrypt"
}

def load_extra_words(path: str = "data/extra_words.txt"):
    p = Path(path)
    if not p.exists():
        return set()
    words = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        w = line.strip().lower()
        if not w:
            continue
        if w.startswith("#"):
            continue
        words.add(w)
    return words

def get_dictionary_words():
    return BASE_COMMON_WORDS | load_extra_words()
