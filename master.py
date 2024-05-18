import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from processor import response_handler

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('GMRE Chatbot')
        self.setGeometry(100,100,400,500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.layout.addWidget(self.chat_history)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText('Enter your prompt here')
        self.layout.addWidget(self.message_input)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)


    def send_message(self):
        message = self.message_input.text()

        if message:
            self.chat_history.append(f'You: {message}')
            self.message_input.clear()

            self.receive_message(f'Bot: "{response_handler(message)}"')

    def receive_message(self,message):
        self.chat_history.append(message)


def main():
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()