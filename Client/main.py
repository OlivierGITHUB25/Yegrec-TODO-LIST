import sys
#from PyQt5.QtGui import QcloseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication, QLabel, QLineEdit, QPushButton

class Login(QMainWindow):
    def __init__(self):
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

        self.bouton = QPushButton(self)
        self.bouton.setText("Login")
        #self.bouton.clicked.Login(self.Login)

        grid.addWidget(self.lbl, 1, 1)
        grid.addWidget(self.lbl2, 1, 2)
        grid.addWidget(self.champ, 1, 3)
        grid.addWidget(self.champ2, 1, 4)
        grid.addWidget(self.bouton, 1, 5)


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

    Window = Login()
    Window.show()

    app.exec()