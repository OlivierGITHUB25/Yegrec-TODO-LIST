import sys
from PyQt5 import QtWidgets, QtGui, QtCore

# Classe principale pour l'application de to-do list
class TodoListApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Initialiser l'interface utilisateur

    # Initialiser l'interface utilisateur
    def init_ui(self):
        self.setWindowTitle("To-Do List")  # Définir le titre de la fenêtre
        self.setGeometry(100, 100, 400, 600)  # Définir la taille et la position
        self.setStyleSheet("background-color: black; color: white;")  # Définir le style de base

        layout = QtWidgets.QVBoxLayout()  # Créer un layout vertical

        # Créer et configurer le titre de la to-do list
        title = QtWidgets.QLabel("To-Do List")
        title.setAlignment(QtCore.Qt.AlignCenter)  # Centrer le titre
        title.setFont(QtGui.QFont('Arial', 24))  # Définir la police et la taille

        # Créer la zone de saisie pour les nouvelles tâches
        self.task_input = QtWidgets.QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.setStyleSheet("background-color: black; border: 1px solid cyan; border-radius: 5px; color: cyan; padding: 5px;")

        # Créer le sélecteur de date et heure
        self.date_time_selector = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_time_selector.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.date_time_selector.setStyleSheet("background-color: black; color: cyan; border: 1px solid cyan; padding: 5px;")

        # Créer le bouton pour ajouter une nouvelle tâche
        add_button = QtWidgets.QPushButton("Add Task")
        add_button.setStyleSheet("QPushButton {background-color: cyan; border: 1px solid cyan; border-radius: 10px; padding: 5px; color: black;} QPushButton::hover {background-color: white;}")

        # Créer la liste des tâches
        self.tasks_list = QtWidgets.QListWidget()
        self.tasks_list.setStyleSheet("background-color: black; border: 1px solid cyan; color: cyan; padding: 5px;")

        # Créer le bouton pour supprimer la tâche sélectionnée
        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.setStyleSheet("QPushButton {background-color: red; border: 1px solid red; border-radius: 10px; padding: 5px; color: black;} QPushButton::hover {background-color: white;}")

        # Connecter les boutons à leurs actions correspondantes
        add_button.clicked.connect(self.add_task)
        delete_button.clicked.connect(self.delete_task)

        # Ajouter les widgets au layout
        layout.addWidget(title)
        layout.addWidget(self.task_input)
        layout.addWidget(self.date_time_selector)
        layout.addWidget(add_button)
        layout.addWidget(self.tasks_list)
        layout.addWidget(delete_button)

        # Appliquer le layout à la fenêtre de l'application
        self.setLayout(layout)

    # Ajouter une nouvelle tâche à la liste
    def add_task(self):
        task_text = self.task_input.text().strip()  # Récupérer le texte saisi et supprimer les espaces
        task_date_time = self.date_time_selector.dateTime().toString("yyyy-MM-dd HH:mm")  # Récupérer la date et l'heure
        if task_text:  # Si le texte n'est pas vide
            task_with_date = f"{task_text} (Due: {task_date_time})"  # Formater la tâche avec la date
            self.tasks_list.addItem(task_with_date)  # Ajouter la tâche à la liste
            self.task_input.clear()  # Effacer le champ de saisie

    # Supprimer la tâche sélectionnée de la liste
    def delete_task(self):
        selected_items = self.tasks_list.selectedItems()  # Récupérer les éléments sélectionnés
        if selected_items:  # Si un élément est sélectionné
            for item in selected_items:
                self.tasks_list.takeItem(self.tasks_list.row(item))  # Supprimer l'élément de la liste

# Point d'entrée de l'application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Créer une application PyQt
    window = TodoListApp()  # Instancier la fenêtre de la to-do list
    window.show()  # Afficher la fenêtre
    sys.exit(app.exec_())  # Exécuter l'application
