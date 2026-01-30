from affine import random_key, encrypt, decrypt, is_valid_a, derive_key_from_first_letter
from brute import brute_force_topk
from wordlist import extract_candidate_words, append_extra_words
from colors import title, success, error, warning, info, highlight, key_value, separator, colorize, Colors

def _read_int(prompt: str):
    s = input(prompt).strip()
    try:
        return int(s)
    except ValueError:
        return None

def _read_tf(prompt: str):
    s = input(prompt).strip().lower()
    return s in ("t", "true", "y", "yes", "1")

def main():
    growth_mode = False

    while True:
        print("\n" + separator())
        print(title("Affine Cipher Tool (v2.1)"))
        print("0) Exit")
        print("1) Encrypt")
        print("2) Decrypt")
        print("3) Brute-force Crack (dictionary scoring)")
        growth_status = success("ON") if growth_mode else warning("OFF")
        print(f"4) Toggle Growth Mode (currently {growth_status})")
        print(separator())

        choice = input("Choose (0/1/2/3/4): ").strip()

        if choice == "0":
            print(info("Exited."))
            break

        elif choice == "4":
            growth_mode = not growth_mode
            status = success("ON") if growth_mode else warning("OFF")
            print(f"Growth Mode is now {status}.")
            continue

        elif choice == "1":
            plaintext = input("Enter plaintext: ")
            a, b = random_key()
            ciphertext = encrypt(plaintext, a, b)
            print("\n" + title("=== Encryption Result ==="))
            print(key_value("Ciphertext", ciphertext))
            print(key_value("Key", f"a={a}, b={b}"))

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            a = _read_int("Enter key a: ")
            b = _read_int("Enter key b: ")

            if a is None or b is None:
                print(error("Error: a and b must be integers."))
                continue

            if not is_valid_a(a):
                print(error("Error: a must be coprime with 26."))
                continue

            if not (0 <= b <= 25):
                print(error("Error: b must be in the range 0..25."))
                continue

            plaintext = decrypt(ciphertext, a, b)
            print("\n" + title("=== Decryption Result ==="))
            print(key_value("Plaintext", plaintext))

            if growth_mode:
                ok = _read_tf("Is this plaintext correct? (T/F): ")
                if ok:
                    words = extract_candidate_words(plaintext, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"Growth Mode: added {len(added_words)} new word(s) to data/extra_words.txt:"))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("Growth Mode: no new words to add."))
                else:
                    # 用户说不正确，询问是否纠正
                    correct = _read_tf("Do you want to correct it? (T/F): ")
                    if correct:
                        print(info("Affine cipher only needs to know the position of any one letter to derive the key."))
                        print(info("Please enter the first letter of the plaintext:"))
                        first_letter = input("First letter: ").strip()
                        
                        if not first_letter:
                            print(error("Error: First letter cannot be empty."))
                            continue
                        
                        # 根据第一个字母反推密钥
                        key_result = derive_key_from_first_letter(ciphertext, first_letter)
                        if key_result is None:
                            print(error("Error: Failed to derive key from first letter. Please check your input."))
                            continue
                        
                        new_a, new_b = key_result
                        corrected_plaintext = decrypt(ciphertext, new_a, new_b)
                        
                        print("\n" + title("=== Corrected Decryption Result ==="))
                        print(key_value("Plaintext", corrected_plaintext))
                        print(key_value("Derived Key", f"a={new_a}, b={new_b}"))
                        
                        # 记录单词到词典
                        words = extract_candidate_words(corrected_plaintext, min_len=4)
                        added_words = append_extra_words(words)
                        if added_words:
                            print(success(f"Growth Mode: added {len(added_words)} new word(s) to data/extra_words.txt:"))
                            print(info(f"  {', '.join(added_words)}"))
                        else:
                            print(warning("Growth Mode: no new words to add."))
                    else:
                        print(warning("Growth Mode: correction cancelled, nothing added."))

        elif choice == "3":
            ciphertext = input("Enter ciphertext to crack: ")
            k = _read_int("Show top K candidates (default 5): ")
            if k is None or k <= 0:
                k = 5

            results = brute_force_topk(ciphertext, top_k=k)

            print("\n" + title("=== Brute-force Candidates ==="))
            for idx, r in enumerate(results, 1):
                score_str = success(str(r['score'])) if r['score'] > 0 else warning(str(r['score']))
                print(f"\n{info(f'[{idx}]')} {colorize('score', Colors.CYAN)}: {score_str}   {key_value('a', str(r['a']))} {key_value('b', str(r['b']))}")
                print(highlight(r["plain"]))

            if growth_mode and results:
                ok = _read_tf("Is the #1 candidate correct? (T/F): ")
                if ok:
                    top_plain = results[0]["plain"]
                    words = extract_candidate_words(top_plain, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"Growth Mode: added {len(added_words)} new word(s) to data/extra_words.txt:"))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("Growth Mode: no new words to add."))
                else:
                    # 用户说不正确，询问是否纠正
                    correct = _read_tf("Do you want to correct it? (T/F): ")
                    if correct:
                        print(info("Affine cipher only needs to know the position of any one letter to derive the key."))
                        print(info("Please enter the first letter of the plaintext:"))
                        first_letter = input("First letter: ").strip()
                        
                        if not first_letter:
                            print(error("Error: First letter cannot be empty."))
                            continue
                        
                        # 根据第一个字母反推密钥
                        key_result = derive_key_from_first_letter(ciphertext, first_letter)
                        if key_result is None:
                            print(error("Error: Failed to derive key from first letter. Please check your input."))
                            continue
                        
                        new_a, new_b = key_result
                        corrected_plaintext = decrypt(ciphertext, new_a, new_b)
                        
                        print("\n" + title("=== Corrected Decryption Result ==="))
                        print(key_value("Plaintext", corrected_plaintext))
                        print(key_value("Derived Key", f"a={new_a}, b={new_b}"))
                        
                        # 记录单词到词典
                        words = extract_candidate_words(corrected_plaintext, min_len=4)
                        added_words = append_extra_words(words)
                        if added_words:
                            print(success(f"Growth Mode: added {len(added_words)} new word(s) to data/extra_words.txt:"))
                            print(info(f"  {', '.join(added_words)}"))
                        else:
                            print(warning("Growth Mode: no new words to add."))
                    else:
                        print(warning("Growth Mode: correction cancelled, nothing added."))

        else:
            print(error("Invalid option. Please enter 0 / 1 / 2 / 3 / 4."))

if __name__ == "__main__":
    main()
