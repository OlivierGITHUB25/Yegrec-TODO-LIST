import sys
from PyQt5 import QtWidgets, QtGui, QtCore

# Création de la classe de la fenêtre de connexion
class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Initialiser l'interface utilisateur

    # Initialiser l'interface utilisateur
    def init_ui(self):
        self.setWindowTitle("Login")  # Définir le titre de la fenêtre
        self.setGeometry(100, 100, 280, 150)  # Définir la taille et la position
        self.setStyleSheet("background-color: black; color: white;")  # Définir le style de base

        layout = QtWidgets.QVBoxLayout()  # Créer un layout vertical

        # Créer et configurer le label du titre
        title = QtWidgets.QLabel("Login")
        title.setAlignment(QtCore.Qt.AlignCenter)  # Centrer le titre
        title.setFont(QtGui.QFont('Arial', 20))  # Définir la police et la taille

        # Créer et configurer le label du nom d'utilisateur
        username_label = QtWidgets.QLabel("username")
        username_label.setFont(QtGui.QFont('Arial', 10))  # Définir la police et la taille

        # Créer et configurer la zone de saisie du nom d'utilisateur
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setStyleSheet("background-color: black; border: 1px solid cyan; border-radius: 5px; color: cyan; padding: 5px;")

        # Créer et configurer le label du mot de passe
        password_label = QtWidgets.QLabel("password")
        password_label.setFont(QtGui.QFont('Arial', 10))  # Définir la police et la taille

        # Créer et configurer la zone de saisie du mot de passe
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)  # Masquer le mot de passe
        self.password_input.setStyleSheet("background-color: black; border: 1px solid cyan; border-radius: 5px; color: cyan; padding: 5px;")

        # Créer et configurer le bouton de connexion
        login_button = QtWidgets.QPushButton("Login")
        login_button.setStyleSheet("QPushButton {background-color: cyan; border: 1px solid cyan; border-radius: 10px; padding: 5px; color: black;} QPushButton::hover {background-color: white;}")

        # Ajouter les widgets au layout
        layout.addWidget(title)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.setAlignment(QtCore.Qt.AlignCenter)  # Centrer les widgets dans le layout

        # Appliquer le layout à la fenêtre de l'application
        self.setLayout(layout)

# Point d'entrée de l'application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Créer une application PyQt
    window = LoginWindow()  # Instancier la fenêtre de connexion
    window.show()  # Afficher la fenêtre
    sys.exit(app.exec_())  # Exécuter l'application
