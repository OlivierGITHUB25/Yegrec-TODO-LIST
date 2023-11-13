import re
from . import C_Exceptions


class User:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self._validate_args()

    def __str__(self):
        return (f"username : {self.__username}\n"
                f"password : {self.__password}\n")

    def _validate_args(self):
        if not re.search(r"^[a-zA-Z-0-9]+$", self.__username): # username verifications
            raise C_Exceptions.UsernameError
        elif len(self.__username) < 5 or len(self.__username) >= 255:
            raise C_Exceptions.UsernameError

        if len(self.__password) < 7 or len(self.__password) >= 255: #password verification
            raise C_Exceptions.PasswordError

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password
