import sys
import socket
import json
import ssl
import threading
from threading import Thread
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QScrollArea, QVBoxLayout, QFormLayout, QGroupBox, QComboBox, QDateEdit

def CssLoader(filename):
    with open(filename,'r') as rd:
        content = rd.read()
        rd.close()
    return content
class Login(QWidget):
    def __init__(self):
        self.window = None
        self.window2 = None
        self.thread = None
        super().__init__()
        #self.setCentralWidget(self)
        self.setObjectName('MainWindow')
        grid = QGridLayout()
        self.setLayout(grid)
        self.thread = MyThreadsend(self)
        self.setStyleSheet(CssLoader('style.css'))

        self.setWindowTitle("YeGrec login")
        self.setWindowIcon(QIcon('logo.png'))

        self.lbl = QLabel(self)
        self.lbl.setText("Identifiant:")
        self.lbl.setObjectName('id')
        self.champ = QLineEdit(self)
        self.champ.setObjectName('champ')

        self.lbl2 = QLabel(self)
        self.lbl2.setText("Mots de Passe:")
        self.champ2 = QLineEdit(self)
        self.champ2.setEchoMode(QLineEdit.Password)

        self.bouton1 = QPushButton(self)
        self.bouton1.setText("Connexion")
        self.bouton1.clicked.connect(self.monThread)

        self.bouton2 = QPushButton(self)
        self.bouton2.setText("Créer un compte")
        self.bouton2.clicked.connect(self.user)

        grid.addWidget(self.lbl, 1, 1)
        grid.addWidget(self.lbl2, 3, 1)
        grid.addWidget(self.champ, 2, 1, 1, 4)
        grid.addWidget(self.champ2, 4, 1, 1, 4)
        grid.addWidget(self.bouton1, 5, 1, 1, 2)
        grid.addWidget(self.bouton2, 5, 3, 1, 2)

    def user(self):
        self.window2 = User()
        self.window2.show()
        window.close()

    def monThread(self):
        action_client = "login"
        user = self.champ.text()
        PSW = self.champ2.text()
        self.thread.action(action_client, user, PSW)

    def LoginErreur(self):
        thead = threading.Thread(target=self.__LoginErreur)
        thead.start()

    def __LoginErreur(self):
        InfoBoxLogin("erreur mots de passe ou identifiant invalide", QMessageBox.Icon.Warning)
class InfoBoxLogin(QMessageBox):
    def __init__(self, message: str, type: QMessageBox.Icon):
        super().__init__()
        self.setText(message)
        self.setWindowTitle("Error")
        self.setIcon(type)
        self.setStandardButtons(QMessageBox.Ok)
        self.exec_()

class MyThreadsend:

    def __init__(self, login_object):
        self.login_object = login_object
        self.hostname = '127.0.0.1'
        self.context = ssl.create_default_context()
        self.connexion = False
        self.threadtest = False


    def action(self, action_client, user="", PSW=""):
        self.action_client = action_client
        self.user = user
        self.PSW = PSW
        if not self.threadtest:
            thread = threading.Thread(target=self.run)
            thread.start()
            self.threadtest = True
        else:
            self.run()

    def run(self):
        self.context.load_verify_locations("./certs/CA.crt")
        if not self.connexion:
            sock = socket.create_connection((self.hostname, 5000))
            self.conn = self.context.wrap_socket(sock, server_hostname=self.hostname)
            self.connexion = True

        while True:
            #time.sleep(1)
            if self.action_client == "login":
                print("test9")
                self.logintest()


    def logintest(self):
            print("test")
            credentials = json.dumps([
                {
                    "client": self.action_client,
                    "username": self.user,
                    "password": self.PSW,
                }
            ])
            print("test8")
            self.conn.send(credentials.encode('utf-8'))
            print("test9")
            buffer = self.conn.recv(1024)
            print("test10")
            rc = buffer.decode('utf-8')
            rc =json.loads(rc)
            for item in rc:
                print("ssqqs")
                autho = item["authorized"]
            if autho == "yes":
                print("yes")
            else:
                print("no")
                self.login_object.LoginErreur()





class User(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.setWindowTitle("YeGrec User")

        self.lbl = QLabel(self)
        self.lbl.setText("Identifiant:")
        self.champ = QLineEdit(self)

        self.lbl2 = QLabel(self)
        self.lbl2.setText("Mots de Passe:")
        self.champ2 = QLineEdit(self)
        self.champ2.setEchoMode(QLineEdit.Password)

        self.lbl3 = QLabel(self)
        self.lbl3.setText("Confirmer le mot de passe:")
        self.champ3 = QLineEdit(self)
        self.champ3.setEchoMode(QLineEdit.Password)

        self.bouton1 = QPushButton(self)
        self.bouton1.setText("suivant")
        self.bouton1.clicked.connect(self.suivant)

        self.msg = QMessageBox

        grid.addWidget(self.lbl, 1, 1)
        grid.addWidget(self.lbl2, 3, 1)
        grid.addWidget(self.lbl3, 5, 1)
        grid.addWidget(self.champ, 2, 1, 1, 2)
        grid.addWidget(self.champ2, 4, 1, 1, 2)
        grid.addWidget(self.champ3, 6, 1, 1, 2)
        grid.addWidget(self.bouton1, 7, 1)

    def suivant(self):
        user = self.champ.text()
        psw1 = self.champ2.text()
        psw2 = self.champ3.text()

        if psw1 != psw2 :
            InfoBox("erreur mots de passe pas identique", QMessageBox.Icon.Warning)
        else:
            print("test")
            self.close()

class InfoBox(QMessageBox):
    def __init__(self, message: str, type: QMessageBox.Icon):
        super().__init__()
        self.setText(message)
        self.setWindowTitle("Error")
        self.setIcon(type)
        self.setStandardButtons(QMessageBox.Ok)
        self.exec_()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setGeometry(100, 100, 1000, 300)

        self.setWindowTitle("YeGrec")

        self.formLayout1 = QFormLayout()
        self.groupBox1 = QGroupBox()

        self.formLayout2 = QFormLayout()
        self.groupBox2 = QGroupBox()

        self.groupBox1.setLayout(self.formLayout1)

        self.scroll1 = QScrollArea()
        self.scroll1.setWidget(self.groupBox1)
        self.scroll1.setWidgetResizable(True)

        self.layout1 = QVBoxLayout(self)
        self.layout1.addWidget(self.scroll1)

        self.groupBox2.setLayout(self.formLayout2)

        self.scroll2 = QScrollArea()
        self.scroll2.setWidget(self.groupBox2)
        self.scroll2.setWidgetResizable(True)

        self.layout2 = QVBoxLayout(self)
        self.layout2.addWidget(self.scroll2)

        self.bouton1 = QPushButton(self)
        self.bouton1.setText("Créer une tâche")
        self.bouton1.clicked.connect(self.tache)

        grid.addWidget(self.bouton1, 1, 1)
        grid.addWidget(self.scroll1, 2, 1)
        grid.addWidget(self.scroll2, 3, 1)

    def tache(self):
        self.window2 = Tache()
        self.window2.show()


        for n in range(100):
            label1 = QLabel("YOYOYOYO")
            self.formLayout1.addRow(label1)

        for n in range(100):
            label2 = QLabel("YOYOYOYO")
            self.formLayout2.addRow(label2)

class Tache(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.setWindowTitle("YeGrec Tâche")

        self.lbl1 = QLabel(self)
        self.lbl1.setText("Attribuer la tâche à quel utilisateur")
        self.combobox = QComboBox()

        self.lbl2 = QLabel(self)
        self.lbl2.setText("nom de la tâche:")
        self.champ2 = QLineEdit(self)
        self.champ2.setEchoMode(QLineEdit.Password)

        self.lbl3 = QLabel(self)
        self.lbl3.setText("priorité")
        self.combobox2 = QComboBox()
        self.combobox2.addItems(['faible', 'moyenne', 'haut'])

        self.lbl4 = QLabel(self)
        self.lbl4.setText("Date")
        self.date = QDateEdit(self, calendarPopup=True)

        #pas supr
        #self.datetime = QDate.currentDate()
        #self.lbl4 = QLabel(self)
        #self.lbl4.setText(self.datetime.toString(Qt.DefaultLocaleLongDate))

        
        grid.addWidget(self.lbl1, 1, 1)
        grid.addWidget(self.combobox, 2, 1)
        grid.addWidget(self.lbl2, 3, 1)
        grid.addWidget(self.champ2, 4, 1)
        grid.addWidget(self.lbl3, 5, 1)
        grid.addWidget(self.combobox2, 6, 1)
        grid.addWidget(self.date, 8, 1)
        grid.addWidget(self.lbl4, 7, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #window = MainWindow()
    window = Login()
    window.show()

    app.exec()