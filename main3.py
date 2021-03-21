import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from interface3 import *
from sympy import *

class MyWin(QtWidgets.QWidget):
    

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.pushButton_clicked)
        self.ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
 

    def pushButton_clicked(self):
        fx = self.ui.fxinput.text()
        x, y = symbols('x y')
        res = str(integrate(fx, x)) + ' + C'
        self.ui.fxoutput.setText(res)

    def pushButton_2_clicked(self):
        fx = self.ui.fx2input.text()
        a = self.ui.fainput.text()
        b = self.ui.fbinput.text()
        x, y = symbols('x y')
        res = str(integrate(fx, (x, a, b)))
        self.ui.fx2output.setText(res)


    def mbox(self, body, title='Error'):
        dialog = QMessageBox(QMessageBox.Information, title, body)
        dialog.exec_()

    


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())