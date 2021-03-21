from interface import *
import sys
import base64
from flask import *
from requests import get
import socket
import subprocess as sp
import tkinter as tk
from threading import Thread


def do_nothing(): pass


class Flag:
    def __init__(self, val: bool=False):
        self.__value = bool(val)
        self.__event_handlers = {'set': do_nothing, 'unset': do_nothing}
    def set(self):
        self.__value = True
        self.__do_event('set')
    def unset(self):
        self.__value = False
        self.__do_event('unset')
    def get(self):
        return self.__value
    def handler(self, event_name):
        def decor(func):
            self.__event_handlers[event_name] = func
            return func
        return decor
    def on_set(self, func):
        return self.handler('set')
    def on_unset(self, func):
        return self.handler('unset')
    def __do_event(self, name):
        self.__event_handlers[name]()


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
    def setTitle(self, text):
        self.label.setText(text)


app = QtWidgets.QApplication(sys.argv)
win = Window()
win.show()
win.hide()
ip = get('https://api.ipify.org').text

f = Flask(__name__)
locked = False
@f.route('/lock/')
def page_l():
    global locked
    locked = True
    msg = request.args.get('msg', 'Заблокировано')
    win.setTitle(msg)
    win.show()
    win.showFullScreen()
    return redirect('/')
@f.route('/unlock/')
def page_u():
    global locked
    locked = False
    win.showNormal()
    win.hide()
    return redirect('/')
@f.route('/')
def page_c():
    content = f'<html><head><title>Блокировка экрана:  {socket.gethostbyname(socket.gethostname())}</title></head><body>'
    if not locked:
        content += '<form action="/lock"><p>Сообщение (необязательно): <input name="msg"></p><input type="submit" value="Заблокировать"></form>'
    else:
        content += '<p><a href="/unlock">Разблокировать</a></p>'
    content += '</body></html>'
    return content
kwargs = {'host': '0.0.0.0', 'port': 5000, 'threaded': True, 'use_reloader': False, 'debug': False}
flaskThread = Thread(target=f.run, daemon=True, kwargs=kwargs).start()
app.exec_()
