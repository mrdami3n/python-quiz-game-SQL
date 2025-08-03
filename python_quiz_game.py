import sys
import sqlite3
import random
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QFrame, QGridLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

# --- Application Styling (QSS - Qt Style Sheets) ---
# This is similar to CSS and allows for detailed styling of the UI elements.
STYLESHEET = """
    QWidget#MainWindow {
        background-color: #2B2B2B; /* Dark charcoal background */
    }
    QLabel {
        color: #F0F0F0; /* Light grey text for readability */
        font-size: 16px;
    }
    QLabel#TitleLabel {
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50; /* A nice green for Python theme */
        padding-bottom: 10px;
    }
    QLabel#QuestionLabel {
        font-size: 18px;
        font-style: italic;
        color: #F0F0F0;
        padding: 15px;
        border: 1px solid #444;
        border-radius: 8px;
        background-color: #3C3C3C; /* Slightly lighter charcoal for the question box */
        min-height: 100px;
    }
    QPushButton.AnswerButton {
        background-color: #4682B4; /* Steel Blue for answer buttons */
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        padding: 15px;
        margin-top: 5px;
    }
    QPushButton.AnswerButton:hover {
        background-color: #5A9BD5; /* Lighter blue on hover */
    }
    QPushButton.AnswerButton:pressed {
        background-color: #3A729B; /* Darker blue when pressed */
    }
    QPushButton#NewGameButton {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        margin-top: 10px;
    }
    QPushButton#NewGameButton:hover {
        background-color: #66BB6A;
    }
    QFrame#Header, QFrame#Footer {
        background-color: #3C3C3C;
        border-radius: 10px;
    }
"""

class PythonQuizGame(QWidget):
    """
    Main application class for the Python Quiz game.
    This class handles the UI setup, game logic, and database interaction.
    """
    def __init__(self):
        super().__init__()
        self.current_question_data = {}
        self.answer_buttons = []

        # --- Database Setup ---
        self.db_connection = sqlite3.connect('python_quiz.db')
        self.setup_database()

        # --- UI Initialization ---
        self.init_ui()
        self.start_new_game()

    def setup_database(self):
        """
        Sets up the SQLite database. Creates the 'questions' table if it
        doesn't exist and populates it with some sample data.
        """
        cursor = self.db_connection.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_option TEXT NOT NULL,
                explanation TEXT
            )
        ''')

        # Check if the table is empty
        cursor.execute("SELECT COUNT(*) FROM questions")
        if cursor.fetchone()[0] == 0:
            # Populate with sample Python questions
            sample_questions = [
                ('What is the output of `print(2 ** 3)`?', '6', '8', '9', '12', 'B', 'The `**` operator is used for exponentiation. 2 to the power of 3 is 8.'),
                ('Which of the following is a mutable data type in Python?', 'Tuple', 'String', 'List', 'Integer', 'C', 'Lists are mutable, meaning their elements can be changed after creation. Tuples and Strings are immutable.'),
                ('How do you start a single-line comment in Python?', '//', '#', '/*', '<!--', 'B', 'A single-line comment in Python starts with the hash (`#`) character.'),
                ('What method is used to get the length of a list named `my_list`?', 'my_list.length()', 'size(my_list)', 'len(my_list)', 'my_list.size()', 'C', 'The built-in `len()` function is used to get the number of items in a list or other sequence types.'),
                ('Which keyword is used to define a function in Python?', 'def', 'func', 'function', 'define', 'A', 'The `def` keyword is used to create, or define, a new function.')
            ]
            cursor.executemany('INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_option, explanation) VALUES (?, ?, ?, ?, ?, ?, ?)', sample_questions)
        
        self.db_connection.commit()

    def init_ui(self):
        """
        Initializes the main user interface of the application.
        It sets up all the widgets, layouts, and applies the stylesheet.
        """
        self.setObjectName("MainWindow")
        self.setWindowTitle("Python Quiz Challenge")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet(STYLESHEET)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Header ---
        header_frame = QFrame(self)
        header_frame.setObjectName("Header")
        header_layout = QVBoxLayout(header_frame)
        self.title_label = QLabel("Python Quiz Challenge", self)
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        # --- Question Display ---
        self.question_label = QLabel("This is where the question will appear.", self)
        self.question_label.setObjectName("QuestionLabel")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setWordWrap(True)

        # --- Answer Buttons ---
        answers_layout = QGridLayout()
        answers_layout.setSpacing(15)
        self.answer_buttons = []
        options = ['A', 'B', 'C', 'D']
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for i in range(4):
            button = QPushButton(f"Option {options[i]}", self)
            button.setObjectName("AnswerButton")
            button.setProperty("class", "AnswerButton") # For styling
            # Use a lambda to pass the option letter to the handler
            button.clicked.connect(lambda checked, opt=options[i]: self.handle_answer(opt))
            answers_layout.addWidget(button, positions[i][0], positions[i][1])
            self.answer_buttons.append(button)

        # --- Footer (New Game Button) ---
        footer_frame = QFrame(self)
        footer_frame.setObjectName("Footer")
        footer_layout = QVBoxLayout(footer_frame)
        self.new_game_button = QPushButton("Next Question", self)
        self.new_game_button.setObjectName("NewGameButton")
        self.new_game_button.clicked.connect(self.start_new_game)
        footer_layout.addWidget(self.new_game_button)

        # --- Assembling the Layout ---
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.question_label)
        main_layout.addLayout(answers_layout)
        main_layout.addStretch()
        main_layout.addWidget(footer_frame)

    def start_new_game(self):
        """
        Starts a new round by fetching a random question from the database
        and resetting the UI.
        """
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT question_text, option_a, option_b, option_c, option_d, correct_option, explanation FROM questions ORDER BY RANDOM() LIMIT 1")
        data = cursor.fetchone()

        if data:
            self.current_question_data = {
                'question': data[0],
                'options': {'A': data[1], 'B': data[2], 'C': data[3], 'D': data[4]},
                'correct': data[5],
                'explanation': data[6]
            }
        
        self.update_display()

    def update_display(self):
        """Updates the question and answer buttons with new data."""
        self.question_label.setText(self.current_question_data.get('question', ''))
        
        options = self.current_question_data.get('options', {})
        for i, button in enumerate(self.answer_buttons):
            option_letter = chr(65 + i) # A, B, C, D
            button.setText(f"{option_letter}: {options.get(option_letter, '')}")
            button.setEnabled(True) # Re-enable buttons for the new question

    def handle_answer(self, selected_option):
        """
        Checks the user's answer and provides feedback.
        """
        # Disable all buttons after an answer is chosen
        for button in self.answer_buttons:
            button.setEnabled(False)

        correct_option = self.current_question_data.get('correct')
        explanation = self.current_question_data.get('explanation')

        if selected_option == correct_option:
            title = "Correct!"
            message = f"That's right!\n\nExplanation: {explanation}"
            icon = QMessageBox.Icon.Information
        else:
            title = "Incorrect!"
            message = f"Sorry, the correct answer was {correct_option}.\n\nExplanation: {explanation}"
            icon = QMessageBox.Icon.Warning

        self.show_feedback(message, title, icon)

    def show_feedback(self, message, title, icon):
        """Shows a feedback message box."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setStyleSheet("QMessageBox { background-color: #3C3C3C; font-size: 14px; } QLabel { color: white; }")
        msg_box.exec()

    def closeEvent(self, event):
        """Ensures the database connection is closed when the app exits."""
        self.db_connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PythonQuizGame()
    game.show()
    sys.exit(app.exec())
