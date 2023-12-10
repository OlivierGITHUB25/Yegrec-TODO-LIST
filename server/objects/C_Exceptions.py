

class UsernameError(Exception):
    def __init__(self, message="USERNAME_ERROR"):
        self.__message = message
        super().__init__(self.__message)


class PasswordError(Exception):
    def __init__(self, message="PASSWORD_ERROR"):
        self.__message = message
        super().__init__(self.__message)
