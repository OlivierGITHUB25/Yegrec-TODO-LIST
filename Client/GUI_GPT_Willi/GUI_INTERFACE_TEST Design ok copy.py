import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore

# Compteur global pour l'identifiant des tâches
task_id_counter = 0


def get_next_task_id():
    global task_id_counter
    task_id_counter += 1
    return task_id_counter

# Fenêtre de dialogue pour la version


class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Version")
        self.setGeometry(100, 100, 200, 100)
        layout = QtWidgets.QVBoxLayout(self)
        version_label = QtWidgets.QLabel("Version 1.0", self)
        layout.addWidget(version_label)

# Fenêtre de dialogue pour la création de tâche


class TaskCreationWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Task")
        self.setGeometry(100, 100, 300, 200)
        layout = QtWidgets.QVBoxLayout(self)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Task Name")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Task Description")
        self.priority_input = QtWidgets.QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.date_input = QtWidgets.QDateTimeEdit(
            QtCore.QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.clicked.connect(self.accept)

        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.date_input)
        layout.addWidget(add_task_btn)

    def get_task_details(self):
        return {
            'id': get_next_task_id(),
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText(),
            'priority': self.priority_input.currentText(),
            'date': self.date_input.dateTime().toString("yyyy-MM-dd HH:mm"),
            'subtasks': []
        }

# Fenêtre de dialogue pour la création de sous-tâche


class SubTaskCreationWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Subtask")
        self.setGeometry(100, 100, 300, 150)
        layout = QtWidgets.QVBoxLayout(self)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Subtask Name")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Subtask Description")
        add_subtask_btn = QtWidgets.QPushButton("Add Subtask")
        add_subtask_btn.clicked.connect(self.accept)

        layout.addWidget(self.name_input)
        layout.addWidget(self.description_input)
        layout.addWidget(add_subtask_btn)

    def get_subtask_details(self):
        return {
            'id': get_next_task_id(),
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText()
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

        menu_bar = self.menuBar()
        option_menu = menu_bar.addMenu("&Options")
        help_menu = menu_bar.addMenu("&Help")

        theme_menu = option_menu.addMenu("&Theme")
        light_theme_action = theme_menu.addAction("Light Theme")
        dark_theme_action = theme_menu.addAction("Dark Theme")
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))

        contact_action = help_menu.addAction("&Contact")
        version_action = help_menu.addAction("&Version")
        contact_action.triggered.connect(self.open_github)
        version_action.triggered.connect(self.show_version)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.title = QtWidgets.QLabel("Ye'Grec")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont('Arial', 24))

        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.clicked.connect(self.show_task_creation_dialog)

        sort_buttons_layout = QtWidgets.QHBoxLayout()
        sort_date_btn = QtWidgets.QPushButton("Sort by Date")
        sort_date_btn.clicked.connect(lambda: self.apply_filter("date"))
        sort_priority_btn = QtWidgets.QPushButton("Sort by Priority")
        sort_priority_btn.clicked.connect(
            lambda: self.apply_filter("priority"))
        sort_buttons_layout.addWidget(sort_date_btn)
        sort_buttons_layout.addWidget(sort_priority_btn)

        self.tasks_list = QtWidgets.QListWidget()

        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.clicked.connect(self.delete_task)

        layout.addWidget(self.title)
        layout.addWidget(add_task_btn)
        layout.addLayout(sort_buttons_layout)
        layout.addWidget(self.tasks_list)
        layout.addWidget(delete_button)

        self.set_theme("dark")

    def set_theme(self, theme):
        if theme == "light":
            self.setStyleSheet("""
                QMainWindow { background-color: white; color: black; }
                QLabel { color: black; }
                QPushButton { 
                    background-color: lightgrey; 
                    color: black; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 10px;
                }
                QPushButton::hover { 
                    background-color: grey; 
                    color: white; 
                }
                QListWidget { background-color: white; color: black; }
                QLineEdit { background-color: white; color: black; }
                QTextEdit { background-color: white; color: black; }
            """)
        elif theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #282828; color: white; }
                QLabel { color: white; }
                QPushButton { 
                    background-color: #505050; 
                    color: white; 
                    border: none; 
                    padding: 5px; 
                    border-radius: 10px;
                }
                QPushButton::hover { 
                    background-color: #606060; 
                    color: white; 
                }
                QListWidget { background-color: #383838; color: white; }
                QLineEdit { background-color: #383838; color: white; }
                QTextEdit { background-color: #383838; color: white; }
            """)

    def open_github(self):
        webbrowser.open("https://github.com/your-github-link")

    def show_version(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def show_task_creation_dialog(self):
        dialog = TaskCreationWindow()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            task_details = dialog.get_task_details()
            self.tasks.append(task_details)
            self.update_tasks_list()

    def add_subtask(self, task):
        dialog = SubTaskCreationWindow()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            subtask_details = dialog.get_subtask_details()
            task['subtasks'].append(subtask_details)
            self.update_tasks_list()

    def delete_task(self):
        selected_item = self.tasks_list.currentRow()
        if selected_item >= 0:
            item_data = self.tasks_list.item(
                selected_item).data(QtCore.Qt.UserRole)
            task_id, parent_task_id = item_data

            if parent_task_id is None:
                # Suppression d'une tâche principale
                self.tasks = [
                    task for task in self.tasks if task['id'] != task_id]
            else:
                # Suppression d'une sous-tâche
                for task in self.tasks:
                    if task['id'] == parent_task_id:
                        task['subtasks'] = [
                            subtask for subtask in task['subtasks'] if subtask['id'] != task_id]
                        break

            self.update_tasks_list()

    def update_tasks_list(self):
        self.tasks_list.clear()
        for task in self.tasks:
            self.add_task_to_list(task, is_subtask=False)
            for subtask in task['subtasks']:
                self.add_task_to_list(
                    subtask, is_subtask=True, parent_task_id=task['id'])

    def add_task_to_list(self, task, is_subtask, parent_task_id=None):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        # Formatage du texte de la tâche ou de la sous-tâche
        if is_subtask:
            label_text = f"    - {task['name']} : {task['description']}"
            task_label = QtWidgets.QLabel(label_text)
            # Style pour les sous-tâches
            task_label.setStyleSheet("background-color: #f0f0f0;")
        else:
            label_text = f"{task['name']} : {task['description']} | {task['date']}"
            task_label = QtWidgets.QLabel(label_text)

        layout.addWidget(task_label)

        if not is_subtask:
            add_subtask_btn = QtWidgets.QPushButton("+")
            add_subtask_btn.clicked.connect(lambda: self.add_subtask(task))
            layout.addWidget(add_subtask_btn)

        list_item = QtWidgets.QListWidgetItem(self.tasks_list)
        list_item.setData(QtCore.Qt.UserRole, (task['id'], parent_task_id))

        # Réduire la hauteur du QListWidgetItem
        list_item.setSizeHint(QtCore.QSize(0, 40))

        self.tasks_list.addItem(list_item)
        self.tasks_list.setItemWidget(list_item, widget)

    def apply_filter(self, filter_type):
        if filter_type == "date":
            self.tasks.sort(key=lambda x: x['date'])
        elif filter_type == "priority":
            self.tasks.sort(key=lambda x: x['priority'])
        self.update_tasks_list()


# Point d'entrée principal
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec_())
