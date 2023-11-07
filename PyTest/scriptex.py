import pytest
from PyQt5.QtWidgets import QApplication
from votre_script import Login

app = QApplication([])


def test_login_initialization():
    login_window = Login()
    assert login_window.lbl.text() == "Identifiant:"
    assert login_window.lbl2.text() == "Mots de Passe:"
    assert login_window.bouton1.text() == "Connexion"
    assert login_window.bouton2.text() == "Créer un compte"
