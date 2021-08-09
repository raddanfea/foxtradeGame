import os
import re
import socket
import threading
import sys

import qdarkstyle
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QListWidget, QPushButton, QLineEdit, QPlainTextEdit


class chat_window(QWidget):


    def disconnect(self):
        self.client.disconnect()
        self.sendBtn.setDisabled(True)
        self.connBtn.setDisabled(False)
        self.discBtn.setDisabled(True)
        self.name_bar.setDisabled(False)
        self.ip_bar.setDisabled(False)

    def send_msg(self):
        message = self.textbox.text()
        name = self.name_bar.text()
        self.client.send_msg_manual(name + ": " + message)
        self.textbox.setText("")

    def is_ip(self, ip):
        return re.match(r'^\d{1,255}[.]\d{1,255}[.]\d{1,255}[.]\d{1,255}$', ip)

    def connect(self):
        try:
            ip = self.ip_bar.text()
            if self.is_ip(ip) is None:
                text = self.label.toPlainText()
                text += "Invalid IP.\n"
                self.label.setPlainText(text)

        except (ConnectionRefusedError, TimeoutError):
            text = self.label.toPlainText()
            text += "No Connection found.\n"
            self.label.setPlainText(text)



class Client:
    def __init__(self):
        self.terminal = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log = ""

    def connect(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, 10000))
        self.log += "Connected." + "\n"
        print("Connected.")

        oThread = threading.Thread(target=self.get_msg)
        oThread.daemon = True
        oThread.start()

        if self.terminal:
            while True:
                self.sock.send(bytes(input(""), 'utf-8'))
                print("\033")

    def disconnect(self):
        self.sock.close()

    def get_msg(self):
        try:
            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(str(data, 'utf-8'))
                self.log += str(data, 'utf-8') + "\n"
        except ConnectionAbortedError:
            self.log += "Disconnected." + "\n"

    def send_msg_manual(self, message):
        self.sock.send(bytes(message, 'utf-8'))


if __name__ == '__main__':
    if '-s' not in sys.argv:
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        window = chat_window()
        window.show()
        app.exec()
    else:
        try:
            client = Client()
            client.terminal = True
            client.connect(sys.argv[len(sys.argv) - 1])
        except ConnectionRefusedError:
            print("Failed to connect.")
