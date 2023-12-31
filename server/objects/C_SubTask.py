from datetime import datetime


class SubTask:
    def __init__(self, name, state, date, task_id, labels: list = None):
        self.__name = name
        self.__state = state
        self.__date = date
        self.__task_id = task_id
        self.__labels = labels
        self._validate_args()

    def __str__(self):
        return (f"name : {self.__name}\n"
                f"state : {self.__state}\n"
                f"date : {self.__date}\n"
                f"task_id : {self.__task_id}\n"
                f"labels : {self.__labels}")

    def _validate_args(self):
        if not isinstance(self.__name, str):  # name verifications
            raise TypeError("InvalidJSONFormat")
        elif len(self.__name) <= 0 or len(self.__name) > 45:
            raise ValueError("ValueError")

        if not isinstance(self.__state, int):  # state verifications
            raise TypeError("InvalidJSONFormat")
        elif self.__state <= 0 or self.__state > 3:
            raise ValueError("ValueError")

        if not isinstance(self.__date, str):  # date verifications
            raise TypeError("InvalidJSONFormat")
        else:
            try:
                datetime.strptime(self.__date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("ValueError")

        if not isinstance(self.__task_id, int):  # task_id verifications
            raise TypeError("InvalidJSONFormat")

        if not isinstance(self.__labels, list):  # labels verifications
            raise TypeError("InvalidJSONFormat")

    def get_name(self) -> str:
        return self.__name

    def get_state(self) -> int:
        return self.__state

    def get_date(self) -> str:
        return self.__date

    def get_task_id(self) -> int:
        return self.__task_id

    def get_labels(self) -> list:
        return self.__labels
