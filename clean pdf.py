import pdfplumber

def extract_clean_text(filepath):
    full_text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    return full_text

answer_text = extract_clean_text("Tests/ISTQB_CTFL_v4.0_Sample-Exam-A-Answers_v1.7.pdf")
print(answer_text[:1000])