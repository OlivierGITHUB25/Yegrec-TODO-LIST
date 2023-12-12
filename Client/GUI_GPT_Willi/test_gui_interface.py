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
        self.name_input.setStyleSheet("background-color: black; border: 1px solid cyan; color: cyan;")
        
        # Description de la tâche
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Task Description")
        self.description_input.setStyleSheet("background-color: black; border: 1px solid cyan; color: cyan;")
        
        # Priorité de la tâche
        self.priority_input = QtWidgets.QComboBox()
        self.priority_input.addItems(["1", "2", "3"])
        self.priority_input.setStyleSheet("background-color: black; border: 1px solid cyan; color: cyan;")
        
        # Date de la tâche
        self.date_input = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.date_input.setStyleSheet("background-color: black; border: 1px solid cyan; color: cyan;")
        
        # Bouton pour ajouter la tâche
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.setStyleSheet("QPushButton {background-color: cyan; color: white;} QPushButton::hover {background-color: white; color: black;}")
        add_task_btn.clicked.connect(self.accept)
        
        # Ajout des widgets au layout
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

        # Bouton pour ajouter une nouvelle tâche
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.setStyleSheet("QPushButton {background-color: rgba(0,201,177,255); color: white;font-weight: bold;} QPushButton::hover {background-color: white; color: black;font-weight: bold;}")
        add_task_btn.clicked.connect(self.show_task_creation_dialog)

        # Bouton pour supprimer la tâche sélectionnée
        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.setStyleSheet("QPushButton {background-color: red; color: white;} QPushButton::hover {background-color: white; color: black;}")
        delete_button.clicked.connect(self.delete_task)

        # Menu déroulant pour le filtrage des tâches
        self.filter_options = QtWidgets.QComboBox()
        self.filter_options.addItem("Sort by Date")
        self.filter_options.addItem("Sort by Priority")
        self.filter_options.setStyleSheet("background-color: black; color: cyan; border: 1px solid cyan;")
        self.filter_options.currentIndexChanged.connect(self.apply_filter)

        # Liste des tâches
        self.tasks_list = QtWidgets.QListWidget()
        self.tasks_list.setStyleSheet("background-color: black; border: 1px solid cyan; color: cyan; padding: 5px;")

        # Ajouter les widgets au layout
        layout.addWidget(title)
        layout.addWidget(add_task_btn)
        layout.addWidget(self.filter_options)
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

    def apply_filter(self):
        sort_key = self.filter_options.currentText()
        if sort_key == "Sort by Date":
            self.tasks.sort(key=lambda x: x['date'])
        elif sort_key == "Sort by Priority":
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
