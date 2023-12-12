import sys
from PyQt5 import QtWidgets, QtGui, QtCore

# Fenêtre de dialogue pour la création de tâche
class TaskCreationWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Task")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("background-color: black; color: white;")
        self.init_ui()
    
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # Nom de la tâche
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Task Name")
        self.name_input.setStyleSheet("background-color: black; border: 1px solid rgba(0,201,177,255); color: rgba(0,201,177,255);")
        
        # Description de la tâche
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Task Description")
        self.description_input.setStyleSheet("background-color: black; border: 1px solid rgba(0,201,177,255); color: rgba(0,201,177,255);")
        
        # Priorité de la tâche
        self.priority_input = QtWidgets.QComboBox()
        self.priority_input.addItems(["1", "2", "3"])
        self.priority_input.setStyleSheet("background-color: black; border: 1px solid rgba(0,201,177,255); color: rgba(0,201,177,255);")
        
        # Date de la tâche
        self.date_input = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.date_input.setStyleSheet("background-color: black; border: 1px solid rgba(0,201,177,255); color: rgba(0,201,177,255);")
        
        # Bouton pour ajouter la tâche
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.setStyleSheet("QPushButton {background-color: rgba(0,201,177,255); color: white;} QPushButton::hover {background-color: white; color: black;}")
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
class TodoListApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ye'Grec")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: black; color: white;")

        layout = QtWidgets.QVBoxLayout()

        # Titre de la fenêtre
        title = QtWidgets.QLabel("Ye'Grec")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(QtGui.QFont('Arial', 24))
        title.setStyleSheet("color: rgba(0,201,177,255);")

        # Bouton pour ajouter une nouvelle tâche
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.setStyleSheet("QPushButton {background-color: rgba(0,201,177,255); color: white;} QPushButton::hover {background-color: white; color: black;}")
        add_task_btn.clicked.connect(self.show_task_creation_dialog)

        # Layout pour les boutons de tri
        sort_buttons_layout = QtWidgets.QHBoxLayout()

        # Bouton pour trier par date
        sort_date_btn = QtWidgets.QPushButton("Sort by Date")
        sort_date_btn.setStyleSheet("QPushButton {background-color: rgba(0,201,177,255); color: white;} QPushButton::hover {background-color: white; color: black;}")
        sort_date_btn.clicked.connect(lambda: self.apply_filter("date"))

        # Bouton pour trier par priorité
        sort_priority_btn = QtWidgets.QPushButton("Sort by Priority")
        sort_priority_btn.setStyleSheet("QPushButton {background-color: rgba(0,201,177,255); color: white;} QPushButton::hover {background-color: white; color: black;}")
        sort_priority_btn.clicked.connect(lambda: self.apply_filter("priority"))

        # Ajout des boutons de tri au layout horizontal
        sort_buttons_layout.addWidget(sort_date_btn)
        sort_buttons_layout.addWidget(sort_priority_btn)

        # Liste des tâches
        self.tasks_list = QtWidgets.QListWidget()
        self.tasks_list.setStyleSheet("background-color: black; border: 1px solid rgba(0,201,177,255); color: rgba(0,201,177,255); padding: 5px;")

        # Bouton pour supprimer la tâche sélectionnée
        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.setStyleSheet("QPushButton {background-color: red; color: white;} QPushButton::hover {background-color: white; color: black;}")
        delete_button.clicked.connect(self.delete_task)

        # Ajouter les widgets au layout
        layout.addWidget(title)
        layout.addWidget(add_task_btn)
        layout.addLayout(sort_buttons_layout)
        layout.addWidget(self.tasks_list)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def show_task_creation_dialog(self):
        dialog = TaskCreationWindow()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            task_details = dialog.get_task_details()
            self.tasks.append(task_details)
            self.apply_filter()

    def delete_task(self):
        selected_item = self.tasks_list.currentRow()
        if selected_item >= 0:
            del self.tasks[selected_item]
            self.apply_filter()

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
