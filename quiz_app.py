import streamlit as st
import json
import random

# Load question data from questions.json
@st.cache_data
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize session state on first load
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
    st.session_state.questions = []
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.show_results = False

def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.questions = []
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.show_results = False

def start_quiz():
    all_qs = load_questions()
    set_choice = st.session_state.set_choice
    count = st.session_state.num_questions

    if set_choice != "ALL":
        all_qs = [q for q in all_qs if q["set"] == set_choice]

    selected = random.sample(all_qs, min(count, len(all_qs)))
    st.session_state.questions = selected
    st.session_state.quiz_started = True

# Sidebar setup
with st.sidebar:
    st.title("🧠 ITQSB Quiz Setup")
    st.session_state.set_choice = st.selectbox("Select Set", ["ALL", "A", "B", "C", "D"])
    st.session_state.num_questions = st.number_input("How many questions?", 1, 40, 5)
    if st.button("Start Quiz"):
        start_quiz()

st.title("📘 ITQSB Foundation Practice Quiz")

# Quiz Flow
if st.session_state.quiz_started and not st.session_state.show_results:
    q_idx = st.session_state.current
    if q_idx < len(st.session_state.questions):
        q = st.session_state.questions[q_idx]

        st.markdown(f"### Q{q_idx + 1}: (Set {q['set']} — #{q['number']} — Section {q['section']})")
        st.markdown(q["question"])

        # Detect multi-answer format
        is_multi = "," in q["answer"]
        options = q["options"]
        letter_list = list(options.keys())
        choices = [f"{k}) {v}" for k, v in options.items()]

        if is_multi:
            st.warning("🔁 This question has more than one correct answer.")
            selected = st.multiselect("Select one or more:", choices, key=f"multi_{q_idx}")
            submit_label = "Submit Multiple Answers"
        else:
            selected = st.radio("Choose your answer:", choices, key=f"single_{q_idx}")
            selected = [selected]  # Normalize as list
            submit_label = "Submit Answer"

        if st.button(submit_label, key=f"submit_{q_idx}"):
            user_letters = [s[0] for s in selected]
            correct_set = set(q["answer"].replace(" ", "").split(","))
            user_set = set(user_letters)

            if user_set == correct_set:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {q['answer']}")
                st.session_state.answers.append({
                    "number": q['number'],
                    "question": q['question'],
                    "your_answer": ", ".join(user_letters),
                    "correct_answer": q['answer'],
                    "options": q['options'],
                    "section": q['section'],
                    "set": q['set']
                })

            st.session_state.current += 1
            st.rerun()
    else:
        st.session_state.show_results = True
        st.rerun()

# Final Score and Review
if st.session_state.show_results:
    total = len(st.session_state.questions)
    score = st.session_state.score
    st.success(f"🎉 Quiz complete! You scored {score}/{total} ({(score/total)*100:.1f}%)")

    if st.session_state.answers:
        st.write("### ❌ Review Missed Questions")
        for wa in st.session_state.answers:
            st.markdown(f"**Q{wa['number']} (Set {wa['set']}, Section {wa['section']})**")
            st.markdown(wa["question"])
            for k, v in wa["options"].items():
                st.markdown(f"- **{k})** {v}")
            st.markdown(f"❌ Your answer: `{wa['your_answer']}`")
            st.markdown(f"✅ Correct answer: `{wa['correct_answer']}`")
            st.markdown("---")

    if st.button("🔁 Restart Quiz"):
        reset_quiz()
        st.rerun()
