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