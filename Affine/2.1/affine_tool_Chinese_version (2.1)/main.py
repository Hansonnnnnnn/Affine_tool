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
    return s in ("t", "true", "y", "yes", "1", "是", "对", "正确")

def main():
    growth_mode = False

    while True:
        print("\n" + separator())
        print(title("仿射密码工具（版本2.1）"))
        print("0) 退出")
        print("1) 加密")
        print("2) 解密")
        print("3) 暴力破解（词典评分）")
        growth_status = success("开启") if growth_mode else warning("关闭")
        print(f"4) 切换学习模式（当前：{growth_status}）")
        print(separator())

        choice = input("请选择 (0/1/2/3/4): ").strip()

        if choice == "0":
            print(info("已退出。"))
            break

        elif choice == "4":
            growth_mode = not growth_mode
            status = success("开启") if growth_mode else warning("关闭")
            print(f"学习模式现在是 {status}。")
            continue

        elif choice == "1":
            plaintext = input("请输入明文: ")
            a, b = random_key()
            ciphertext = encrypt(plaintext, a, b)
            print("\n" + title("=== 加密结果 ==="))
            print(key_value("密文", ciphertext))
            print(key_value("密钥", f"a={a}, b={b}"))

        elif choice == "2":
            ciphertext = input("请输入密文: ")
            a = _read_int("请输入密钥 a: ")
            b = _read_int("请输入密钥 b: ")

            if a is None or b is None:
                print(error("错误：a 和 b 必须是整数。"))
                continue

            if not is_valid_a(a):
                print(error("错误：a 必须与 26 互质。"))
                continue

            if not (0 <= b <= 25):
                print(error("错误：b 必须在 0..25 范围内。"))
                continue

            plaintext = decrypt(ciphertext, a, b)
            print("\n" + title("=== 解密结果 ==="))
            print(key_value("明文", plaintext))

            if growth_mode:
                ok = _read_tf("这个明文是否正确？(T/F): ")
                if ok:
                    words = extract_candidate_words(plaintext, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"学习模式：已将 {len(added_words)} 个新单词添加到 data/extra_words.txt:"))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("学习模式：没有新单词可添加。"))
                else:
                    # 用户说不正确，询问是否纠正
                    correct = _read_tf("您想要纠正它吗？(T/F): ")
                    if correct:
                        print(info("仿射密码只需要知道任意一个字母的位置就可以推导出密钥。"))
                        print(info("请输入明文的第一个字母："))
                        first_letter = input("第一个字母: ").strip()
                        
                        if not first_letter:
                            print(error("错误：第一个字母不能为空。"))
                            continue
                        
                        # 根据第一个字母反推密钥
                        key_result = derive_key_from_first_letter(ciphertext, first_letter)
                        if key_result is None:
                            print(error("错误：无法根据第一个字母推导密钥。请检查您的输入。"))
                            continue
                        
                        new_a, new_b = key_result
                        corrected_plaintext = decrypt(ciphertext, new_a, new_b)
                        
                        print("\n" + title("=== 纠正后的解密结果 ==="))
                        print(key_value("明文", corrected_plaintext))
                        print(key_value("推导出的密钥", f"a={new_a}, b={new_b}"))
                        
                        # 记录单词到词典
                        words = extract_candidate_words(corrected_plaintext, min_len=4)
                        added_words = append_extra_words(words)
                        if added_words:
                            print(success(f"学习模式：已将 {len(added_words)} 个新单词添加到 data/extra_words.txt:"))
                            print(info(f"  {', '.join(added_words)}"))
                        else:
                            print(warning("学习模式：没有新单词可添加。"))
                    else:
                        print(warning("学习模式：纠正已取消，未添加任何内容。"))

        elif choice == "3":
            ciphertext = input("请输入要破解的密文: ")
            k = _read_int("显示前 K 个候选结果（默认 5）: ")
            if k is None or k <= 0:
                k = 5

            results = brute_force_topk(ciphertext, top_k=k)

            print("\n" + title("=== 暴力破解候选结果 ==="))
            for idx, r in enumerate(results, 1):
                score_str = success(str(r['score'])) if r['score'] > 0 else warning(str(r['score']))
                print(f"\n{info(f'[{idx}]')} {colorize('得分', Colors.CYAN)}: {score_str}   {key_value('a', str(r['a']))} {key_value('b', str(r['b']))}")
                print(highlight(r["plain"]))

            if growth_mode and results:
                ok = _read_tf("第 1 个候选结果是否正确？(T/F): ")
                if ok:
                    top_plain = results[0]["plain"]
                    words = extract_candidate_words(top_plain, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"学习模式：已将 {len(added_words)} 个新单词添加到 data/extra_words.txt:"))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("学习模式：没有新单词可添加。"))
                else:
                    # 用户说不正确，询问是否纠正
                    correct = _read_tf("您想要纠正它吗？(T/F): ")
                    if correct:
                        print(info("仿射密码只需要知道任意一个字母的位置就可以推导出密钥。"))
                        print(info("请输入明文的第一个字母："))
                        first_letter = input("第一个字母: ").strip()
                        
                        if not first_letter:
                            print(error("错误：第一个字母不能为空。"))
                            continue
                        
                        # 根据第一个字母反推密钥
                        key_result = derive_key_from_first_letter(ciphertext, first_letter)
                        if key_result is None:
                            print(error("错误：无法根据第一个字母推导密钥。请检查您的输入。"))
                            continue
                        
                        new_a, new_b = key_result
                        corrected_plaintext = decrypt(ciphertext, new_a, new_b)
                        
                        print("\n" + title("=== 纠正后的解密结果 ==="))
                        print(key_value("明文", corrected_plaintext))
                        print(key_value("推导出的密钥", f"a={new_a}, b={new_b}"))
                        
                        # 记录单词到词典
                        words = extract_candidate_words(corrected_plaintext, min_len=4)
                        added_words = append_extra_words(words)
                        if added_words:
                            print(success(f"学习模式：已将 {len(added_words)} 个新单词添加到 data/extra_words.txt:"))
                            print(info(f"  {', '.join(added_words)}"))
                        else:
                            print(warning("学习模式：没有新单词可添加。"))
                    else:
                        print(warning("学习模式：纠正已取消，未添加任何内容。"))

        else:
            print(error("无效选项。请输入 0 / 1 / 2 / 3 / 4。"))

if __name__ == "__main__":
    main()
