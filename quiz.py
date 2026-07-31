from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
import string
import os

app = Flask(__name__, template_folder="_templates")
app.secret_key = "your-secret-key"

# ----------------------------------------------------
# Load questions from test bank
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_BANK_DIR = os.path.join(BASE_DIR, "test_bank")

def load_questions(exam_name):

    exam_dir = os.path.join(TEST_BANK_DIR, exam_name)

    all_questions = []

    for filename in sorted(os.listdir(exam_dir)):
        if filename.endswith(".json"):
            with open(os.path.join(exam_dir, filename), "r", encoding="utf-8") as f:
                all_questions.extend(json.load(f))

    ids = [q["question_id"] for q in all_questions]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate question_id detected")

    question_lookup = {
        q["question_id"]: q
        for q in all_questions
    }

    return all_questions, question_lookup

# ----------------------------------------------------
# START PAGE: Configure quiz
# ----------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def start_quiz():
    if request.method == "POST":

        # ----- Parse inputs safely -----
        try:
            requested = int(request.form.get("num_questions", 60))
        except ValueError:
            requested = 60

        requested = max(1, requested)

        randomize = "randomize" in request.form
        exam_name = request.form["exam_name"]
        all_questions, question_lookup = load_questions(exam_name)

        total_available = len(all_questions)
        effective_count = min(requested, total_available)

        # ----- Select questions -----
        if randomize:
            selected_questions = random.sample(all_questions, effective_count)
        else:
            selected_questions = all_questions[:effective_count]

        # ----- Initialize session -----
        session.clear()
        session.update({
            "exam_name": exam_name,
            "quiz_question_ids": [q["question_id"] for q in selected_questions],
            "question_index": 0,
            "score": 0,
            "answered": False,
            "is_correct": None
        })

        return redirect(url_for("quiz"))

    exams = sorted([
        folder
        for folder in os.listdir(TEST_BANK_DIR)
        if os.path.isdir(os.path.join(TEST_BANK_DIR, folder))
    ])

    return render_template(
        "quiz_start.html",
        exams=exams
    )


# ----------------------------------------------------
# QUIZ PAGE
# ----------------------------------------------------

@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if "quiz_question_ids" not in session:
        return redirect(url_for("start_quiz"))

    exam_name = session["exam_name"]
    all_questions, question_lookup = load_questions(exam_name)

    question_ids = session["quiz_question_ids"]
    questions = [question_lookup[qid] for qid in question_ids]
    q_index = session["question_index"]

    # Quiz finished
    if q_index >= len(questions):
        score = session["score"]
        total = len(questions)
        session.clear()
        return render_template("quiz_end.html", score=score, total=total)

    question = questions[q_index]

    # Shuffle ANSWERS deterministically per question
    choices = question["choices"][:]
    rng = random.Random(question["question_id"])
    rng.shuffle(choices)

    labels = list(string.ascii_uppercase)
    labeled_choices = dict(zip(labels, choices))

    # ---------------- POST LOGIC ----------------
    if request.method == "POST":

        # NEXT QUESTION
        if "next" in request.form:
            session["question_index"] += 1
            session["answered"] = False
            session["is_correct"] = None
            return redirect(url_for("quiz"))

        session["answered"] = True

        if question["type"] == "MC":
            selected_label = request.form["choice"]
            selected_choice = labeled_choices[selected_label]

            if selected_choice["id"] == question["ans_id"]:
                session["score"] += 1
                session["is_correct"] = True
            else:
                session["is_correct"] = False

        elif question["type"] == "MS":
            selected_labels = request.form.getlist("choice")
            selected_ids = [labeled_choices[label]["id"] for label in selected_labels]

            if sorted(selected_ids) == sorted(question["ans_ids"]):
                session["score"] += 1
                session["is_correct"] = True
            else:
                session["is_correct"] = False

    correct_answers = []

    if question["type"] == "MC":
        for label, choice in labeled_choices.items():
            if choice["id"] == question["ans_id"]:
                correct_answers.append({
                    "label": label,
                    "text": choice["text"]
                })

    elif question["type"] == "MS":
        for label, choice in labeled_choices.items():
            if choice["id"] in question["ans_ids"]:
                correct_answers.append({
                    "label": label,
                    "text": choice["text"]
                })

    return render_template(
    "quiz.html",
    question=question,
    labeled_choices=labeled_choices,
    answered=session["answered"],
    is_correct=session["is_correct"],
    current_number=q_index + 1,
    total_questions=len(questions),
    correct_answers=correct_answers
    )

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("quiz"))



@app.route("/exit")
def exit_quiz():
    session.clear()
    return redirect(url_for("start_quiz"))

if __name__ == "__main__":
    app.run(debug=True)
