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
        print("Affine Cipher 工具")
        print("0) 退出")
        print("1) 加密")
        print("2) 解密")
        print("3) 暴力破译")
        print("==============================")

        choice = input("请选择(0/1/2/3): ").strip()

        if choice == "0":
            print("已退出程序。")
            break

        elif choice == "1":
            plain = input("请输入要加密的文字: ")
            a, b = random_key()
            cipher = encrypt(plain, a, b)
            print("\n=== 加密结果 ===")
            print("密文:", cipher)
            print(f"密钥: a={a}, b={b}")

        elif choice == "2":
            cipher = input("请输入要解密的文字: ")
            a = _read_int("请输入密钥 a: ")
            b = _read_int("请输入密钥 b: ")

            if a is None or b is None:
                print("错误：a 和 b 必须是整数。")
                continue

            if not is_valid_a(a):
                print("错误：a 必须与 26 互素。")
                continue

            if not (0 <= b <= 25):
                print("错误：b 必须在 0~25。")
                continue

            plain = decrypt(cipher, a, b)
            print("\n=== 解密结果 ===")
            print("明文:", plain)

        elif choice == "3":
            cipher = input("请输入要破译的文字: ")
            k = _read_int("输出前 K 个候选(默认 5): ")
            if k is None or k <= 0:
                k = 5

            results = brute_force_topk(cipher, top_k=k)

            print("\n=== 暴力破译候选 ===")
            for idx, r in enumerate(results, 1):
                print(f"\n[{idx}] score={r['score']}   a={r['a']} b={r['b']}")
                print(r["plain"])

            print("\n提示：若破译不准，把新词加入 data/extra_words.txt。")

        else:
            print("无效选项，请输入 0 / 1 / 2 / 3。")

if __name__ == "__main__":
    main()
