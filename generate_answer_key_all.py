import fitz
import re
import json
import os

# Each tuple: (PDF path, offset, set label)
SET_FILES = [
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-A-Answers_v1.7.pdf", 0, "A"),
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-B-Answers_v1.7.pdf", 100, "B"),
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-C-Answers_v1.6.pdf", 200, "C"),
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-D-Answers_v1.5.pdf", 300, "D"),
]

def extract_text(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    doc = fitz.open(filepath)
    return "\n".join(page.get_text() for page in doc)

def extract_answer_data(text, offset, set_label):
    pattern = re.compile(r"(\d{1,2})\s+([a-d](?:,\s*[a-e])?)\s+FL-([\d.]+)", re.IGNORECASE)
    answers = {}

    for match in pattern.finditer(text):
        q_raw = int(match.group(1))
        answer = match.group(2).replace(" ", "").lower()
        section = match.group(3).strip()

        q_number = q_raw + offset
        answers[q_number] = {
            "answer": answer,
            "section": section,
            "set": set_label
        }

    return answers

def main():
    all_answers = {}

    for path, offset, set_label in SET_FILES:
        print(f"📄 Extracting Set {set_label} from: {path}")
        try:
            text = extract_text(path)
            answers = extract_answer_data(text, offset, set_label)
            print(f"✅ Found {len(answers)} entries for Set {set_label}")
            all_answers.update(answers)
        except Exception as e:
            print(f"❌ Failed to extract from {path}: {e}")

    # Save to JSON
    with open("answer_key_all.json", "w", encoding="utf-8") as f:
        json.dump(all_answers, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! Saved full answer key to answer_key_all.json ({len(all_answers)} total questions)")

if __name__ == "__main__":
    main()
