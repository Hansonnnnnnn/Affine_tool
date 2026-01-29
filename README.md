# Affine Cipher Tool

A clean, modular command-line toolkit for working with the **Affine Cipher**.  
This project supports encryption, decryption, and dictionary-based brute-force cryptanalysis, and is designed to be **extensible, interactive, and self-improving over time**.

> **Latest release:** v2.0.0

---

## Highlights (v2.0)

- **Growth Mode**: optionally learn new words from confirmed correct decryptions
- **Colorized CLI output** for clearer and more readable interaction
- Persistent menu loop with explicit exit option
- Improved usability for long-term experimentation

---

## Features

- Encrypt plaintext using a randomly generated Affine Cipher key
- Decrypt ciphertext using a provided key `(a, b)`
- Brute-force crack Affine Cipher ciphertexts using dictionary-based scoring
- Preserve spaces, punctuation, and non-letter characters
- Interactive command-line interface with looped menu
- Optional **Growth Mode** for adaptive dictionary learning
- Self-improving word dictionary for increasingly accurate cryptanalysis

---

## Project Structure

```
affine_tool/
├─ main.py          # CLI entry point and menu loop
├─ affine.py        # Core Affine Cipher math and transformations
├─ brute.py         # Brute-force cracking and scoring logic
├─ wordlist.py      # Dictionary management (base + user-extended)
├─ colors.py        # Colorized CLI output utilities
├─ data/
│  └─ extra_words.txt   # User-maintained word list for improving cracking accuracy
```

---

## Dictionary-Based Cryptanalysis

Instead of relying on a large external corpus, this tool uses a **lightweight and adaptive approach**:

- A built-in set of common English words
- An external `data/extra_words.txt` file that users can extend over time
- Each brute-force candidate is scored by how many dictionary words appear in the decrypted text

When **Growth Mode** is enabled, the user can confirm correct plaintext results.  
High-information words are then automatically appended to `extra_words.txt`, allowing the system to improve organically with continued use.

---

## Usage

Run the tool from the project root:

```bash
python main.py
```

You will be prompted to choose between:

```
0) Exit
1) Encrypt
2) Decrypt
3) Brute-force Crack
4) Toggle Growth Mode
```

---

## Design Philosophy

- **Separation of concerns**: cryptographic logic, scoring heuristics, UI, and data are clearly separated
- **Transparency**: all scoring and decisions are explainable and deterministic
- **Extensibility**: new scoring rules or learning strategies can be added with minimal changes
- **Educational focus**: designed for learning classical cryptography and cryptanalysis, not production security

---

## Notes

This project is intended for **educational and experimental purposes**.  
The Affine Cipher is **not secure** by modern cryptographic standards and should not be used to protect real data.

---

## License

MIT License
