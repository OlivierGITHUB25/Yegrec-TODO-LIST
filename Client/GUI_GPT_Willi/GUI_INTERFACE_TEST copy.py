import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore

# Fenêtre de dialogue pour la version
class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Version")
        self.setGeometry(100, 100, 200, 100)
        layout = QtWidgets.QVBoxLayout(self)
        version_label = QtWidgets.QLabel("alpha V0.1", self)
        layout.addWidget(version_label)

# Fenêtre de dialogue pour la création et la modification de tâche
class TaskCreationWindow(QtWidgets.QDialog):
    def __init__(self, task=None):
        super().__init__()
        self.task = task or {}
        self.setWindowTitle("Task Details")
        self.setGeometry(100, 100, 300, 200)
        layout = QtWidgets.QVBoxLayout(self)
        
        # Nom de la tâche
        self.name_input = QtWidgets.QLineEdit(self.task.get('name', ''))
        self.name_input.setPlaceholderText("Task Name")
        
        # Description de la tâche
        self.description_input = QtWidgets.QTextEdit(self.task.get('description', ''))
        self.description_input.setPlaceholderText("Task Description")
        
        # Priorité de la tâche
        self.priority_input = QtWidgets.QComboBox()
        self.priority_input.addItems(["1", "2", "3"])
        priority_index = self.priority_input.findText(self.task.get('priority', '1'))
        self.priority_input.setCurrentIndex(priority_index)
        
        # Date de la tâche
        date = QtCore.QDateTime.fromString(self.task.get('date', QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm")), "yyyy-MM-dd HH:mm")
        self.date_input = QtWidgets.QDateTimeEdit(date)
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        
        # Bouton pour sauvegarder la tâche
        save_task_btn = QtWidgets.QPushButton("Save Task")
        save_task_btn.clicked.connect(self.accept)
        
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.date_input)
        layout.addWidget(save_task_btn)

    def get_task_details(self):
        return {
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText(),
            'priority': self.priority_input.currentText(),
            'date': self.date_input.dateTime().toString("yyyy-MM-dd HH:mm")
        }

# Fenêtre de dialogue pour la création et la modification de sous-tâche
class SubTaskCreationWindow(QtWidgets.QDialog):
    def __init__(self, subtask=None):
        super().__init__()
        self.subtask = subtask or {}
        self.setWindowTitle("Subtask Details")
        self.setGeometry(100, 100, 300, 150)
        layout = QtWidgets.QVBoxLayout(self)
        
        # Nom de la sous-tâche
        self.name_input = QtWidgets.QLineEdit(self.subtask.get('name', ''))
        self.name_input.setPlaceholderText("Subtask Name")
        
        # Description de la sous-tâche
        self.description_input = QtWidgets.QTextEdit(self.subtask.get('description', ''))
        self.description_input.setPlaceholderText("Subtask Description")
        
        # Bouton pour sauvegarder la sous-tâche
        save_subtask_btn = QtWidgets.QPushButton("Save Subtask")
        save_subtask_btn.clicked.connect(self.accept)
        
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(save_subtask_btn)

    def get_subtask_details(self):
        return {
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText()
        }
# ... [Les classes de la Partie 1 vont ici] ...

# Classe principale pour l'application de to-do list
class TodoListApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ye'Grec")
        self.setGeometry(100, 100, 400, 600)

        # Menu Bar
        menu_bar = self.menuBar()
        option_menu = menu_bar.addMenu("&Option")
        help_menu = menu_bar.addMenu("&Aide")

        # Theme Menu
        theme_menu = option_menu.addMenu("&Thème")
        light_theme_action = theme_menu.addAction("Thème clair")
        dark_theme_action = theme_menu.addAction("Thème sombre")

        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))

        # Help Menu
        contact_action = help_menu.addAction("&Contact")
        version_action = help_menu.addAction("&Version")

        contact_action.triggered.connect(self.open_github)
        version_action.triggered.connect(self.show_version)

        # Central Widget and Layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Titre de la fenêtre
        self.title = QtWidgets.QLabel("Ye'Grec")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont('Arial', 24))

        # Bouton pour ajouter une nouvelle tâche
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.clicked.connect(self.show_task_creation_dialog)

        # Layout pour les boutons de tri
        sort_buttons_layout = QtWidgets.QHBoxLayout()

        # Bouton pour trier par date
        sort_date_btn = QtWidgets.QPushButton("Sort by Date")
        sort_date_btn.clicked.connect(lambda: self.apply_filter("date"))

        # Bouton pour trier par priorité
        sort_priority_btn = QtWidgets.QPushButton("Sort by Priority")
        sort_priority_btn.clicked.connect(lambda: self.apply_filter("priority"))

        # Ajout des boutons de tri au layout horizontal
        sort_buttons_layout.addWidget(sort_date_btn)
        sort_buttons_layout.addWidget(sort_priority_btn)

        # Liste des tâches
        self.tasks_list = QtWidgets.QListWidget()
        self.tasks_list.itemClicked.connect(self.edit_task_or_subtask)

        # Bouton pour supprimer la tâche sélectionnée
        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.clicked.connect(self.delete_task)

        # Ajouter les widgets au layout
        layout.addWidget(self.title)
        layout.addWidget(add_task_btn)
        layout.addLayout(sort_buttons_layout)
        layout.addWidget(self.tasks_list)
        layout.addWidget(delete_button)

        # Set the initial theme
        self.set_theme("dark")

    # ... [Méthodes de TodoListApp, y compris update_tasks_list, edit_task_or_subtask, etc.] ...

# ... [Reste du code, y compris le point d'entrée principal] ...
    # ... [Suite de la classe TodoListApp] ...

    def update_tasks_list(self):
        self.tasks_list.clear()
        for index, task in enumerate(self.tasks):
            task_text = f"{task['name']}: {task['description']} | {task['date']}"
            task_item = QtWidgets.QListWidgetItem(task_text)
            self.tasks_list.addItem(task_item)
            task_item.setData(QtCore.Qt.UserRole, (index, None))

            for subindex, subtask in enumerate(task.get('subtasks', [])):
                subtask_text = f"    → {subtask['name']}: {subtask['description']}"
                subtask_item = QtWidgets.QListWidgetItem(subtask_text)
                subtask_item.setFont(QtGui.QFont('Arial', 10))
                self.tasks_list.addItem(subtask_item)
                subtask_item.setData(QtCore.Qt.UserRole, (index, subindex))

        self.tasks_list.itemClicked.connect(self.edit_task_or_subtask)

    def edit_task_or_subtask(self, item):
        indexes = item.data(QtCore.Qt.UserRole)
        if indexes[1] is None:  # It's a main task
            task = self.tasks[indexes[0]]
            dialog = TaskCreationWindow(task)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self.tasks[indexes[0]] = dialog.get_task_details()
                self.update_tasks_list()
        else:  # It's a subtask
            subtask = self.tasks[indexes[0]]['subtasks'][indexes[1]]
            dialog = SubTaskCreationWindow(subtask)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self.tasks[indexes[0]]['subtasks'][indexes[1]] = dialog.get_subtask_details()
                self.update_tasks_list()

    # ... [Autres méthodes pour les thèmes, ouvrir GitHub, etc.] ...
    # ... [Suite de la classe TodoListApp] ...

    def set_theme(self, theme):
        if theme == "light":
            self.setStyleSheet("""
                QMainWindow { background-color: white; color: black; }
                QLabel { color: black; }
                QPushButton { background-color: lightgrey; color: black; border: none; padding: 5px; }
                QPushButton::hover { background-color: grey; color: white; }
                QListWidget { background-color: white; color: black; }
                QLineEdit { background-color: white; color: black; }
                QTextEdit { background-color: white; color: black; }
            """)
        elif theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #282828; color: white; }
                QLabel { color: white; }
                QPushButton { background-color: #505050; color: white; border: none; padding: 5px; }
                QPushButton::hover { background-color: #606060; color: white; }
                QListWidget { background-color: #383838; color: white; }
                QLineEdit { background-color: #383838; color: white; }
                QTextEdit { background-color: #383838; color: white; }
            """)

    def open_github(self):
        webbrowser.open("https://github.com/TheWilli67/YeGrec")

    def show_version(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def show_task_creation_dialog(self):
        dialog = TaskCreationWindow()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            task_details = dialog.get_task_details()
            self.tasks.append(task_details)
            self.update_tasks_list()

    def delete_task(self):
        selected_item = self.tasks_list.currentRow()
        if selected_item >= 0:
            del self.tasks[selected_item]
            self.update_tasks_list()

    def apply_filter(self, filter_type):
        if filter_type == "date":
        # Trier les tâches par date
            self.tasks.sort(key=lambda x: QtCore.QDateTime.fromString(x['date'], "yyyy-MM-dd HH:mm"))
        elif filter_type == "priority":
        # Trier les tâches par priorité (en supposant que 1 est la plus haute priorité)
            self.tasks.sort(key=lambda x: int(x['priority']))

        self.update_tasks_list()


# Point d'entrée principal
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec_())
