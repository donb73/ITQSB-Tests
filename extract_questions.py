import fitz  # PyMuPDF
import json
import re
import os

questions_pdf = "Tests/ISTQB_CTFL_v4.0_Sample-Exam-A-Questions_v1.7.pdf"
answers_pdf = "Tests/ISTQB_CTFL_v4.0_Sample-Exam-A-Answers_v1.7.pdf"

def extract_text(filepath):
    doc = fitz.open(filepath)
    return "\n".join(page.get_text() for page in doc)

def extract_answers(answer_text):
    answer_map = {}
    pattern = re.compile(r"(\d{1,2})\s+([a-d](?:, [a-e])?)")  # handles cases like "6 a, e"
    for match in pattern.finditer(answer_text):
        q_num = int(match.group(1))
        correct = match.group(2).split(", ")
        answer_map[q_num] = correct if len(correct) > 1 else correct[0]
    return answer_map

def extract_questions(question_text):
    # Very basic parser: matches Question #X and captures 4 options
    q_blocks = re.split(r"Question #(\d{1,2}) \(\d+ Point\)", question_text)[1:]
    questions = []

    for i in range(0, len(q_blocks), 2):
        q_num = int(q_blocks[i].strip())
        block = q_blocks[i+1].strip()

        question_match = re.match(r"(.+?)\n\s*a\)", block, re.DOTALL)
        if not question_match:
            continue
        question_text = question_match.group(1).strip()

        options = dict(re.findall(r"([a-d])\)\s(.+?)(?=\n[a-d]\)|$)", block, re.DOTALL))
        questions.append({
            "number": q_num,
            "question": question_text,
            "options": options,
            "answer": None  # we'll fill this in next
        })

    return questions

def combine_questions_and_answers(questions, answers):
    for q in questions:
        q_num = q["number"]
        if q_num in answers:
            q["answer"] = answers[q_num]
    return questions

def main():
    q_text = extract_text(questions_pdf)
    a_text = extract_text(answers_pdf)

    raw_questions = extract_questions(q_text)
    answer_map = extract_answers(a_text)

    combined = combine_questions_and_answers(raw_questions, answer_map)

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"✅ Extracted {len(combined)} questions to questions.json")

if __name__ == "__main__":
    main()