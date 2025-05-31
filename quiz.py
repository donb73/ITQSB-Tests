import json
import random
import datetime

def load_questions(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def run_quiz(questions):
    score = 0
    wrong_answers = []
    random.shuffle(questions)

    for q in questions:
        print(f"\nQ{q['number']}: {q['question']}")
        for key, value in q['options'].items():
            print(f"  {key}. {value}")
        user_answer = input("Your answer (a/b/c/d): ").strip().lower()

        correct = q['answer']
        if user_answer == correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect. Correct answer: {correct}")
            wrong_answers.append({
                "number": q['number'],
                "question": q['question'],
                "your_answer": user_answer,
                "correct_answer": correct,
                "options": q['options']
            })

    print(f"\n🎯 Final Score: {score}/{len(questions)}")
    save_wrong_answers(wrong_answers)

def save_wrong_answers(wrong_answers):
    if wrong_answers:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wrong_answers_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(wrong_answers, f, indent=2, ensure_ascii=False)
        print(f"❗ {len(wrong_answers)} wrong answers saved to {filename}")
    else:
        print("🎉 You got everything right!")

if __name__ == "__main__":
    questions = load_questions("questions.json")
    run_quiz(questions)