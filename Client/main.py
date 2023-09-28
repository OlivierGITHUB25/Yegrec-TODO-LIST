import sys
import socket
import json
import ssl
from threading import Thread
import time
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox, QScrollArea, QVBoxLayout, QFormLayout, QGroupBox, QComboBox, QDateEdit

class Login(QMainWindow):
    def __init__(self):
        self.window = None
        self.window2 = None
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        self.setWindowTitle("YeGrec login")

        self.lbl = QLabel(self)
        self.lbl.setText("Identifiant:")
        self.champ = QLineEdit(self)

        self.lbl2 = QLabel(self)
        self.lbl2.setText("Mots de Passe:")
        self.champ2 = QLineEdit(self)
        self.champ2.setEchoMode(QLineEdit.Password)

        self.bouton1 = QPushButton(self)
        self.bouton1.setText("Connexion")
        self.bouton1.clicked.connect(self.conn1)

        self.bouton2 = QPushButton(self)
        self.bouton2.setText("Créer un compte")
        self.bouton2.clicked.connect(self.user)

        grid.addWidget(self.lbl, 1, 1)
        grid.addWidget(self.lbl2, 3, 1)
        grid.addWidget(self.champ, 2, 1, 1, 2)
        grid.addWidget(self.champ2, 4, 1, 1, 2)
        grid.addWidget(self.bouton1, 5, 1)
        grid.addWidget(self.bouton2, 5, 2)

    def user(self):
        self.window2 = User()
        self.window2.show()
        window.close()

    def MonThread(self):
        

class MyThread(Thread):
    def __init__(self, jusqua):
        Thread.__init__(self)
        self.jusqua = jusqua
        self.etat = False

    def run(self):
        self.etat = True
        hostname = '127.0.0.1'

        context = ssl.create_default_context()
        context.load_verify_locations("./certs/CA.crt")

        with socket.create_connection((hostname, 5000)) as sock:
            print("test")
            with context.wrap_socket(sock, server_hostname=hostname) as conn:
                credentials = json.dumps([
                    {
                        "client": "login",
                        "username": "user",
                        "password": "psw1",
                    }
                ])
                conn.send(credentials.encode('utf-8'))

                msg = ""

                buffer = conn.recv(1024)
                rc = buffer.decode('utf-8')
                if rc != msg:
                    print(rc)
                    msg = rc

                conn.send(json.dumps([
                    {
                        "client": "disconnect"
                    }
                ]).encode('utf-8'))

m = MyThread(10)
m.start()

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