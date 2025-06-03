import fitz  # PyMuPDF
import json
import re
import os

# Each tuple: (PDF path, question offset, set label)
SET_FILES = [
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-A-Questions_v1.7.pdf", 0, "A"),
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-B-Questions_v1.7.pdf", 100, "B"),
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-C-Questions_v1.6.pdf", 200, "C"),
    ("Tests/ISTQB_CTFL_v4.0_Sample-Exam-D-Questions_v1.5.pdf", 300, "D"),
]

# Load the answer key from JSON
with open("answer_key_all.json", "r", encoding="utf-8") as f:
    answer_key = json.load(f)

def extract_text(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    doc = fitz.open(filepath)
    return "\n".join(page.get_text() for page in doc)

def extract_questions(question_text, question_offset=0, set_name="A"):
    q_blocks = re.split(r"Question #(\d{1,2}) \(\d+ Point\)", question_text)[1:]
    questions = []

    for i in range(0, len(q_blocks), 2):
        try:
            q_num = int(q_blocks[i].strip()) + question_offset
            block = q_blocks[i + 1].strip()

            # Extract question text before "a)"
            question_match = re.match(r"(.+?)\n\s*a\)", block, re.DOTALL)
            if not question_match:
                continue

            question_text = question_match.group(1).strip()
            # Extract options
            options = dict(re.findall(r"([a-d])\)\s(.+?)(?=\n[a-d]\)|\Z)", block, re.DOTALL))

            questions.append({
                "number": q_num,
                "question": question_text,
                "options": options,
                "answer": None,
                "section": None,
                "set": set_name
            })
        except Exception as e:
            print(f"⚠️ Failed to parse question block: {e}")

    return questions

def combine_questions_and_answers(questions, answers):
    for q in questions:
        q_num = str(q["number"])  # keys from JSON are strings
        if q_num in answers:
            q["answer"] = answers[q_num]["answer"]
            q["section"] = answers[q_num]["section"]
            q["set"] = answers[q_num]["set"]
        else:
            q["answer"] = "N/A"
            q["section"] = "N/A"
    return questions

def main():
    all_questions = []

    for path, offset, set_label in SET_FILES:
        print(f"📄 Processing Set {set_label}...")
        try:
            text = extract_text(path)
            raw_questions = extract_questions(text, offset, set_label)
            full_questions = combine_questions_and_answers(raw_questions, answer_key)
            all_questions.extend(full_questions)
            print(f"✅ Added {len(full_questions)} questions from Set {set_label}")
        except Exception as e:
            print(f"❌ Failed to process {set_label}: {e}")

    output_file = "questions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! All sets saved to {output_file} ({len(all_questions)} total questions)")

if __name__ == "__main__":
    main()
