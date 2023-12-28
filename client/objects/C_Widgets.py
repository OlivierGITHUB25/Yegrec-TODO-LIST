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
        self.exec_()


class CreateTask(QtWidgets.QDialog):
    def __init__(self, TCP_Session):
        super().__init__()
        self.TCP_Session = TCP_Session

        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("Create task")
        self.setFixedWidth(400)

        self.label1 = QtWidgets.QLabel("Task name")
        self.name_lineedit = QtWidgets.QLineEdit()

        self.label2 = QtWidgets.QLabel("State")
        self.state_cmbobox = QtWidgets.QComboBox()
        self.state_cmbobox.addItems(["TODO", "IN PROGRESS", "FINISHED"])

        self.label3 = QtWidgets.QLabel("Priority")
        self.priority_cmbobox = QtWidgets.QComboBox()
        self.priority_cmbobox.addItems(["LOW", "NORMAL", "HIGH"])

        self.label4 = QtWidgets.QLabel("Date")
        self.date_dateedit = QtWidgets.QDateTimeEdit()
        self.date_dateedit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.label5 = QtWidgets.QLabel("Description")
        self.description_plaintext = QtWidgets.QPlainTextEdit()

        self.ok_button = QtWidgets.QPushButton("Validate")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.name_lineedit)
        layout.addWidget(self.label2)
        layout.addWidget(self.state_cmbobox)
        layout.addWidget(self.label3)
        layout.addWidget(self.priority_cmbobox)
        layout.addWidget(self.label4)
        layout.addWidget(self.date_dateedit)
        layout.addWidget(self.label5)
        layout.addWidget(self.description_plaintext)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.api_send_data)
        self.cancel_button.clicked.connect(self.reject)

    def api_send_data(self):
        task_name = self.name_lineedit.text()
        task_state = self.state_cmbobox.currentText()
        state_mapping = {"TODO": 1, "IN PROGRESS": 2, "FINISHED": 3}
        task_state = state_mapping.get(task_state)
        task_priority = self.priority_cmbobox.currentText()
        priority_mapping = {"LOW": 1, "NORMAL": 2, "HIGH": 3}
        task_priority = priority_mapping.get(task_priority)
        task_date = self.date_dateedit.text()
        task_description = self.description_plaintext.toPlainText()

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

        if self.TCP_Session.get_data()["success"] == "yes":
            self.accept()
        else:
            InfoBox("Value Error", QtWidgets.QMessageBox.Icon.Critical)


class CreateLabel(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("Create label")
        self.setFixedWidth(300)

        self.label1 = QtWidgets.QLabel("Label name")
        self.edit1 = QtWidgets.QLineEdit()

        self.color_layout = QtWidgets.QHBoxLayout()

        self.label2 = QtWidgets.QLabel("Color (hex)")
        self.edit2 = QtWidgets.QLineEdit()
        self.color_btn = QtWidgets.QPushButton("Pick color")
        self.color_btn.clicked.connect(self.show_color_widget)

        self.color_layout.addWidget(self.edit2)
        self.color_layout.addWidget(self.color_btn)

        self.ok_button = QtWidgets.QPushButton("Validate")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.edit1)
        layout.addWidget(self.label2)
        layout.addLayout(self.color_layout)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def show_color_widget(self):
        color = QtWidgets.QColorDialog.getColor()
        self.edit2.setText(color.name())


class TaskDetails(QtWidgets.QWidget):
    def __init__(self, task_id, name, state, priority, date, description, TCP_Session):
        super().__init__()
        self.task_id = task_id
        self.name = name
        self.state = state
        self.priority = priority
        self.date = date
        self.description = description
        self.TCP_Session = TCP_Session
        self.subtasks = self.api_get_subtasks()
        self.initUi()

    def initUi(self):
        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("Task detail")
        self.setGeometry(100, 100, 1000, 600)

        self.task_name_label = QtWidgets.QLabel("Task name")
        self.task_name_label.setProperty("class", "title")
        self.task_name = QtWidgets.QLabel(self.name)
        self.task_name.setProperty("class", "content")

        self.task_state_label = QtWidgets.QLabel("State")
        self.task_state_label.setProperty("class", "title")
        state_mapping = {1: "TODO", 2: "IN PROGRESS", 3: "FINISHED"}
        self.task_state = QtWidgets.QLabel(state_mapping.get(int(self.state), "Error"))
        self.task_state.setProperty("class", "content")

        self.task_priority_label = QtWidgets.QLabel("Priority")
        self.task_priority_label.setProperty("class", "title")
        priority_mapping = {1: "LOW", 2: "NORMAL", 3: "HIGH"}
        self.task_priority = QtWidgets.QLabel(priority_mapping.get(int(self.state), "Error"))
        self.task_priority.setProperty("class", "content")

        self.task_date_label = QtWidgets.QLabel("Deadline")
        self.task_date_label.setProperty("class", "title")
        self.task_date = QtWidgets.QLabel(self.date)
        self.task_date.setProperty("class", "content")

        self.task_description_label = QtWidgets.QLabel("Description")
        self.task_description_label.setProperty("class", "title")
        self.task_description = QtWidgets.QTextEdit()
        self.task_description.setPlainText(self.description)
        self.task_description.setReadOnly(True)
        self.task_description.setProperty("class", "content")

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.task_name_label)
        left_layout.addWidget(self.task_name)
        left_layout.addWidget(self.task_state_label)
        left_layout.addWidget(self.task_state)
        left_layout.addWidget(self.task_priority_label)
        left_layout.addWidget(self.task_priority)
        left_layout.addWidget(self.task_date_label)
        left_layout.addWidget(self.task_date)
        left_layout.addWidget(self.task_description_label)
        left_layout.addWidget(self.task_description)

        left_layout.setAlignment(QtCore.Qt.AlignTop)

        #######################

        self.subtask_label = QtWidgets.QLabel("Subtasks")
        self.subtask_label.setProperty("class", "title")

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        content_widget = QtWidgets.QWidget(self.scrollArea)
        self.scrollArea.setWidget(content_widget)

        self.scroll_area_layout = QtWidgets.QVBoxLayout(content_widget)
        self.scroll_area_layout.setAlignment(QtCore.Qt.AlignTop)

        for subtask in self.subtasks:
            self.scroll_area_layout.addWidget(self.add_subtasks_to_scroll_area(subtask["name"], str(subtask["state"]), subtask["date"]))

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setAlignment(QtCore.Qt.AlignTop)
        right_layout.addWidget(self.subtask_label)
        right_layout.addWidget(self.scrollArea)

        #######################

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addLayout(left_layout)
        horizontal_layout.addLayout(right_layout)

        self.setLayout(horizontal_layout)

    def add_subtasks_to_scroll_area(self, name, state, date):
        self.task_widget = QtWidgets.QWidget()
        self.task_widget.setFixedHeight(50)
        widgetLayout = QtWidgets.QHBoxLayout()

        task_label = QtWidgets.QLabel(name)

        task_label_state = QtWidgets.QLabel("State:")
        task_label_state.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        task_state = QtWidgets.QLabel(state)

        task_label_deadline = QtWidgets.QLabel("Deadline:")
        task_label_deadline.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        task_deadline = QtWidgets.QLabel(date)
        task_deadline.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../client/assets/edit.svg"))
        task_button2 = QtWidgets.QPushButton()
        task_button2.setIcon(icon2)
        task_button2.setIconSize(QtCore.QSize(24, 24))
        task_button2.setSizePolicy(sizePolicy)

        widgetLayout.addWidget(task_label)
        widgetLayout.addWidget(task_label_state)
        widgetLayout.addWidget(task_state)
        widgetLayout.addWidget(task_label_deadline)
        widgetLayout.addWidget(task_deadline)
        widgetLayout.addWidget(task_button2)

        self.task_widget.setLayout(widgetLayout)
        self.task_widget.setFixedHeight(50)
        self.task_widget.setObjectName("task")

        return self.task_widget

    def api_get_subtasks(self):
        self.TCP_Session.send_data({
            "client": "get_subtasks",
            "task_id": self.task_id
        })
        try:
            result = self.TCP_Session.get_data()["content"]
        except KeyError:
            return []
        else:
            return result