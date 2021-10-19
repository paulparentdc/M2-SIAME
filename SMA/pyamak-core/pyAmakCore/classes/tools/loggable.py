"""
class allowing to save the state of the system at a given moment
"""
from os import path
from typing import List
from pandas import DataFrame


class Loggable:
    """
    class Loggable
    """
    def __init__(self):
        self.__do_log = False
        self.__file_path = None
        self.__ignore_attribute: List[str] = ["_Agent__amas", "_Agent__environment"]

    def to_csv(self, cycle: int, var_list: List['Agent']) -> None:
        """
        get cycle and agent list and print them
        """
        if not self.__do_log:
            return

        table = [{**{e: x[e] for e in x if e not in self.__ignore_attribute},
                  **{'nombre_cycle': cycle}} for x in map(vars, var_list)]
        dataframe = DataFrame(table)

        if self.__file_path is None:
            print(dataframe.to_csv(index=False))
        else:
            if path.exists(self.__file_path):
                dataframe.to_csv(path_or_buf=self.__file_path, mode='a', header=False, index=False)
            else:
                dataframe.to_csv(path_or_buf=self.__file_path, index=False)

    def set_do_log(self, boolean: bool) -> None:
        """
        tell the amas if it should log or not
        """
        self.__do_log = boolean

    def set_file_path(self, path_to_file: str) -> None:
        """
        specify path to csv
        """
        self.__file_path = path_to_file

    def add_ignore_attribute(self, attribute: str) -> None:
        """
        add attribute in ignored attribute
        """
        self.__ignore_attribute.append(attribute)

    def remove_ignore_attribute(self, attribute: str) -> None:
        """
        remove attribute in ignored attribute
        """
        if attribute not in self.__ignore_attribute:
            return
        self.__ignore_attribute.remove(attribute)
