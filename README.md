# Python SQL Quiz Challenge
A sleek and engaging desktop quiz application built with Python, PyQt6, and SQLite. This project serves as a practical and educational example of how to create a modern GUI application that interacts with a local database.

## Features
Modern User Interface: Styled with QSS (similar to CSS) for a dark, professional look and feel.

Dynamic Content: Questions are loaded dynamically from a local SQLite database.

Multiple-Choice Format: Classic and effective quiz format with four selectable answers.

Instant Feedback: Immediately know if your answer was correct, along with a clear explanation.

Educational: A fun way to test your Python knowledge.

Self-Contained: The application creates and populates its own database on the first run.

## Technologies Used
Python: The core programming language.

PyQt6: A comprehensive set of Python bindings for the Qt v6 application framework, used for the graphical user interface (GUI).

SQLite: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. Used for local data storage.

## Setup and Installation
To get this project up and running on your local machine, follow these simple steps.

Prerequisites
Make sure you have Python 3 installed on your system. You can download it from python.org.

Installation
Clone the repository

```
git clone https://github.com/mrdami3n/python-quiz-game-SQL.git
cd python-quiz-game-SQL
```

Install the necessary dependencies
The only external library required is PyQt6. You can install it using pip.

```
pip install PyQt6
```

Run the application
Execute the main Python script from your terminal.

```
python python_quiz_game.py 
```

The application will automatically create a python_quiz.db file in the same directory on its first launch.

## How It Works
The application is built around a single main class, PythonQuizGame, which handles the UI, game logic, and database interactions.

Database (setup_database): On startup, the application connects to an SQLite database file (python_quiz.db). If the file or the questions table doesn't exist, it creates them and populates the table with a set of sample Python questions.

User Interface (init_ui): The UI is constructed using widgets from the PyQt6 library (like QPushButton, QLabel, etc.) and arranged using layouts (QVBoxLayout, QGridLayout). The entire application is styled using a QSS stylesheet string, which provides a custom look distinct from standard OS styles.

Game Logic (start_new_game, handle_answer):

A new question is started by fetching a random row from the questions table in the database using an ORDER BY RANDOM() SQL query.

The UI is updated with the new question and answer options.

When the user clicks an answer, the handle_answer method checks if the selected option matches the correct_option stored in the database for the current question.

A message box provides immediate feedback, including an explanation for the correct answer, which is also retrieved from the database.

📄 License
This project is licensed under the MIT License
