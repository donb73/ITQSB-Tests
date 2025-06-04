import pdfplumber
import re
import json
import os

# Load the full answer key
with open("answer_key_all.json", "r", encoding="utf-8") as f:
    answer_key = json.load(f)

# Define all test sets
SET_FILES = [
    ("ISTQB_CTFL_v4.0_Sample-Exam-A-Questions_v1.7.pdf", 0, "A"),
    ("ISTQB_CTFL_v4.0_Sample-Exam-B-Questions_v1.7.pdf", 100, "B"),
    ("ISTQB_CTFL_v4.0_Sample-Exam-C-Questions_v1.6.pdf", 200, "C"),
    ("ISTQB_CTFL_v4.0_Sample-Exam-D-Questions_v1.5.pdf", 300, "D"),
]

base_dir = "Tests"
all_questions = []

def clean_option_text(text):
    text = text.strip().replace("\n", " ")
    for footer in ["Certified Tester", "Sample Exams", "Version", "Page", "Release", "©"]:
        if footer in text:
            text = text.split(footer)[0].strip()
    return text

def parse_question_blocks(lines):
    blocks = []
    current = []

    for line in lines:
        if re.match(r"^\s*\d{1,2}[\.\)]\s*", line): # e.g., "1. Question text..."
            if current:
                blocks.append(current)
                current = []
        current.append(line.strip())

    if current:
        blocks.append(current)

    return blocks

def extract_questions_from_pdf(pdf_path, offset, set_label):
    import pdfplumber
    import re
    import os

    questions = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )

    # ✅ Match only numeric questions like "Question #1 (1 Point)"
    pattern = re.compile(
        r"Question\s+#([0-9]{1,2})\s+\(\d+ Point\)\s*(.*?)(?=\nQuestion\s+#(?:[0-9]{1,2})\s+\(\d+ Point\)|\Z)",
        re.DOTALL,
    )

    matches = pattern.findall(full_text)
    print(f"🧪 Found {len(matches)} raw blocks in {os.path.basename(pdf_path)}")

    for number_str, block in matches:
        if not number_str.isdigit():
            continue  # ❌ Skip optional questions like A1, A26, etc.

        q_number = int(number_str) + offset
        q_key = str(q_number)

        # Extract question text
        parts = re.split(r"\n[a-e]\)", block, maxsplit=1)
        question_text = parts[0].strip().replace("\n", " ")

        # Extract answer options
        options = {}
        matches_opt = list(
            re.finditer(r"([a-e])\)\s((?:.|\n)+?)(?=\n[a-e]\)|\Z)", block)
        )

        if len(matches_opt) < 2:
            continue  # ❌ Skip malformed or duplicate blocks

        for match in matches_opt:
            key = match.group(1)
            val = match.group(2).strip().replace("\n", " ")
            for footer in ["Certified Tester", "Sample Exams", "Version", "Page", "Release", "©"]:
                if footer in val:
                    val = val.split(footer)[0].strip()
            options[key] = val

        # Pull answer metadata
        if q_key in answer_key:
            answer = answer_key[q_key]["answer"]
            section = answer_key[q_key]["section"]
            set_val = answer_key[q_key]["set"]
        else:
            answer = "N/A"
            section = "N/A"
            set_val = set_label

        questions.append({
            "number": q_number,
            "question": question_text,
            "options": options,
            "answer": answer,
            "section": section,
            "set": set_val
        })

    return questions

def main():
    for filename, offset, set_label in SET_FILES:
        full_path = os.path.join(base_dir, filename)
        if not os.path.exists(full_path):
            print(f"❌ Missing file: {full_path}")
            continue

        print(f"📄 Processing {filename} (Set {set_label})...")
        extracted = extract_questions_from_pdf(full_path, offset, set_label)
        print(f"✅ Found {len(extracted)} questions from Set {set_label}")
        all_questions.extend(extracted)

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 All done! Wrote {len(all_questions)} questions to questions.json")

if __name__ == "__main__":
    main()
