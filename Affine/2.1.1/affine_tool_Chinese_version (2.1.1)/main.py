from affine import random_key, encrypt, decrypt, is_valid_a, derive_key_from_first_letter
from brute import brute_force_topk
from wordlist import extract_candidate_words, append_extra_words
from colors import title, success, error, warning, info, highlight, key_value, separator, colorize, Colors
import re

_WORD_RE = re.compile(r"[A-Za-z]+")

def _read_int(prompt: str):
    s = input(prompt).strip()
    try:
        return int(s)
    except ValueError:
        return None

def _read_tf(prompt: str):
    s = input(prompt).strip().lower()
    return s in ("t", "true", "y", "yes", "1", "是", "对", "正确")

def _extract_first_word(text: str) -> str:
    """提取文本中的第一个单词（忽略前导标点和空格）"""
    words = _WORD_RE.findall(text)
    return words[0].lower() if words else ""

def _rerank_by_first_word(candidates: list[dict], first_word: str) -> list[dict]:
    """根据第一个单词重新排序候选结果，给匹配的候选添加大额加分"""
    BONUS_SCORE = 1000  # 大额加分，确保匹配的候选排在前面
    
    reranked = []
    for candidate in candidates:
        original_score = candidate["score"]
        candidate_first_word = _extract_first_word(candidate["plain"])
        new_score = original_score
        has_bonus = False
        if candidate_first_word == first_word.lower():
            new_score += BONUS_SCORE
            has_bonus = True
        reranked.append({
            "score": new_score,
            "original_score": original_score,
            "has_bonus": has_bonus,
            "a": candidate["a"],
            "b": candidate["b"],
            "plain": candidate["plain"]
        })
    
    reranked.sort(key=lambda x: x["score"], reverse=True)
    return reranked

def main():
    growth_mode = False

    while True:
        print("\n" + separator())
        print(title("仿射密码工具 (v2.1.1)"))
        print("0) 退出")
        print("1) 加密")
        print("2) 解密")
        print("3) 暴力破解（词典评分）")
        growth_status = success("开启") if growth_mode else warning("关闭")
        print(f"4) 切换成长模式（当前：{growth_status}）")
        print(separator())

        choice = input("请选择 (0/1/2/3/4): ").strip()

        if choice == "0":
            print(info("已退出。"))
            break

        elif choice == "4":
            growth_mode = not growth_mode
            status = success("开启") if growth_mode else warning("关闭")
            print(f"成长模式现在是 {status}。")
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
                        print(success(f"成长模式：已向 data/extra_words.txt 添加 {len(added_words)} 个新单词："))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("成长模式：没有新单词可添加。"))
                else:
                    # 用户说不正确，询问是否纠正
                    correct = _read_tf("您想要纠正它吗？(T/F): ")
                    if correct:
                        print(info("仿射密码只需要知道任意一个字母的位置即可推导出密钥。"))
                        print(info("请输入明文的第一个字母："))
                        first_letter = input("第一个字母: ").strip()
                        
                        if not first_letter:
                            print(error("错误：第一个字母不能为空。"))
                            continue
                        
                        # 根据第一个字母反推密钥
                        key_result = derive_key_from_first_letter(ciphertext, first_letter)
                        if key_result is None:
                            print(error("错误：无法从第一个字母推导密钥。请检查您的输入。"))
                            continue
                        
                        new_a, new_b = key_result
                        corrected_plaintext = decrypt(ciphertext, new_a, new_b)
                        
                        print("\n" + title("=== 纠正后的解密结果 ==="))
                        print(key_value("明文", corrected_plaintext))
                        print(key_value("推导的密钥", f"a={new_a}, b={new_b}"))
                        
                        # 记录单词到词典
                        words = extract_candidate_words(corrected_plaintext, min_len=4)
                        added_words = append_extra_words(words)
                        if added_words:
                            print(success(f"成长模式：已向 data/extra_words.txt 添加 {len(added_words)} 个新单词："))
                            print(info(f"  {', '.join(added_words)}"))
                        else:
                            print(warning("成长模式：没有新单词可添加。"))
                    else:
                        print(warning("成长模式：纠正已取消，未添加任何内容。"))

        elif choice == "3":
            ciphertext = input("请输入要破解的密文: ")
            
            # 获取所有候选结果（312个：12个a值 * 26个b值）以便重新排序
            all_candidates = brute_force_topk(ciphertext, top_k=312)
            # 显示前5个
            results = all_candidates[:5]

            print("\n" + title("=== 暴力破解候选结果 ==="))
            for idx, r in enumerate(results, 1):
                score_str = success(str(r['score'])) if r['score'] > 0 else warning(str(r['score']))
                print(f"\n{info(f'[{idx}]')} {colorize('分数', Colors.CYAN)}: {score_str}   {key_value('a', str(r['a']))} {key_value('b', str(r['b']))}")
                print(highlight(r["plain"]))

            if growth_mode and results:
                ok = _read_tf("第 1 个候选结果是否正确？(T/F): ")
                if ok:
                    top_plain = results[0]["plain"]
                    words = extract_candidate_words(top_plain, min_len=4)
                    added_words = append_extra_words(words)
                    if added_words:
                        print(success(f"成长模式：已向 data/extra_words.txt 添加 {len(added_words)} 个新单词："))
                        print(info(f"  {', '.join(added_words)}"))
                    else:
                        print(warning("成长模式：没有新单词可添加。"))
                else:
                    # 用户说不正确，询问第一个单词
                    first_word = input("请输入明文的正确第一个单词: ").strip()
                    
                    if not first_word:
                        print(error("错误：第一个单词不能为空。"))
                        continue
                    
                    # 移除可能的空格，只保留第一个单词
                    first_word = first_word.split()[0].lower()
                    
                    # 根据第一个单词重新排序所有候选
                    reranked = _rerank_by_first_word(all_candidates, first_word)
                    results = reranked[:5]
                    
                    # 显示重新排序后的前5个
                    print("\n" + title("=== 重新排序后的候选结果 ==="))
                    for idx, r in enumerate(results, 1):
                        original_score = r.get('original_score', r['score'])
                        score_str = success(str(original_score)) if original_score > 0 else warning(str(original_score))
                        if r.get('has_bonus', False):
                            score_str += success(" (+1000 加分)")
                        print(f"\n{info(f'[{idx}]')} {colorize('分数', Colors.CYAN)}: {score_str}   {key_value('a', str(r['a']))} {key_value('b', str(r['b']))}")
                        print(highlight(r["plain"]))
                    
                    # 再次询问是否正确
                    ok2 = _read_tf("现在第 1 个候选结果是否正确？(T/F): ")
                    if ok2:
                        top_plain = results[0]["plain"]
                        words = extract_candidate_words(top_plain, min_len=4)
                        added_words = append_extra_words(words)
                        if added_words:
                            print(success(f"成长模式：已向 data/extra_words.txt 添加 {len(added_words)} 个新单词："))
                            print(info(f"  {', '.join(added_words)}"))
                        else:
                            print(warning("成长模式：没有新单词可添加。"))
                    else:
                        print(warning("成长模式：请手动将相关单词添加到 data/extra_words.txt 以提高未来的准确性。"))

        else:
            print(error("无效选项。请输入 0 / 1 / 2 / 3 / 4。"))

if __name__ == "__main__":
    main()
