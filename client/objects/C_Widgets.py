import ssl
import sys

from PyQt5 import QtWidgets, QtCore, QtGui


def css_loader(filename):
    with open(filename, 'r') as rd:
        content = rd.read()
        rd.close()
    return content


class InfoBox(QtWidgets.QMessageBox):
    def __init__(self, message: str, event_type: QtWidgets.QMessageBox.Icon):
        super().__init__()
        self.setText(message)
        self.setWindowTitle("Information")
        self.setIcon(event_type)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.exec_()


class Question(QtWidgets.QMessageBox):
    def __init__(self, title, message):
        super().__init__()
        self.setText(message)
        self.setWindowTitle(title)
        self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setDefaultButton(QtWidgets.QMessageBox.No)
        self.setIcon(QtWidgets.QMessageBox.Icon.Question)
        self.setStyleSheet(css_loader('../client/styles/styles.css'))


class TaskDetails(QtWidgets.QWidget):
    def __init__(self, task_id, name, state, priority, date, description, labels_id, TCP_Session):
        super().__init__()
        self.scroll_area_layout = None
        self.task_id = task_id
        self.name = name
        self.state = state
        self.priority = priority
        self.date = date
        self.description = description
        self.labels_id = labels_id
        self.TCP_Session = TCP_Session
        self.subtasks = self.get_subtasks()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("Task detail")
        self.setGeometry(0, 0, 1300, 800)
        self.center_window()

        task_name_label = QtWidgets.QLabel("Task name")
        task_name_label.setProperty("class", "title")
        task_name = QtWidgets.QLabel(self.name)
        task_name.setProperty("class", "content")

        task_state_label = QtWidgets.QLabel("State")
        task_state_label.setProperty("class", "title")
        state_mapping = {1: "TODO", 2: "IN PROGRESS", 3: "FINISHED"}
        task_state = QtWidgets.QLabel(state_mapping.get(int(self.state), "Error"))
        task_state.setProperty("class", "content")

        task_priority_label = QtWidgets.QLabel("Priority")
        task_priority_label.setProperty("class", "title")
        priority_mapping = {1: "LOW", 2: "NORMAL", 3: "HIGH"}
        task_priority = QtWidgets.QLabel(priority_mapping.get(int(self.priority), "Error"))
        task_priority.setProperty("class", "content")

        task_date_label = QtWidgets.QLabel("Deadline")
        task_date_label.setProperty("class", "title")
        task_date = QtWidgets.QLabel(self.date)
        task_date.setProperty("class", "content")

        task_description_label = QtWidgets.QLabel("Description")
        task_description_label.setProperty("class", "title")
        task_description = QtWidgets.QTextEdit()
        task_description.setPlainText(self.description)
        task_description.setReadOnly(True)
        task_description.setProperty("class", "content")

        #########################

        task_labels_label = QtWidgets.QLabel("Labels")
        task_labels_label.setProperty("class", "title")
        task_labels = LabelContainer(self.task_id, self.TCP_Session)

        #########################

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(task_name_label)
        left_layout.addWidget(task_name)
        left_layout.addWidget(task_state_label)
        left_layout.addWidget(task_state)
        left_layout.addWidget(task_priority_label)
        left_layout.addWidget(task_priority)
        left_layout.addWidget(task_date_label)
        left_layout.addWidget(task_date)
        left_layout.addWidget(task_labels_label)
        left_layout.addWidget(task_labels)
        left_layout.addWidget(task_description_label)
        left_layout.addWidget(task_description)

        left_layout.setAlignment(QtCore.Qt.AlignTop)

        #######################

        subtask_label = QtWidgets.QLabel("Subtasks")
        subtask_label.setProperty("class", "title")

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../client/assets/task.svg"))
        subtask_button = QtWidgets.QPushButton()
        subtask_button.setIconSize(QtCore.QSize(24, 24))
        subtask_button.setSizePolicy(size_policy)
        subtask_button.setIcon(icon1)
        subtask_button.clicked.connect(self.action_create_subtask)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QtWidgets.QWidget(scroll_area)
        scroll_area.setWidget(content_widget)

        self.scroll_area_layout = QtWidgets.QVBoxLayout(content_widget)
        self.scroll_area_layout.setAlignment(QtCore.Qt.AlignTop)

        for subtask in self.subtasks:
            self.scroll_area_layout.addWidget(self.add_subtasks_to_scroll_area(
                subtask["subtask_id"],
                subtask["name"],
                str(subtask["state"]),
                subtask["date"])
            )

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(subtask_label)
        top_layout.addWidget(subtask_button)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setAlignment(QtCore.Qt.AlignTop)
        right_layout.addLayout(top_layout)
        right_layout.addWidget(scroll_area)

        #######################

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addLayout(left_layout)
        horizontal_layout.addLayout(right_layout)

        self.setLayout(horizontal_layout)

    def add_subtasks_to_scroll_area(self, subtask_id, name, state, date):
        task_widget = QtWidgets.QWidget()
        task_widget.setFixedHeight(50)
        widget_layout = QtWidgets.QHBoxLayout()

        task_label = QtWidgets.QLabel(name)

        task_label_state = QtWidgets.QLabel("State:")
        task_label_state.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        state_mapping = {1: "TODO", 2: "IN PROGRESS", 3: "FINISHED"}
        task_state = QtWidgets.QLabel(state_mapping.get(int(state), "Error"))

        task_label_deadline = QtWidgets.QLabel("Deadline:")
        task_label_deadline.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        task_deadline = QtWidgets.QLabel(date)
        task_deadline.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../client/assets/edit.svg"))
        subtask_edit_button = QtWidgets.QPushButton()
        subtask_edit_button.setIcon(icon2)
        subtask_edit_button.setIconSize(QtCore.QSize(24, 24))
        subtask_edit_button.setSizePolicy(size_policy)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../client/assets/bin.svg"))
        subtask_delete_button = QtWidgets.QPushButton()
        subtask_delete_button.setIcon(icon2)
        subtask_delete_button.setIconSize(QtCore.QSize(24, 24))
        subtask_delete_button.setSizePolicy(size_policy)
        subtask_delete_button.clicked.connect(lambda : self.delete_subtask(subtask_id))

        widget_layout.addWidget(task_label)
        widget_layout.addWidget(task_label_state)
        widget_layout.addWidget(task_state)
        widget_layout.addWidget(task_label_deadline)
        widget_layout.addWidget(task_deadline)
        widget_layout.addWidget(subtask_edit_button)
        widget_layout.addWidget(subtask_delete_button)

        task_widget.setLayout(widget_layout)
        task_widget.setFixedHeight(50)
        task_widget.setObjectName("task")

        return task_widget

    def action_create_subtask(self):
        dialog = CreateSubTask(self.task_id, self.TCP_Session)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            self.reload_subtasks()

    def get_subtasks(self):
        try:
            self.TCP_Session.send_data({
                "client": "get_subtasks",
                "task_id": self.task_id
            })
            result = self.TCP_Session.get_data()["content"]
        except KeyError:
            return []
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()
        else:
            return result

    def delete_subtask(self, subtask_id):
        try:
            self.TCP_Session.send_data({
                "client": "delete_subtask",
                "subtask_id": subtask_id
            })
            result = self.TCP_Session.get_data()["success"]
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()
        else:
            if result == "yes":
                self.reload_subtasks()
            else:
                InfoBox("Internal error", QtWidgets.QMessageBox.Icon.Critical)

    def reload_subtasks(self):
        self.subtasks = self.get_subtasks()
        while self.scroll_area_layout.count():
            item = self.scroll_area_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for subtask in self.subtasks:
            self.scroll_area_layout.addWidget(self.add_subtasks_to_scroll_area(
                subtask["subtask_id"],
                subtask["name"],
                str(subtask["state"]),
                subtask["date"])
            )

    def center_window(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class CreateTask(QtWidgets.QDialog):
    def __init__(self, TCP_Session):
        super().__init__()
        self.description_plaintext = None
        self.date_date_edit = None
        self.priority_combobox = None
        self.state_combobox = None
        self.name_line_edit = None
        self.TCP_Session = TCP_Session
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(400)
        self.setWindowTitle("Create task")
        self.setStyleSheet(css_loader('../client/styles/styles.css'))

        task_label = QtWidgets.QLabel("Task name")
        self.name_line_edit = QtWidgets.QLineEdit()

        state_label = QtWidgets.QLabel("State")
        self.state_combobox = QtWidgets.QComboBox()
        self.state_combobox.addItems(["TODO", "IN PROGRESS", "FINISHED"])

        priority_label = QtWidgets.QLabel("Priority")
        self.priority_combobox = QtWidgets.QComboBox()
        self.priority_combobox.addItems(["LOW", "NORMAL", "HIGH"])

        date_label = QtWidgets.QLabel("Date")
        self.date_date_edit = QtWidgets.QDateTimeEdit()
        self.date_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        description_label = QtWidgets.QLabel("Description")
        self.description_plaintext = QtWidgets.QPlainTextEdit()

        ok_button = QtWidgets.QPushButton("Validate")
        cancel_button = QtWidgets.QPushButton("Cancel")

        self.layout.addWidget(task_label)
        self.layout.addWidget(self.name_line_edit)
        self.layout.addWidget(state_label)
        self.layout.addWidget(self.state_combobox)
        self.layout.addWidget(priority_label)
        self.layout.addWidget(self.priority_combobox)
        self.layout.addWidget(date_label)
        self.layout.addWidget(self.date_date_edit)
        self.layout.addWidget(description_label)
        self.layout.addWidget(self.description_plaintext)
        self.layout.addWidget(ok_button)
        self.layout.addWidget(cancel_button)

        ok_button.clicked.connect(self.api_send_data)
        cancel_button.clicked.connect(self.reject)

    def api_send_data(self):
        task_name = self.name_line_edit.text()
        task_state = self.state_combobox.currentText()
        state_mapping = {"TODO": 1, "IN PROGRESS": 2, "FINISHED": 3}
        task_state = state_mapping.get(task_state)
        task_priority = self.priority_combobox.currentText()
        priority_mapping = {"LOW": 1, "NORMAL": 2, "HIGH": 3}
        task_priority = priority_mapping.get(task_priority)
        task_date = self.date_date_edit.text()
        task_description = self.description_plaintext.toPlainText()

        if task_name == "" or task_state == "" or task_priority == "" or task_date == "" or task_description == "":
            return InfoBox("One or many field are blank", QtWidgets.QMessageBox.Icon.Warning)

        try:
            self.TCP_Session.send_data({
                "client": "create_task",
                "name": task_name,
                "state": task_state,
                "priority": task_priority,
                "date": task_date,
                "description": task_description,
                "labels_id": [],
                "users_id": []
            })
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

        result = self.TCP_Session.get_data()

        if result["success"] == "yes":
            InfoBox("Success", QtWidgets.QMessageBox.Icon.Information)
            self.accept()
        else:
            if result["error"] == "InvalidJSONFormat" or result["error"] == "ValueError":
                InfoBox("Value Error", QtWidgets.QMessageBox.Icon.Critical)
            elif result["error"] == "InternalError":
                InfoBox("Internal Error", QtWidgets.QMessageBox.Icon.Critical)
            elif result["error"] == "NotAuthorized":
                InfoBox("NotAuthorized", QtWidgets.QMessageBox.Icon.Critical)
            self.reject()


class CreateSubTask(QtWidgets.QDialog):
    def __init__(self, task_id, TCP_Session):
        super().__init__()
        self.description_plaintext = None
        self.date_date_edit = None
        self.priority_combobox = None
        self.state_combobox = None
        self.name_line_edit = None
        self.task_id = task_id
        self.TCP_Session = TCP_Session
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        self.setFixedWidth(400)
        self.setWindowTitle("Create subtask")
        self.setStyleSheet(css_loader('../client/styles/styles.css'))

        task_label = QtWidgets.QLabel("Subtask name")
        self.name_line_edit = QtWidgets.QLineEdit()

        state_label = QtWidgets.QLabel("State")
        self.state_combobox = QtWidgets.QComboBox()
        self.state_combobox.addItems(["TODO", "IN PROGRESS", "FINISHED"])

        date_label = QtWidgets.QLabel("Date")
        self.date_date_edit = QtWidgets.QDateTimeEdit()
        self.date_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        ok_button = QtWidgets.QPushButton("Validate")
        cancel_button = QtWidgets.QPushButton("Cancel")

        self.layout.addWidget(task_label)
        self.layout.addWidget(self.name_line_edit)
        self.layout.addWidget(state_label)
        self.layout.addWidget(self.state_combobox)
        self.layout.addWidget(date_label)
        self.layout.addWidget(self.date_date_edit)
        self.layout.addWidget(ok_button)
        self.layout.addWidget(cancel_button)

        ok_button.clicked.connect(self.api_send_data)
        cancel_button.clicked.connect(self.reject)

    def api_send_data(self):
        subtask_name = self.name_line_edit.text()
        subtask_state = self.state_combobox.currentText()
        state_mapping = {"TODO": 1, "IN PROGRESS": 2, "FINISHED": 3}
        subtask_state = state_mapping.get(subtask_state)
        subtask_date = self.date_date_edit.text()
        task_id = self.task_id

        if subtask_name == "" or subtask_state == "" or subtask_date == "":
            return InfoBox("One or many field are blank", QtWidgets.QMessageBox.Icon.Warning)

        try:
            self.TCP_Session.send_data({
                "client": "create_subtask",
                "name": subtask_name,
                "state": subtask_state,
                "date": subtask_date,
                "task_id": task_id,
                "labels_id": []
            })
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

        result = self.TCP_Session.get_data()

        if result["success"] == "yes":
            InfoBox("Success", QtWidgets.QMessageBox.Icon.Information)
            self.accept()
        else:
            if result["error"] == "InvalidJSONFormat" or result["error"] == "ValueError":
                InfoBox("Value Error", QtWidgets.QMessageBox.Icon.Critical)
            elif result["error"] == "InternalError":
                InfoBox("Internal Error", QtWidgets.QMessageBox.Icon.Critical)
            elif result["error"] == "NotAuthorized":
                InfoBox("NotAuthorized", QtWidgets.QMessageBox.Icon.Critical)
            self.reject()


class CreateLabel(QtWidgets.QDialog):
    def __init__(self, TCP_Session):
        super().__init__()
        self.label_line_edit = None
        self.color_line_edit = None
        self.TCP_Session = TCP_Session
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("Create label")
        self.setFixedWidth(300)

        label_label = QtWidgets.QLabel("Label name")
        self.label_line_edit = QtWidgets.QLineEdit()

        color_layout = QtWidgets.QHBoxLayout()

        color_label = QtWidgets.QLabel("Color (hex)")
        self.color_line_edit = QtWidgets.QLineEdit()
        color_btn = QtWidgets.QPushButton("Pick color")
        color_btn.clicked.connect(self.show_color_widget)

        color_layout.addWidget(self.color_line_edit)
        color_layout.addWidget(color_btn)

        ok_button = QtWidgets.QPushButton("Validate")
        cancel_button = QtWidgets.QPushButton("Cancel")

        self.layout.addWidget(label_label)
        self.layout.addWidget(self.label_line_edit)
        self.layout.addWidget(color_label)
        self.layout.addLayout(color_layout)
        self.layout.addWidget(ok_button)
        self.layout.addWidget(cancel_button)

        ok_button.clicked.connect(self.api_send_data)
        cancel_button.clicked.connect(self.reject)

    def show_color_widget(self):
        color = QtWidgets.QColorDialog.getColor()
        self.color_line_edit.setText(color.name())

    def api_send_data(self):
        label_name = self.label_line_edit.text()
        label_color = self.color_line_edit.text()

        if label_name == "" or label_color == "":
            return InfoBox("One or many field are blank", QtWidgets.QMessageBox.Icon.Warning)

        try:
            self.TCP_Session.send_data({
                "client": "create_label",
                "name": label_name,
                "color": label_color,
            })
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

        result = self.TCP_Session.get_data()

        if result["success"] == "yes":
            InfoBox("Success", QtWidgets.QMessageBox.Icon.Information)
            self.accept()
        else:
            if result["error"] == "InvalidJSONFormat" or result["error"] == "ValueError":
                InfoBox("Value Error", QtWidgets.QMessageBox.Icon.Critical)
            elif result["error"] == "InternalError":
                InfoBox("Internal Error", QtWidgets.QMessageBox.Icon.Critical)
            elif result["error"] == "NotAuthorized":
                InfoBox("NotAuthorized", QtWidgets.QMessageBox.Icon.Critical)
                self.reject()


class ListUsers(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("User list")
        self.setGeometry(0, 0, 400, 600)
        self.center_window()
        # TODO

    def center_window(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class LabelContainer(QtWidgets.QWidget):
    def __init__(self, task_id, TCP_Session):
        super().__init__()
        self.task_id = task_id
        self.TCP_Session = TCP_Session

        self.tag_container = QtWidgets.QWidget()
        self.tag_global_layout = QtWidgets.QVBoxLayout(self.tag_container)
        self.tag_global_layout.setContentsMargins(0, 0, 0, 0)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tag_container)

        self.get_labels()

    def add_labels(self, labels_list = []):
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        tag_label = QtWidgets.QLabel()
        tag_label.setProperty("class", "test")
        tag_label.setSizePolicy(size_policy)

        layout_list = []

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.tag_global_layout.addLayout(h_layout)

        if not labels_list:
            self.tag_global_layout.addWidget(QtWidgets.QLabel("No labels"))
        else:
            for i in labels_list:
                tag_label = QtWidgets.QLabel()
                tag_label.setProperty("class", "labels")
                tag_label.setSizePolicy(size_policy)
                tag_label.setText(i[1])
                tag_label.setStyleSheet(f"background-color: {i[2]};")

                if h_layout.count() < 4:
                    h_layout.addWidget(tag_label)
                else:
                    layout_list.append(h_layout)
                    h_layout = QtWidgets.QHBoxLayout()
                    h_layout.setAlignment(QtCore.Qt.AlignLeft)
                    self.tag_global_layout.addLayout(h_layout)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.setAlignment(QtCore.Qt.AlignLeft)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../client/assets/tag.svg"))
        add_label_button = QtWidgets.QPushButton()
        add_label_button.setIcon(icon)
        add_label_button.setIconSize(QtCore.QSize(24, 24))
        add_label_button.setSizePolicy(size_policy)

        h_layout.addWidget(add_label_button)
        self.tag_global_layout.addLayout(h_layout)

    def get_labels(self):
        try:
            self.TCP_Session.send_data({
                "client": "get_labels_for_a_task",
                "task_id": self.task_id
            })
            result = self.TCP_Session.get_data()["content"]
        except KeyError:
            self.add_labels()
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()
        else:
            self.add_labels(result)
