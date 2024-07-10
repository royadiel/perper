import sys
import pyperclip
import requests
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

def read_clipboard():
    return pyperclip.paste()

def query_perplexity(text):
    url = 'https://api.perplexity.ai/chat/completions'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer YOUR_API_KEY'
    }
    body = {
        'model': 'llama-3-sonar-small-32k-chat',
        'stream': False,
        'max_tokens': 1024,
        'temperature': 0.0,
        'messages': [
            {'role': 'system', 'content': 'Be precise and concise in your responses.'},
            {'role': 'user', 'content': text}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as e:
        error_detail = response.json() if response.text else "No error details available"
        return f"HTTP error occurred: {e}. Error details: {error_detail}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return f"Error parsing API response: {e}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perplexity API Response")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setFont(QFont("Arial", 12))
        layout.addWidget(self.response_text)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.process_query()

    def process_query(self):
        clipboard_text = read_clipboard()
        api_response = query_perplexity(clipboard_text)
        self.response_text.setText(api_response)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.response_text.toPlainText())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()%                                                                     roy.adiel@vsap-mac-CJ74T196PV Misc % cat perper2.py
