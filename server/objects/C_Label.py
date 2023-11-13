import re


class Label:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        self._validate_args()

    def __str__(self):
        return (f"name : {self.__name}\n"
                f"color : {self.__color}\n")

    def _validate_args(self):
        if not isinstance(self.__name, str): # name verification
            raise TypeError("InvalidJSONFormat")
        elif len(self.__name) <= 0 or len(self.__name) > 45:
            raise ValueError("ValueError")

        if not isinstance(self.__color, str): # hex color code verification
            raise TypeError("InvalidJSONFormat")
        elif not re.search("^#[A-Fa-f0-9]{6}$", self.__color):
            raise ValueError("ValueError")

    def get_name(self) -> str:
        return self.__name

    def get_color(self) -> str:
        return self.__color
