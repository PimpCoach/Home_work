import json
import csv

from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractFile(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def read(self) -> Any:
        """
        Абстрактный метод для чтения данных из файла
        Returns:
            Any: Данные, прочитанные из файла
        """
        pass

    @abstractmethod
    def write(self, data: Any) -> None:
        """
        Абстрактный метод для записи данных в файл
        Args:
            data (Any): данные которые нужно записать
        Returns:
            None
        """
        pass

    @abstractmethod
    def append(self, data: Any) -> None:
        """
        Абстрактный метод для добалвения данных в файл
        Args:
            data(Any): данные которые нужно добавить
        Returns:
            None
        """
        pass


class JsonFile(AbstractFile):
    """
    Класс для работы с JSON файлами
    Чтение, запись и добавление
    """

    def __init__(self, file_path: str):
        """
        Инициализотор обработчика файла
        Args:
            file_path (str): Путь к файлу
        """
        self.file_path = file_path

    def read(self) -> Dict[str, Any]:
        """
        Чтение данных из JSON файла
        Returns:
            Dict[str, Any]: Данные из JSON файла
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, data: dict[str, Any]) -> None:
        """
        Запись данных в JSON файл
        Args:
            data (Dict[str, Any]): Данные которые нужно записать в файл
        Returns:
            None
        """

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def append(self, data: dict[str, Any]) -> None:
        """
        Добавление данных в существующий JSON файл
        Args:
            data(Dict[str, Any]): данные которые нужно добавить в файл
        Returns:
            None
        """
        data_json =  self.read()

        data_json.update(data)

        self.write(data_json)


class TxtFile(AbstractFile):
    """
    Класс дря работы с TXT файлами
    Чтение, запись и добавление
    """

    def __init__(self, file_path: str):
        """
        Инициализотор обработчика файла
        Args:
            file_path (str): Путь к файлу
        """
        self.file_path = file_path

    def read(self) -> str:
        """
        Чтение данных из TXT файла
        Returns:
            str: Данные из TXT документа
        """
        with open(self.file_path, 'r', encoding= 'utf-8') as f:
            return f.read()

    def write(self, data: str) -> None:
        """
        Запись данных в TXT документ
        Args:
            data (str): данные которые нужно записать в файл
        Returns:
            None
        """
        with open(self.file_path, 'w', encoding= 'utf-8') as f:
            f.write(data)

    def append(self, data:str):
        """
        Добавление данных в существующий TXT документ
        Args:
            data (str): данные которые нужно добавить в файл
        Returns:
            None
        """
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(data + '\n')


class CsvFile(AbstractFile):
    """
    Класс для работы с CSV файлами
    Чтение, запись и добавление
    """

    def __init__(self, file_path: str):
        """
        Инициализотор обработчика файла
        Args:
            file_path (str): Путь к файлу
        """
        self.file_path = file_path

    def read(self) -> list:
        """
        Чтение данных из CSV файла
        Returns:
            list: данные из CSV документа в виде списка с разделитем "; "
        """
        with open(self.file_path, 'r', encoding = 'utf-8-sig') as f:
            return list(csv.reader(f, delimiter=";"))

    def write(self, data: list) -> None:
        """
        Запись данных в CSV файл
        Args:
            data (list): данные которые нужно записать в CSV файл
        Returns:
            None
        """
        with open(self.file_path, 'w', encoding ='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerow(data)

    def append(self, data: list) -> None:
        """
        Добавлние данных в CSV файл
        Args:
            data (list): данные которые нужно добавить в CSV файл
        Returns:
            None
        """
        with open(self.file_path, 'a', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';', lineterminator='\n')
            writer.writerow(data)