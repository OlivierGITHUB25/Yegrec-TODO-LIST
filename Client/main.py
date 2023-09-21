import sys
#from PyQt5.QtGui import
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox

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

        if psw1 == psw2 :
            InfoBox("erreur mots de passe identique", QMessageBox.Icon.Warning)
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

        self.setWindowTitle("YeGrec")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Login()
    window.show()

    app.exec()