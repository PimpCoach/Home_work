import json
import csv

from abc import ABC, abstractmethod


class AbstractFile(ABC):
    """
    Абстрактный класс для работы с файлами
    """

    @abstractmethod
    def read(self):
        """
        Абстрактный метод для чтения данных из файла

        Returns:
            Данные, прочитанные из файла
            
        """
        pass

    @abstractmethod
    def write(self, data) -> None:
        """
        Абстрактный метод для записи данных в файл

        Args:
            data: данные которые нужно записать

        Returns:
            None
        """
        pass

    @abstractmethod
    def append(self, data) -> None:
        """
        Абстрактный метод для добалвения данных в файл

        Args:
            data: данные которые нужно добавить

        Returns:
            None
        """
        pass

