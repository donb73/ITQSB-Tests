import json
import glob
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def find_latest_wrong_answers_file():
    files = glob.glob("wrong_answers_*.json")
    if not files:
        print("❌ No wrong_answers_*.json files found.")
        return None
    return max(files, key=os.path.getmtime)

def load_wrong_answers(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def save_wrong_answers_pdf(wrong_answers, filename="wrong_answers_report.pdf"):
    if not wrong_answers:
        print("No wrong answers found.")
        return

    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    margin = 50
    y = height - margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "ISTQB Wrong Answers Review Report")
    y -= 30

    c.setFont("Helvetica", 11)

    for wa in wrong_answers:
        if y < 60:
            c.showPage()
            y = height - margin
            c.setFont("Helvetica", 11)
        q_num = wa['number']
        section = wa.get("section", "N/A")
        c.drawString(margin, y, f"Question {q_num} — Section: {section}")
        y -= 18

    c.save()
    print(f"📄 Simplified PDF report saved as: {filename}")
if __name__ == "__main__":
    latest_file = find_latest_wrong_answers_file()
    if latest_file:
        print(f"📂 Using: {latest_file}")
        data = load_wrong_answers(latest_file)
        save_wrong_answers_pdf(data)
