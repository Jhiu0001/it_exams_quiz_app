# IT Exams Quiz App

### v0.2.0 – James Hiu – Aug.01.2026

A Flask-based quiz application designed to deliver structured, repeatable certification exams from JSON-based question banks.

The application supports multiple certification exams, configurable quiz lengths, deterministic answer randomization, and both Multiple Choice (MC) and Multi-Select (MS) question types. New certification exams can be added without modifying the application code by simply creating a new folder within the `test_bank` directory.

---

## Latest Updates (v0.2.0)

* Renamed project to support multiple IT certification exams.
* Added support for multiple exam banks through automatic folder discovery.
* Added exam selection drop-down on the quiz configuration page.
* Updated `quiz.py` to dynamically load questions from the selected exam.
* Improved question formatting to better support lengthy certification questions.
* Added display of the correct answer(s) after an incorrect response.
* Removed legacy question loading architecture in favor of per-exam loading.
* Simplified project maintenance by organizing each certification into its own folder.

---

## Features

* Flask web application
* Multiple certification exam support
* Automatic discovery of available exams
* JSON-driven question banks
* Multiple Choice (MC) support
* Multi-Select (MS) support
* Deterministic answer randomization per question
* Sequential or randomized question order
* Configurable quiz length
* Session-based scoring and progress tracking
* Displays correct answer(s) after incorrect responses
* Explanation support for each question
* Clean, lightweight interface
* Modular architecture for easy expansion

---

## Project Structure

```text
IT_EXAMS_QUIZ_APP/
│
├── quiz.py
├── _templates/
│   ├── quiz_start.html
│   ├── quiz.html
│   ├── quiz_end.html
│   └── test_question_template.json
│
├── test_bank/
│   ├── Databricks_GenAI_Engineer_Associate/
│   │   ├── Q001-Q010.json
│   │   ├── Q011-Q020.json
│   │   └── ...
│   │
│   ├── <Exam #2>/
│   │   ├── ...
|
│
├── archive/
│
├── user_testing/
│
├── README.md
└── .gitignore
```

---

## How It Works

1. On startup, the application scans the `test_bank` directory for available certification exams.
2. The user selects which certification exam to take.
3. Questions are loaded only from the selected exam folder.
4. The user configures:

   * Number of questions
   * Sequential or randomized question order
5. Answer choices are shuffled deterministically using each question's unique `question_id`.
6. Quiz progress and scoring are maintained using Flask sessions.
7. After an incorrect response, the application displays the correct answer(s) along with any explanation provided.

---

## Adding a New Certification Exam

Adding support for a new certification requires no code changes.

Simply create a new folder inside `test_bank`:

```text
test_bank/
    My_New_Certification/
        Q001-Q010.json
        Q011-Q020.json
```

The application will automatically detect the new certification and include it in the exam selection drop-down.

---

## Question Bank Notes

* Questions are stored as JSON files.
* Multiple JSON files may exist within a certification folder.
* Questions are merged automatically when an exam begins.
* `question_id` values must be unique within an exam.

---

## User Notes

* While editing JSON files in VS Code, press **Alt + Z** to enable Word Wrap.
* Keeping approximately 10 questions per JSON file makes reviewing and maintaining content much easier.
* Store works-in-progress inside `user_testing` before promoting them into `test_bank`.

---

## Prerequisites

* Python 3.9+
* Flask

