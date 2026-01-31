import sys
import io

# 设置 Windows 控制台编码为 UTF-8，解决中文显示问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

from affine import random_key, encrypt, decrypt, is_valid_a
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
        print(title("Affine Cipher 工具"))
        print("0) 退出")
        print("1) 加密")
        print("2) 解密")
        print("3) 暴力破译（字典打分）")
        growth_status = success("开启") if growth_mode else warning("关闭")
        print(f"4) 切换成长模式（当前：{growth_status}）")
        print(separator())

        choice = input("请选择（0/1/2/3/4）：").strip()

        if choice == "0":
            print(info("已退出。"))
            break

        elif choice == "4":
            growth_mode = not growth_mode
            status = success("开启") if growth_mode else warning("关闭")
            print(f"成长模式已切换为：{status}")
            continue

        elif choice == "1":
            plaintext = input("请输入要加密的明文：")
            a, b = random_key()
            ciphertext = encrypt(plaintext, a, b)

            print("\n" + title("=== 加密结果 ==="))
            print(key_value("密文", ciphertext))
            print(key_value("密钥", f"a={a}, b={b}"))

        elif choice == "2":
            ciphertext = input("请输入要解密的密文：")
            a = _read_int("请输入密钥 a：")
            b = _read_int("请输入密钥 b：")

            if a is None or b is None:
                print(error("错误：a 和 b 必须是整数。"))
                continue

            if not is_valid_a(a):
                print(error("错误：a 必须与 26 互素。"))
                continue

            if not (0 <= b <= 25):
                print(error("错误：b 必须在 0~25 之间。"))
                continue

            plaintext = decrypt(ciphertext, a, b)

            print("\n" + title("=== 解密结果 ==="))
            print(key_value("明文", plaintext))

            if growth_mode:
                ok = _read_tf("成长模式：该明文是否正确？(T/F)：")
                if ok:
                    words = extract_candidate_words(plaintext, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"成长模式：已新增 {len(added_words)} 个词到 data/extra_words.txt："))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("成长模式：没有需要新增的词。"))

        elif choice == "3":
            ciphertext = input("请输入要破译的密文：")
            k = _read_int("输出前 K 个候选（默认 5）：")
            if k is None or k <= 0:
                k = 5

            results = brute_force_topk(ciphertext, top_k=k)

            print("\n" + title("=== 暴力破译候选 ==="))
            for idx, r in enumerate(results, 1):
                score_str = success(str(r["score"])) if r["score"] > 0 else warning(str(r["score"]))
                print(
                    f"\n{info(f'[{idx}]')} "
                    f"{colorize('score', Colors.CYAN)}: {score_str}   "
                    f"{key_value('a', str(r['a']))} {key_value('b', str(r['b']))}"
                )
                print(highlight(r["plain"]))

            if growth_mode and results:
                ok = _read_tf("成长模式：第 1 名候选是否正确？(T/F)：")
                if ok:
                    top_plain = results[0]["plain"]
                    words = extract_candidate_words(top_plain, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"成长模式：已新增 {len(added_words)} 个词到 data/extra_words.txt："))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("成长模式：没有需要新增的词。"))
                else:
                    print(warning("成长模式：本次未新增任何词。"))

        else:
            print(error("无效选项：请输入 0 / 1 / 2 / 3 / 4。"))

if __name__ == "__main__":
    main()
