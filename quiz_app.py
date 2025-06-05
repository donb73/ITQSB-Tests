import streamlit as st
import json
import random

# ====================
# ⚙️ Load Questions
# ====================

@st.cache_data
def load_questions():
    with open("questions.json", encoding="utf-8") as f:
        all_questions = json.load(f)

    order_mode = st.session_state.get("order_mode", "Random")
    selected_set = st.session_state.get("set_choice", "ALL")

    sets = ["A", "B", "C", "D"] if selected_set == "ALL" else [selected_set]
    questions = []

    for s in sets:
        set_questions = [q for q in all_questions if q["set"] == s]
        if order_mode == "Random":
            random.shuffle(set_questions)
        else:
            set_questions.sort(key=lambda q: q["number"])
        questions.extend(set_questions)

    return questions


# ====================
# 🎛 Sidebar UI
# ====================

with st.sidebar:
    st.title("🧠 ITQSB Quiz Setup")

    st.session_state.set_choice = st.selectbox("Select Set", ["ALL", "A", "B", "C", "D"])
    st.session_state.num_questions = st.number_input("How many questions?", 1, 40, 5)
    st.session_state.order_mode = st.radio(
        "Question Order", ["Random", "Ordered"], index=0
    )

    if st.button("Start Quiz"):
        st.session_state.questions = load_questions()[:st.session_state.num_questions]
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.completed = False
        st.session_state.feedback_shown = False
        st.rerun()


# ====================
# 🧠 Quiz Logic
# ====================

if "questions" in st.session_state and not st.session_state.get("completed", False):
    questions = st.session_state.questions
    idx = st.session_state.current_q
    q = questions[idx]

    st.markdown("## 📝 Your Quiz")
    st.markdown(f"### Q{q['number']} ({q['set']}) — Section {q['section']}")
    st.write(q["question"])

    options = list(q["options"].keys())
    answer_key = f"answer_{idx}"

    if answer_key not in st.session_state:
        st.session_state[answer_key] = []

    selected = st.multiselect(
        "Select your answer(s):",
        options=options,
        format_func=lambda k: f"{k}) {q['options'][k]}",
        key=f"select_{idx}"
    )

    # Submit button
    if st.button("Submit Answer"):
        correct = [a.strip().lower() for a in q["answer"].split(",")]
        if sorted(selected) == sorted(correct):
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect. Correct answer: {', '.join(correct).upper()}")

        st.session_state[answer_key] = selected
        st.session_state.feedback_shown = True

    if st.session_state.feedback_shown:
        if idx + 1 < len(questions):
            if st.button("Next Question"):
                st.session_state.current_q += 1
                st.session_state.feedback_shown = False
                st.rerun()
        else:
            if st.button("Finish Quiz"):
                st.session_state.completed = True
                st.rerun()

# ====================
# 🏁 Quiz Finished
# ====================

elif st.session_state.get("completed", False):
    st.success(f"🎯 Quiz complete! You scored {st.session_state.score} out of {len(st.session_state.questions)}.")
    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
