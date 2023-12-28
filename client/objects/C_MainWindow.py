import ssl
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from .C_Widgets import InfoBox, Question, CreateTask, CreateLabel, TaskDetails, ListUsers


class MainWindow(QtWidgets.QWidget):
    def __init__(self, tcp_session):
        super().__init__()
        self.dialog = None
        self.TCP_Session = tcp_session
        self.general_layout_grid = QtWidgets.QGridLayout()
        self.setLayout(self.general_layout_grid)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.general_layout_grid.addLayout(self.verticalLayout, 0, 0)
        self.tasks = self.get_tasks()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YeGrec's View")
        self.setGeometry(0, 0, 1000, 700)
        self.setWindowTitle("YeGrec's Todo List")
        self.setStyleSheet(self.css_loader('../client/styles/styles.css'))
        self.center_window()

        # Icons definition

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../client/assets/task.svg"))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../client/assets/tag.svg"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../client/assets/edit.svg"))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../client/assets/bin.svg"))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../client/assets/user.svg"))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../client/assets/disconnect.svg"))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../client/assets/sort.svg"))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("../client/assets/help.svg"))

        # Menu bar

        self.menubar = QtWidgets.QMenuBar()

        self.menu_file = QtWidgets.QMenu("File")
        self._action_create_task = QtWidgets.QAction("Create task")
        self._action_create_task.setIcon(icon1)
        self._action_create_task.triggered.connect(self.action_create_task)
        self._action_create_label = QtWidgets.QAction("Create label")
        self._action_create_label.setIcon(icon2)
        self._action_create_label.triggered.connect(self.action_create_label)
        self._action_edit_object = QtWidgets.QAction("Edit object")
        self._action_edit_object.setIcon(icon3)
        self._action_delete_object = QtWidgets.QAction("Delete object")
        self._action_delete_object.setIcon(icon4)
        self._action_list_users = QtWidgets.QAction("List users")
        self._action_list_users.setIcon(icon5)
        self._action_list_users.triggered.connect(self.action_list_users)
        self._action_quit = QtWidgets.QAction("Quit")
        self._action_quit.setIcon(icon6)
        self._action_quit.triggered.connect(self.closeEvent)

        self.menu_about = QtWidgets.QMenu("About")

        self.menubar.addMenu(self.menu_file)
        self.menu_file.addAction(self._action_create_task)
        self.menu_file.addAction(self._action_create_label)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self._action_edit_object)
        self.menu_file.addAction(self._action_delete_object)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self._action_list_users)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self._action_quit)

        self.menubar.addMenu(self.menu_about)

        self.general_layout_grid.setMenuBar(self.menubar)

        # First line (horizontal layout)

        horizontal_layout = QtWidgets.QHBoxLayout()

        create_task_button = QtWidgets.QPushButton()
        create_task_button.setIcon(icon1)
        create_task_button.setIconSize(QtCore.QSize(32, 32))
        create_task_button.clicked.connect(self.action_create_task)

        create_label_button = QtWidgets.QPushButton()
        create_label_button.setIcon(icon2)
        create_label_button.setIconSize(QtCore.QSize(32, 32))
        create_label_button.clicked.connect(self.action_create_label)

        edit_task_button = QtWidgets.QPushButton()
        edit_task_button.setIcon(icon3)
        edit_task_button.setIconSize(QtCore.QSize(32, 32))

        delete_task_button = QtWidgets.QPushButton()
        delete_task_button.setIcon(icon4)
        delete_task_button.setIconSize(QtCore.QSize(32, 32))

        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        list_user_button = QtWidgets.QPushButton()
        list_user_button.setIcon(icon5)
        list_user_button.setIconSize(QtCore.QSize(32, 32))
        list_user_button.clicked.connect(self.action_list_users)

        help_button = QtWidgets.QPushButton()
        help_button.setIcon(icon8)
        help_button.setIconSize(QtCore.QSize(32, 32))

        quit_button = QtWidgets.QPushButton()
        quit_button.setIcon(icon6)
        quit_button.setIconSize(QtCore.QSize(32, 32))
        quit_button.clicked.connect(self.closeEvent)

        # Second line (scroll area)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QtWidgets.QWidget(scroll_area)
        scroll_area.setWidget(content_widget)

        self.task_view_layout = QtWidgets.QVBoxLayout(content_widget)
        self.task_view_layout.setAlignment(QtCore.Qt.AlignTop)

        for task in self.tasks:
            self.task_view_layout.addWidget(self.add_tasks_to_scroll_area(
                task["task_id"],
                task["name"],
                str(task["state"]),
                str(task["priority"]),
                task["date"],
                task["description"])
            )

        # Third line (horizontal layout)

        horizontal_layout_2 = QtWidgets.QHBoxLayout()

        sort_button = QtWidgets.QPushButton()
        sort_button.setIcon(icon7)
        sort_button.setIconSize(QtCore.QSize(12, 12))

        sort_label = QtWidgets.QLabel("Sort by:")
        sort_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        date_label = QtWidgets.QLabel("Date")
        date_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        spacer_item_2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        annotation_label = QtWidgets.QLabel("YeGrec's list")
        annotation_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Layout definition

        horizontal_layout.addWidget(create_task_button)
        horizontal_layout.addWidget(create_label_button)
        horizontal_layout.addWidget(edit_task_button)
        horizontal_layout.addWidget(delete_task_button)
        horizontal_layout.addItem(spacer_item)
        horizontal_layout.addWidget(help_button)
        horizontal_layout.addWidget(list_user_button)
        horizontal_layout.addWidget(quit_button)

        horizontal_layout_2.addWidget(sort_button)
        horizontal_layout_2.addWidget(sort_label)
        horizontal_layout_2.addWidget(date_label)
        horizontal_layout_2.addItem(spacer_item_2)
        horizontal_layout_2.addWidget(annotation_label)

        self.verticalLayout.addLayout(horizontal_layout)
        self.verticalLayout.addWidget(scroll_area)
        self.verticalLayout.addLayout(horizontal_layout_2)

    def action_task_details(self, task_id, name, state, priority, date, description):
        self.dialog = TaskDetails(task_id, name, state, priority, date, description, self.TCP_Session)
        self.dialog.show()

    def action_create_task(self):
        dialog = CreateTask(self.TCP_Session)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            self.reload_tasks()

    def action_create_label(self):
        dialog = CreateLabel(self.TCP_Session)
        dialog.exec_()

    def action_list_users(self):
        self.dialog = ListUsers()
        self.dialog.show()

    def get_tasks(self):
        try:
            self.TCP_Session.send_data({
                "client": "get_tasks",
            })
            result = self.TCP_Session.get_data()["content"]
        except KeyError:
            return []
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()
        else:
            return result

    def reload_tasks(self):
        self.tasks = self.get_tasks()
        while self.task_view_layout.count():
            item = self.task_view_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for task in self.tasks:
            self.task_view_layout.addWidget(self.add_tasks_to_scroll_area(
                task["task_id"],
                task["name"],
                str(task["state"]),
                str(task["priority"]),
                task["date"],
                task["description"])
            )

    def add_tasks_to_scroll_area(self, task_id, name, state, priority, date, description):
        task_widget = QtWidgets.QWidget()
        task_widget.setFixedHeight(50)
        task_widget_layout = QtWidgets.QGridLayout()

        task_label = QtWidgets.QLabel(name)

        task_label_state = QtWidgets.QLabel("State:")
        task_label_state.setAlignment(QtCore.Qt.AlignRight)
        state_mapping = {1: "TODO", 2: "IN PROGRESS", 3: "FINISHED"}
        task_state = QtWidgets.QLabel(state_mapping.get(int(state), "Error"))

        task_label_priority = QtWidgets.QLabel("Priority:")
        task_label_priority.setAlignment(QtCore.Qt.AlignRight)
        priority_mapping = {1: "LOW", 2: "NORMAL", 3: "HIGH"}
        task_priority = QtWidgets.QLabel(priority_mapping.get(int(priority), "Error"))

        task_label_deadline = QtWidgets.QLabel("Deadline:")
        task_label_deadline.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        task_deadline = QtWidgets.QLabel(date)
        task_deadline.setAlignment(QtCore.Qt.AlignVCenter)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../client/assets/more.svg"))
        task_details_button = QtWidgets.QPushButton()
        task_details_button.setIcon(icon)
        task_details_button.setIconSize(QtCore.QSize(24, 24))
        task_details_button.setSizePolicy(size_policy)
        task_details_button.clicked.connect(
            lambda: self.action_task_details(task_id, name, state, priority, date, description)
        )

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../client/assets/edit.svg"))
        task_edit_button = QtWidgets.QPushButton()
        task_edit_button.setIcon(icon2)
        task_edit_button.setIconSize(QtCore.QSize(24, 24))
        task_edit_button.setSizePolicy(size_policy)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../client/assets/bin.svg"))
        task_delete_button = QtWidgets.QPushButton()
        task_delete_button.setIcon(icon2)
        task_delete_button.setIconSize(QtCore.QSize(24, 24))
        task_delete_button.setSizePolicy(size_policy)

        task_widget_layout.addWidget(task_label, 0, 0, 2, 1)
        task_widget_layout.addWidget(task_label_priority, 0, 1, 1, 1)
        task_widget_layout.addWidget(task_priority, 0, 2, 1, 1)
        task_widget_layout.addWidget(task_label_state, 1, 1, 1, 1)
        task_widget_layout.addWidget(task_state, 1, 2, 1, 1)
        task_widget_layout.addWidget(task_label_deadline, 0, 3, 2, 1)
        task_widget_layout.addWidget(task_deadline, 0, 4, 2, 1)
        task_widget_layout.addWidget(task_details_button, 0, 5, 2, 1)
        task_widget_layout.addWidget(task_edit_button, 0, 6, 2, 1)
        task_widget_layout.addWidget(task_delete_button, 0, 7, 2, 1)

        task_widget.setLayout(task_widget_layout)
        task_widget.setFixedHeight(50)
        task_widget.setObjectName("task")

        return task_widget

    def closeEvent(self, event, **kwargs):
        question = Question("Quit", "Are you sure you want to quit YeGrec ?")
        question = question.exec_()

        if question == QtWidgets.QMessageBox.Yes:
            try:
                self.TCP_Session.send_data({
                    "client": "DISCONNECT",
                })
                print(self.TCP_Session.get_data())
            except ssl.SSLEOFError:
                InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                if type(event) is not bool:
                    event.accept()
                else:
                    sys.exit()
        else:
            if type(event) is not bool:
                event.ignore()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def css_loader(filename):
        with open(filename, 'r') as rd:
            content = rd.read()
            rd.close()
        return content
