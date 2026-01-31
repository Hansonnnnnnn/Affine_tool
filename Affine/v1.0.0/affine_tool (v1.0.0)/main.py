from affine import random_key, encrypt, decrypt, is_valid_a
from brute import brute_force_topk

def _read_int(prompt: str):
    s = input(prompt).strip()
    try:
        return int(s)
    except ValueError:
        return None

def main():
    while True:
        print("\n==============================")
        print("Affine Cipher Tool")
        print("0) Exit")
        print("1) Encrypt")
        print("2) Decrypt")
        print("3) Brute-force Crack (dictionary scoring)")
        print("==============================")

        choice = input("Choose (0/1/2/3): ").strip()

        if choice == "0":
            print("Exited.")
            break

        elif choice == "1":
            plaintext = input("Enter plaintext: ")
            a, b = random_key()
            ciphertext = encrypt(plaintext, a, b)
            print("\n=== Encryption Result ===")
            print("Ciphertext:", ciphertext)
            print(f"Key: a={a}, b={b}")

        elif choice == "2":
            ciphertext = input("Enter ciphertext: ")
            a = _read_int("Enter key a: ")
            b = _read_int("Enter key b: ")

            if a is None or b is None:
                print("Error: a and b must be integers.")
                continue

            if not is_valid_a(a):
                print("Error: a must be coprime with 26.")
                continue

            if not (0 <= b <= 25):
                print("Error: b must be in the range 0..25.")
                continue

            plaintext = decrypt(ciphertext, a, b)
            print("\n=== Decryption Result ===")
            print("Plaintext:", plaintext)

        elif choice == "3":
            ciphertext = input("Enter ciphertext to crack: ")
            k = _read_int("Show top K candidates (default 5): ")
            if k is None or k <= 0:
                k = 5

            results = brute_force_topk(ciphertext, top_k=k)

            print("\n=== Brute-force Candidates ===")
            for idx, r in enumerate(results, 1):
                print(f"\n[{idx}] score={r['score']}   a={r['a']} b={r['b']}")
                print(r["plain"])

            print("\nTip: If cracking fails, add new common words to data/extra_words.txt (one word per line).")

        else:
            print("Invalid option. Please enter 0 / 1 / 2 / 3.")

if __name__ == "__main__":
    main()
