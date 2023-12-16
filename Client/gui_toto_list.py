import sys
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore

# Compteur global pour l'identifiant des tâches
task_id_counter = 0

def get_next_task_id():
    global task_id_counter
    task_id_counter += 1
    return task_id_counter

class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(100, 100, 200, 100)
        layout = QtWidgets.QVBoxLayout(self)
        version_label = QtWidgets.QLabel("Version 1.0", self)
        layout.addWidget(version_label)

class TaskCreationWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Task")
        self.setGeometry(100, 100, 300, 200)
        layout = QtWidgets.QVBoxLayout(self)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Task Name")
        layout.addWidget(self.name_input)

        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Task Description")
        layout.addWidget(self.description_input)

        self.priority_input = QtWidgets.QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        layout.addWidget(self.priority_input)

        self.date_input = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        layout.addWidget(self.date_input)

        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.clicked.connect(self.accept)
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

class SubTaskCreationWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Subtask")
        self.setGeometry(100, 100, 300, 150)
        layout = QtWidgets.QVBoxLayout(self)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Subtask Name")
        layout.addWidget(self.name_input)

        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Subtask Description")
        layout.addWidget(self.description_input)

        add_subtask_btn = QtWidgets.QPushButton("Add Subtask")
        add_subtask_btn.clicked.connect(self.accept)
        layout.addWidget(add_subtask_btn)

    def get_subtask_details(self):
        return {
            'id': get_next_task_id(),
            'name': self.name_input.text(),
            'description': self.description_input.toPlainText()
        }

class TodoListApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"  # Initialize current theme
        self.tasks = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ye'Grec Todo List")
        self.setGeometry(100, 100, 400, 600)

        # Menu Bar
        menu_bar = self.menuBar()
        option_menu = menu_bar.addMenu("&Options")
        help_menu = menu_bar.addMenu("&Help")

        # Theme Menu
        theme_menu = option_menu.addMenu("&Theme")
        light_theme_action = theme_menu.addAction("Light Theme")
        dark_theme_action = theme_menu.addAction("Dark Theme")
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))

        # Help Menu
        contact_action = help_menu.addAction("&Contact")
        version_action = help_menu.addAction("&Version")
        contact_action.triggered.connect(self.open_github)
        version_action.triggered.connect(self.show_version_dialog)

        # Central Widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Title Label
        self.title = QtWidgets.QLabel("Ye'Grec Todo List")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont('Arial', 24))
        layout.addWidget(self.title)

        # Task Buttons Layout
        add_task_btn = QtWidgets.QPushButton("Add Task")
        add_task_btn.clicked.connect(self.show_task_creation_dialog)
        layout.addWidget(add_task_btn)

        sort_buttons_layout = QtWidgets.QHBoxLayout()
        sort_date_btn = QtWidgets.QPushButton("Sort by Date")
        sort_date_btn.clicked.connect(lambda: self.apply_sorting("date"))
        sort_priority_btn = QtWidgets.QPushButton("Sort by Priority")
        sort_priority_btn.clicked.connect(lambda: self.apply_sorting("priority"))
        sort_buttons_layout.addWidget(sort_date_btn)
        sort_buttons_layout.addWidget(sort_priority_btn)
        layout.addLayout(sort_buttons_layout)

        # Tasks List Widget
        self.tasks_list = QtWidgets.QListWidget()
        layout.addWidget(self.tasks_list)

        # Delete Button
        delete_button = QtWidgets.QPushButton("Delete Selected Task")
        delete_button.clicked.connect(self.delete_task)
        layout.addWidget(delete_button)

        # Apply Dark Theme Initially
        self.set_theme("dark")

    def set_theme(self, theme):
        self.current_theme = theme  # Store the current theme
        # Set the stylesheet based on the theme
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
        self.update_tasks_list()

    def open_github(self):
        webbrowser.open("https://github.com/your-github-link")

    def show_version_dialog(self):
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
            item_data = self.tasks_list.item(selected_item).data(QtCore.Qt.UserRole)
            task_id, parent_task_id = item_data

            if parent_task_id is None:
                # Remove a main task
                self.tasks = [task for task in self.tasks if task['id'] != task_id]
            else:
                # Remove a subtask
                for task in self.tasks:
                    if task['id'] == parent_task_id:
                        task['subtasks'] = [subtask for subtask in task['subtasks'] if subtask['id'] != task_id]
                        break
            self.update_tasks_list()

    def update_tasks_list(self):
        self.tasks_list.clear()
        for task in self.tasks:
            self.add_task_to_list(task, is_subtask=False)
            for subtask in task['subtasks']:
                self.add_task_to_list(subtask, is_subtask=True, parent_task_id=task['id'])

    def add_task_to_list(self, task, is_subtask, parent_task_id=None):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)

        task_label = QtWidgets.QLabel()
        if is_subtask:
            label_text = f"    - {task['name']} : {task['description']}"
            task_label.setText(label_text)
            task_label.setStyleSheet(self.get_subtask_style())
        else:
            label_text = f"{task['name']} : {task['description']} | {task['date']}"
            task_label.setText(label_text)
        layout.addWidget(task_label)

        if not is_subtask:
            add_subtask_btn = QtWidgets.QPushButton("+")
            add_subtask_btn.setFixedSize(30, 30)
            add_subtask_btn.clicked.connect(lambda: self.add_subtask(task))
            add_subtask_btn.setStyleSheet(self.get_button_style(self.current_theme))
            layout.addWidget(add_subtask_btn)

        list_item = QtWidgets.QListWidgetItem(self.tasks_list)
        list_item.setData(QtCore.Qt.UserRole, (task['id'], parent_task_id))
        list_item.setSizeHint(widget.sizeHint())
        self.tasks_list.addItem(list_item)
        self.tasks_list.setItemWidget(list_item, widget)

    def get_subtask_style(self):
        if self.current_theme == "dark":
            return "background-color: #383838; color: white; padding-left: 5px;"
        else:
            return "background-color: white; color: black; padding-left: 5px;"

    def get_button_style(self, theme):
        if theme == "light":
            return """
                QPushButton { 
                    background-color: lightgrey; 
                    color: black; 
                    border: none; 
                    border-radius: 15px; 
                }
                QPushButton::hover { 
                    background-color: grey; 
                    color: white; 
                }
            """
        else:
            return """
                QPushButton { 
                    background-color: #505050; 
                    color: white; 
                    border: none; 
                    border-radius: 15px; 
                }
                QPushButton::hover { 
                    background-color: #606060; 
                    color: white; 
                }
            """

    def apply_sorting(self, sort_key):
        if sort_key == "date":
            self.tasks.sort(key=lambda x: x['date'])
        elif sort_key == "priority":
            self.tasks.sort(key=lambda x: x['priority'])
        self.update_tasks_list()

# Point d'entrée principal
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec_())
