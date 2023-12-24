import ssl
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from .C_Infobox import InfoBox


class MainWindow(QtWidgets.QWidget):
    def __init__(self, tcp_session):
        super().__init__()
        self.TCP_Session = tcp_session
        self.setWindowTitle("YeGrec's View")
        self.setGeometry(100, 100, 800, 400)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.grid.addLayout(self.verticalLayout, 0, 0)
        self.tasks = self.get_task()
        print(self.tasks)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YeGrec's Todo List")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(self.css_loader('../client/styles/styles.css'))

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

        # Menu bar

        self.menubar = QtWidgets.QMenuBar()

        self.menuFile = QtWidgets.QMenu("File")
        self.actionCreateTask = QtWidgets.QAction("Create task")
        self.actionCreateTask.setIcon(icon1)
        self.actionCreateLabel = QtWidgets.QAction("Create label")
        self.actionCreateLabel.setIcon(icon2)
        self.actionEditObject = QtWidgets.QAction("Edit object")
        self.actionEditObject.setIcon(icon3)
        self.actionDeleteObject = QtWidgets.QAction("Delete object")
        self.actionDeleteObject.setIcon(icon4)
        self.actionListUsers = QtWidgets.QAction("List users")
        self.actionListUsers.setIcon(icon5)
        self.actionQuit = QtWidgets.QAction("Quit")
        self.actionQuit.setIcon(icon6)
        self.actionQuit.triggered.connect(self.closeEvent)

        self.menuAbout = QtWidgets.QMenu("About")

        self.menubar.addMenu(self.menuFile)
        self.menuFile.addAction(self.actionCreateTask)
        self.menuFile.addAction(self.actionCreateLabel)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEditObject)
        self.menuFile.addAction(self.actionDeleteObject)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionListUsers)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        self.menubar.addMenu(self.menuAbout)

        self.grid.setMenuBar(self.menubar)

        # First line (horizontal layout)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(32, 32))

        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))

        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))

        self.pushButton_4 = QtWidgets.QPushButton()
        self.pushButton_4.setIcon(icon4)
        self.pushButton_4.setIconSize(QtCore.QSize(32, 32))

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.pushButton_5 = QtWidgets.QPushButton()
        self.pushButton_5.setIcon(icon5)
        self.pushButton_5.setIconSize(QtCore.QSize(32, 32))

        self.pushButton_6 = QtWidgets.QPushButton()
        self.pushButton_6.setIcon(icon6)
        self.pushButton_6.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_6.clicked.connect(self.closeEvent)

        # Second line (scroll area)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        content_widget = QtWidgets.QWidget(self.scrollArea)
        self.scrollArea.setWidget(content_widget)

        self.layout = QtWidgets.QVBoxLayout(content_widget)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        for i in range(0, 50):
            self.layout.addWidget(self.add_tasks_to_scroll_area())

        # Third line (horizontal layout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        self.pushButton_7 = QtWidgets.QPushButton()
        self.pushButton_7.setIcon(icon7)
        self.pushButton_7.setIconSize(QtCore.QSize(12, 12))

        self.label = QtWidgets.QLabel("Sort by:")
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.label_2 = QtWidgets.QLabel("Date")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.label_3 = QtWidgets.QLabel("YeGrec's list")
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        # Layout definition

        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.horizontalLayout.addWidget(self.pushButton_6)

        self.horizontalLayout_2.addWidget(self.pushButton_7)
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.label_3)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

    def closeEvent(self, event, **kwargs):
        reply = QtWidgets.QMessageBox.question(self, 'Quit', 'Are you sure you want to quit YeGrec ?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
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

    def get_task(self):
        self.TCP_Session.send_data({
            "client": "get_tasks",
        })
        return self.TCP_Session.get_data()["content"]

    def add_tasks_to_scroll_area(self):
        self.task_widget = QtWidgets.QWidget()
        self.task_widget.setFixedHeight(50)
        widgetLayout = QtWidgets.QGridLayout()

        task_label = QtWidgets.QLabel("Task 1")

        task_label_state = QtWidgets.QLabel("State:")
        task_label_state.setAlignment(QtCore.Qt.AlignRight)
        task_state = QtWidgets.QLabel("HIGH")

        task_label_priority = QtWidgets.QLabel("Priority:")
        task_label_priority.setAlignment(QtCore.Qt.AlignRight)
        task_priority = QtWidgets.QLabel("FINISHED")

        task_label_deadline = QtWidgets.QLabel("Deadline:")
        task_label_deadline.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        task_deadline = QtWidgets.QLabel("20/15/2003")
        task_deadline.setAlignment(QtCore.Qt.AlignVCenter)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../client/assets/settings.svg"))
        task_button = QtWidgets.QPushButton()
        task_button.setIcon(icon)
        task_button.setIconSize(QtCore.QSize(24, 24))

        widgetLayout.addWidget(task_label, 0, 0, 2, 1)
        widgetLayout.addWidget(task_label_priority, 0, 1, 1, 1)
        widgetLayout.addWidget(task_priority, 0, 2, 1, 1)
        widgetLayout.addWidget(task_label_state, 1, 1, 1, 1)
        widgetLayout.addWidget(task_state, 1, 2, 1, 1)
        widgetLayout.addWidget(task_label_deadline, 0, 3, 2, 1)
        widgetLayout.addWidget(task_deadline, 0, 4, 2, 1)
        widgetLayout.addWidget(task_button, 0, 5, 2, 1)

        self.task_widget.setLayout(widgetLayout)
        self.task_widget.setFixedHeight(50)
        self.task_widget.setObjectName("task")

        return self.task_widget

    @staticmethod
    def css_loader(filename):
        with open(filename, 'r') as rd:
            content = rd.read()
            rd.close()
        return content
