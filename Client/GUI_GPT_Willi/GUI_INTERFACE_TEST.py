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

# Fenêtre de dialogue pour la création de tâche
class TaskCreationWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Task")
        self.setGeometry(100, 100, 300, 200)
        layout = QtWidgets.QVBoxLayout(self)
        
        # Nom de la tâche
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Task Name")
        
        # Description de la tâche
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Task Description")
        
        # Priorité de la tâche
        self.priority_input = QtWidgets.QComboBox()
        self.priority_input.addItems(["1", "2", "3"])
        
        # Date de la tâche
        self.date_input = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        
        # Bouton pour ajouter la tâche
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.clicked.connect(self.accept)
        
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.date_input)
        layout.addWidget(add_task_btn)

    def get_task_details(self):
        return {
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText(),
            'priority': self.priority_input.currentText(),
            'date': self.date_input.dateTime().toString("yyyy-MM-dd HH:mm")
        }

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

        # Bouton pour supprimer la tâche sélectionnée
        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.setObjectName("deleteButton")  # Set objectName for this button
        delete_button.clicked.connect(self.delete_task)


        # Ajouter les widgets au layout
        layout.addWidget(self.title)
        layout.addWidget(add_task_btn)
        layout.addLayout(sort_buttons_layout)
        layout.addWidget(self.tasks_list)
        layout.addWidget(delete_button)

        # Set the initial theme
        self.set_theme("dark")

    def set_theme(self, theme):
        if theme == "light":
            self.setStyleSheet("""
                QMainWindow { background-color: white; color: black; font-weight: bold; }
                QLabel { color: black; font-weight: bold; }
                QPushButton { background-color: rgba(0,201,177,255); color: white; border-radius:5%; padding: 5px 2px; font-weight: bold; }
                QPushButton::hover { background-color: grey; color: white; }
                QListWidget { background-color: white; color: black; font-weight: bold; }
                QLineEdit { background-color: white; color: black; font-weight: bold; }
                QTextEdit { background-color: white; color: black; font-weight: bold; }
                QPushButton#deleteButton { background-color: red; color: white; border-radius:5%; padding: 7px 2px; font-weight: bold; }
                QPushButton#deleteButton::hover { background-color: lightcoral; color: white; }
            """)
        elif theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: black; color: white; font-weight: bold; }
                QLabel { color: white; font-weight: bold; }
                QPushButton { background-color: rgba(0,201,177,255); color: white; border-radius:5%; padding: 5px 2px; font-weight: bold; }
                QPushButton::hover { background-color: grey; color: black; }
                QListWidget { background-color: black; color: white; font-weight: bold; }
                QLineEdit { background-color: black; color: white; font-weight: bold; }
                QTextEdit { background-color: black; color: white; font-weight: bold; }
                QPushButton#deleteButton { background-color: red; color: white; border-radius:5%; padding: 7px 2px; font-weight: bold; }
                QPushButton#deleteButton::hover { background-color: darkred; color: white; }
            """)

        # Apply styles to all buttons
        for button in self.findChildren(QtWidgets.QPushButton):
            button.setStyleSheet(self.styleSheet())


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
            self.tasks.sort(key=lambda x: x['date'])
        elif filter_type == "priority":
            self.tasks.sort(key=lambda x: x['priority'], reverse=True)
        self.update_tasks_list()

    def update_tasks_list(self):
        self.tasks_list.clear()
        for task in self.tasks:
            display_text = f"{task['name']} - Priority: {task['priority']} - Due: {task['date']} - {task['description']}"
            list_item = QtWidgets.QListWidgetItem(display_text)
            self.tasks_list.addItem(list_item)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec_())
