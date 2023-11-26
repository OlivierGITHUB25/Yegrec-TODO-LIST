import ssl
from PyQt5 import QtWidgets

from .C_Infobox import InfoBox


class MainWindow(QtWidgets.QWidget):
    def __init__(self, tcp_session):
        super().__init__()
        self.TCP_Session = tcp_session
        self.setWindowTitle("YeGrec's View")
        self.setGeometry(100, 100, 800, 400)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

    def closeEvent(self, event):
        try:
            self.TCP_Session.send_data({
                "client": "DISCONNECT",
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
        finally:
            event.accept()
