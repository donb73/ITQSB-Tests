import json
import random
from datetime import datetime

def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_user_filter(questions):
    set_choice = input("📘 Choose set [A/B/C/D/ALL]: ").strip().upper()
    if set_choice in {"A", "B", "C", "D"}:
        questions = [q for q in questions if q["set"] == set_choice]
    elif set_choice != "ALL":
        print("⚠️ Invalid choice. Using all sets.")
    return questions

def get_question_limit(questions):
    limit = input(f"🎯 How many questions? (1–{len(questions)} or Enter for all): ").strip()
    if limit.isdigit():
        n = int(limit)
        if 1 <= n <= len(questions):
            return random.sample(questions, n)
        else:
            print("⚠️ Invalid number. Using full set.")
    return questions

def run_quiz():
    questions = load_questions()
    questions = get_user_filter(questions)
    questions = get_question_limit(questions)

    score = 0
    wrong_answers = []

    print(f"\n🧪 Starting quiz with {len(questions)} questions...\n")

    for idx, q in enumerate(questions, 1):
        print(f"Q{idx}: (Set {q['set']} — #{q['number']} — Section {q['section']})")
        print(q["question"])
        for letter, text in q["options"].items():
            print(f"  {letter}) {text}")

        user_answer = input("Your answer: ").strip().lower()

        correct = q["answer"]
        correct_set = set(map(str.strip, correct.split(",")))
        user_set = set(map(str.strip, user_answer.split(",")))

        if user_set == correct_set:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {correct}\n")
            wrong_answers.append({
                "number": q['number'],
                "question": q['question'],
                "your_answer": user_answer,
                "correct_answer": correct,
                "options": q['options'],
                "section": q.get("section", "N/A"),
                "set": q.get("set", "N/A")
            })

    print(f"📝 Quiz complete! Score: {score}/{len(questions)}")

    if wrong_answers:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wrong_answers_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(wrong_answers, f, indent=2, ensure_ascii=False)
        print(f"❌ {len(wrong_answers)} wrong answers saved to {filename}")
    else:
        print("🎉 Perfect score! No wrong answers to save.")

if __name__ == "__main__":
    run_quiz()