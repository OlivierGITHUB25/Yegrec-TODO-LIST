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
    def __init__(self):
        super().__init__()

        self.setStyleSheet(css_loader('../client/styles/styles.css'))
        self.setWindowTitle("Create task")
        self.setFixedWidth(400)

        self.label1 = QtWidgets.QLabel("Task name")
        self.edit1 = QtWidgets.QLineEdit()

        self.label2 = QtWidgets.QLabel("State")
        self.edit2 = QtWidgets.QComboBox()
        self.edit2.addItems(["TODO", "In progress", "Finished"])

        self.label3 = QtWidgets.QLabel("Priority")
        self.edit3 = QtWidgets.QComboBox()
        self.edit3.addItems(["LOW", "NORMAL", "HIGH"])

        self.label4 = QtWidgets.QLabel("Date")
        self.edit4 = QtWidgets.QDateEdit()

        self.label5 = QtWidgets.QLabel("Description")
        self.edit5 = QtWidgets.QPlainTextEdit()

        self.ok_button = QtWidgets.QPushButton("Validate")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.edit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.edit2)
        layout.addWidget(self.label3)
        layout.addWidget(self.edit3)
        layout.addWidget(self.label4)
        layout.addWidget(self.edit4)
        layout.addWidget(self.label5)
        layout.addWidget(self.edit5)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


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
        state_mapping = {1: "TODO", 2: "In progress", 3: "Finished"}
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
        return self.TCP_Session.get_data()["content"]
