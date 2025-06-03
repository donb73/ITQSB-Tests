import streamlit as st
import json
import random

# Load question data
@st.cache_data
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# Sidebar: Filters
st.sidebar.title("🧠 Quiz Setup")
set_choice = st.sidebar.selectbox("Choose Set", ["ALL", "A", "B", "C", "D"])
question_count = st.sidebar.number_input("Number of Questions", min_value=1, max_value=40, value=10)

# Apply filters
if set_choice != "ALL":
    questions = [q for q in questions if q["set"] == set_choice]

questions = random.sample(questions, min(question_count, len(questions)))

st.title("📘 ISTQB CTFL Practice Quiz")
st.write(f"Total Questions: **{len(questions)}**")

score = 0
wrong_answers = []

# Quiz loop
for idx, q in enumerate(questions, 1):
    st.markdown(f"### Q{idx}: ({q['set']} #{q['number']}) - Section {q['section']}")
    st.markdown(q["question"])
    answer = st.radio("Choose your answer:", list(q["options"].keys()), key=f"q{idx}")
    submitted = st.button("Submit", key=f"submit{idx}")

    if submitted:
        correct = set(q["answer"].replace(" ", "").split(","))
        user = set(answer.replace(" ", "").split(","))
        if user == correct:
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Incorrect. Correct answer: {q['answer']}")
            wrong_answers.append(q)

        st.markdown("---")

# Show final score
if st.button("Show Results"):
    st.success(f"Your score: {score}/{len(questions)}")
    if wrong_answers:
        st.write("### ❌ Questions You Missed:")
        for wq in wrong_answers:
            st.markdown(f"**{wq['number']} (Set {wq['set']}, Section {wq['section']}):** Correct = {wq['answer']}")

