import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QApplication
import socket


class Notify(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle('Адрес')
        self.text = QLineEdit(self)
        self.text.move(60, 100)
        self.text.resize(300, 24)
        self.text.setText('http://' + socket.gethostbyname(socket.gethostname()) + ':5000/')
        self.text.textChanged[str].connect(self.onChanged)
        self.resize(400, 300)
        self.show()
    def onChanged(self, text):
        self.text.setText(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notify = Notify()
    sys.exit(app.exec_())
