"""
Mishkal Diacritization Tester
------------------------------
1. Install: pip install mishkal
2. Paste your Arabic paragraph into the TEXT variable below.
3. Run: python test_mishkal.py

Outputs:
- The full vocalized paragraph
- A word-by-word breakdown (original -> vocalized)
"""

import sys
import io

# Force UTF-8 output so Arabic characters print correctly on Windows
# (Windows console defaults to cp1252, which can't handle Arabic)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from mishkal import tashkeel

vocalizer = tashkeel.TashkeelClass()

# ------------------------------------------------------
# PASTE YOUR ARABIC TEXT HERE (can be multiple sentences)
# ------------------------------------------------------
TEXT = """
ذهب الرجل المصري الى وزارة التربية وقابل مدير المدرسة الذي كان جالسا امام مكتبه
وقال له انه يريد ان يسجل ابنه في المدرسة هذا العام لان اولئك الطلاب الذين درسوا هناك
نجحوا في الامتحانات وحصلوا على مائة درجة كاملة وكان الاستاذ سعيدا بذلك النجاح الكبير
"""
# ------------------------------------------------------


def main():
    text = TEXT.strip()
    if not text:
        print("Please paste some Arabic text into the TEXT variable.")
        return

    print("=" * 60)
    print("ORIGINAL TEXT:")
    print(text)
    print("=" * 60)

    # Full paragraph vocalization
    try:
        full_result = vocalizer.tashkeel(text)
        print("FULL VOCALIZED OUTPUT:")
        print(full_result)
    except Exception as e:
        print(f"ERROR vocalizing full text: {e}")
        full_result = None
    print("=" * 60)

    # Word-by-word breakdown (helps spot exactly which word
    # got mishandled, e.g. garbled or missing elongation)
    print("WORD-BY-WORD BREAKDOWN:")
    words = text.split()
    for w in words:
        try:
            vocalized_word = vocalizer.tashkeel(w)
            print(f"  {w:15s} -> {vocalized_word}")
        except Exception as e:
            print(f"  {w:15s} -> ERROR: {e}")
    print("=" * 60)


if __name__ == "__main__":
    main()