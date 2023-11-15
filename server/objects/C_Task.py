from datetime import datetime


class Task:
    def __init__(self, name, state, priority, date, description, labels_id: list, users_id: list):
        self.__name = name
        self.__state = state
        self.__priority = priority
        self.__date = date
        self.__description = description
        self.__labels_id = labels_id
        self.__users_id = users_id
        self._validate_args()

    def __str__(self):
        return (f"name : {self.__name}\n"
                f"state : {self.__state}\n"
                f"priority : {self.__priority}\n"
                f"date : {self.__date}\n"
                f"description : {self.__description}\n"
                f"labels : {self.__labels_id}\n"
                f"users : {self.__users_id}")

    def _validate_args(self):
        if not isinstance(self.__name, str):  # name verifications
            raise TypeError("InvalidJSONFormat")
        elif len(self.__name) <= 0 or len(self.__name) > 45:
            raise ValueError("ValueError")

        if not isinstance(self.__state, int):  # state verifications
            raise TypeError("InvalidJSONFormat")
        elif self.__state <= 0 or self.__state > 3:
            raise ValueError("ValueError")

        if not isinstance(self.__priority, int):  # priority verifications
            raise TypeError("InvalidJSONFormat")
        elif self.__priority <= 0 or self.__priority > 3:
            raise ValueError("ValueError")

        if not isinstance(self.__date, str):  # date verifications
            raise TypeError("InvalidJSONFormat")
        else:
            try:
                datetime.strptime(self.__date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("ValueError")

        if not isinstance(self.__description, str):  # description verifications
            raise TypeError("InvalidJSONFormat")
        elif len(self.__description) <= 0 or len(self.__description) > 255:
            raise ValueError("ValueError")

        if not isinstance(self.__labels_id, list):  # labels verifications
            raise TypeError("InvalidJSONFormat")
        else:
            for label_id in self.__labels_id:
                if not isinstance(label_id, int):
                    raise ValueError("ValueError")

        if not isinstance(self.__users_id, list):  # users verifications
            raise TypeError("InvalidJSONFormat")
        else:
            for user_id in self.__users_id:
                if not isinstance(user_id, int):
                    raise ValueError("ValueError")

    def get_name(self) -> str:
        return self.__name

    def get_state(self) -> int:
        return self.__state

    def get_priority(self) -> int:
        return self.__priority

    def get_date(self) -> str:
        return self.__date

    def get_description(self) -> str:
        return self.__description

    def get_labels_id(self) -> list:
        return self.__labels_id

    def get_users_id(self) -> list:
        return self.__users_id
