import pdfplumber
import json
import os

# Files and offsets
SET_FILES = [
    ("ISTQB_CTFL_v4.0_Sample-Exam-A-Answers_v1.7.pdf", 0, "A"),
    ("ISTQB_CTFL_v4.0_Sample-Exam-B-Answers_v1.7.pdf", 100, "B"),
    ("ISTQB_CTFL_v4.0_Sample-Exam-C-Answers_v1.6.pdf", 200, "C"),
    ("ISTQB_CTFL_v4.0_Sample-Exam-D-Answers_v1.5.pdf", 300, "D"),
]

base_dir = "Tests"  # path to folder with your PDFs

def extract_from_table(pdf_path, offset, set_label):
    answers = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or not row[0]:
                        continue
                    try:
                        qnum_raw = int(row[0].strip())
                        answer = row[1].strip().lower().replace(" ", "")
                        section = row[3].strip().replace("FL-", "")
                        qnum = str(qnum_raw + offset)
                        answers[qnum] = {
                            "answer": answer,
                            "section": section,
                            "set": set_label
                        }
                    except (ValueError, IndexError):
                        continue
    return answers

def main():
    all_answers = {}

    for filename, offset, set_label in SET_FILES:
        full_path = os.path.join(base_dir, filename)
        if not os.path.exists(full_path):
            print(f"❌ Missing file: {full_path}")
            continue

        print(f"📄 Extracting from {filename} (Set {set_label})...")
        try:
            extracted = extract_from_table(full_path, offset, set_label)
            print(f"✅ Found {len(extracted)} answers in Set {set_label}")
            all_answers.update(extracted)
        except Exception as e:
            print(f"❌ Failed to extract from {filename}: {e}")

    with open("answer_key_all.json", "w", encoding="utf-8") as f:
        json.dump(all_answers, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 All done! {len(all_answers)} answers saved to answer_key_all.json")

if __name__ == "__main__":
    main()
