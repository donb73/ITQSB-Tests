import fitz  # PyMuPDF
import json
import re
from answer_key_map import answer_key  # <- your hardcoded map

questions_pdf = "Tests/ISTQB_CTFL_v4.0_Sample-Exam-A-Questions_v1.7.pdf"
output_file = "questions.json"

def extract_text(filepath):
    doc = fitz.open(filepath)
    return "\n".join(page.get_text() for page in doc)

def extract_questions(question_text):
    # Split each block by "Question #X"
    q_blocks = re.split(r"Question #(\d{1,2}) \(\d+ Point\)", question_text)[1:]
    questions = []

    for i in range(0, len(q_blocks), 2):
        try:
            q_num = int(q_blocks[i].strip())
            block = q_blocks[i + 1].strip()

            # Extract question text (before option a)
            question_match = re.match(r"(.+?)\n\s*a\)", block, re.DOTALL)
            if not question_match:
                continue
            question_text = question_match.group(1).strip()

            # Extract options: a), b), c), d)
            options = dict(re.findall(r"([a-d])\)\s(.+?)(?=\n[a-d]\)|\Z)", block, re.DOTALL))

            questions.append({
                "number": q_num,
                "question": question_text,
                "options": options,
                "answer": None,   # will be filled in later
                "section": None   # will be filled in later
            })

        except Exception as e:
            print(f"⚠️ Failed to parse question #{i//2 + 1}: {e}")

    return questions

def combine_questions_and_answers(questions, answers):
    for q in questions:
        q_num = q["number"]
        if q_num in answers:
            q["answer"] = answers[q_num]["answer"]
            q["section"] = answers[q_num]["section"]
        else:
            q["answer"] = "N/A"
            q["section"] = "N/A"
    return questions

def main():
    print("📄 Reading questions PDF...")
    question_text = extract_text(questions_pdf)
    print("✅ Extracted raw text.")

    print("📊 Extracting questions...")
    questions = extract_questions(question_text)
    print(f"✅ Found {len(questions)} questions.")

    print("🔗 Merging with answer key...")
    full_data = combine_questions_and_answers(questions, answer_key)

    print(f"💾 Writing to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2, ensure_ascii=False)

    print("✅ Done! questions.json is ready to use.")

if __name__ == "__main__":
    main()