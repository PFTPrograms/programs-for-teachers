from interface import *
import exec_checker
import os
import sys
QApplication = QtWidgets.QApplication
QMainWindow = QtWidgets.QMainWindow
argvHasFile = False
if len(sys.argv) >= 2:
    sys.argv = sys.argv[:2]
    if os.path.isfile(sys.argv[1]):
        argvHasFile = True
class TextEditor(QMainWindow, Ui_MainWindow):
    STRINGS = {
        'E': 'Выйти',
        'N': 'Новый',
        'O': 'Открыть',
        'S': 'Сохранить',
        'C': 'Проверка'
        }
    def __init__(self):
        super(TextEditor, self).__init__(None)
        self.setupUi(self)
        self.openedFile = None
        self.saved = True
        self.checker = None
        if argvHasFile:
            self.openedFile = sys.argv[1]
        self.updateStatusbar()
        self.addActions()
        self.registerEvents()
    def addActions(self):
        self.act_E = QtWidgets.QAction(self.STRINGS['E'], self)
        self.act_N = QtWidgets.QAction(self.STRINGS['N'], self)
        self.act_O = QtWidgets.QAction(self.STRINGS['O'], self)
        self.act_S = QtWidgets.QAction(self.STRINGS['S'], self)
        self.act_C = QtWidgets.QAction(self.STRINGS['C'], self)
    def registerEvents(self):
        self.plainTextEdit.textChanged.connect(self.unsaved)
        self.menubar.addAction(self.act_N)
        self.act_N.triggered.connect(self.new)
        self.menubar.addAction(self.act_O)
        self.act_O.triggered.connect(self.open)
        self.menubar.addAction(self.act_S)
        self.menubar.addAction(self.act_C)
        self.act_C.triggered.connect(self.check_c)
        self.act_S.triggered.connect(self.save)
        self.menubar.addAction(self.act_E)
        self.act_E.triggered.connect(QtWidgets.qApp.quit)
    def unsaved(self):
        self.saved = False
        self.updateStatusbar()
    def updateStatusbar(self):
        msg = ''
        if self.openedFile:
            msg += self.openedFile
        else:
            msg += 'untitled'
        if not self.saved:
            msg += ' (не сохранено!)'
        self.statusBar().showMessage(msg, 3600000)
    def check(self):
        if not self.saved:
            reply = QtWidgets.QMessageBox.warning(
                self,
                'Несохранённый файл!',
                "Этот файл не сохранён.\nПродолжить?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                return True
            return False
        return True
    def save(self, ev=None):
        if not self.openedFile:
            res = QtWidgets.QFileDialog.getSaveFileName(self, 'Сохранить', QtCore.QDir.homePath())
            if not res or not res[0]:
                return
            self.openedFile = res[0]
        with open(self.openedFile, 'w') as f:
            f.write(self.plainTextEdit.toPlainText())
            self.saved = True
            self.updateStatusbar()
    def new(self, ev=None):
        if not self.check():
            return
        self.saved = True
        self.updateStatusbar()
        self.openedFile = None
        self.plainTextEdit.setPlainText('')
    def open(self, ev=None):
        if not self.check():
            return
        res = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', QtCore.QDir.homePath())
        if not res or not res[0]:
            return
        self.openedFile = res[0]
        with open(self.openedFile, 'rb') as f:
            s = f.read()
            try:
                s = s.decode()
            except UnicodeDecodeError:
                QtWidgets.QMessageBox.critical(
                    self,
                    'Ой!',
                    "Не могу прочитать этот файл.",
                    QtWidgets.QMessageBox.Ok,
                    QtWidgets.QMessageBox.Ok
                )
            else:
                self.plainTextEdit.setPlainText(s)
                self.saved = True
                self.updateStatusbar()
    def register_checker(self):
        res = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть чекер', QtCore.QDir.homePath())
        if not res or not res[0]:
            return
        self.openedFile = res[0]
        with open(self.openedFile, 'rb') as f:
            s = f.read()
            try:
                s = s.decode()
            except UnicodeDecodeError:
                QtWidgets.QMessageBox.critical(
                    self,
                    'Ой!',
                    "Не могу прочитать этот файл.",
                    QtWidgets.QMessageBox.Ok,
                    QtWidgets.QMessageBox.Ok
                )
            else:
                self.checker = s.strip()
    def check_c(self, ev=None):
        if not self.checker:
            self.register_checker()
        else:
            exec_checker.exec_(self.checker, self.plainTextEdit.toPlainText().strip(), onok=self.show_ok, onerr=self.show_err, onbad=self.show_bad)
    def show_ok(self):
        QtWidgets.QMessageBox.information(
                    self,
                    'Правильно',
                    "Правильно!",
                    QtWidgets.QMessageBox.Ok,
                    QtWidgets.QMessageBox.Ok
                    )
    def show_err(self):
        QtWidgets.QMessageBox.critical(
                    self,
                    'Ой!',
                    "Ошибка!",
                    QtWidgets.QMessageBox.Ok,
                    QtWidgets.QMessageBox.Ok
                    )
    def show_bad(self):
        QtWidgets.QMessageBox.critical(
                    self,
                    'Ой!',
                    "Ошибка в чекере!",
                    QtWidgets.QMessageBox.Ok,
                    QtWidgets.QMessageBox.Ok
                    )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = TextEditor()
    e.show()
    sys.exit(app.exec_())
