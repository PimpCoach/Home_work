# Класс для работы с текстовыми файлами
class TxtFileHandler:
    """
    Класс для работы с текстовыми файлами с методами чтения, записи 
    и добавления данных в текстовый документ с обработкой исключений
    """
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
            """
            Чтение TXT файла 
            :param file_path: путь к файлу в виде строки
            :paran encoding: кодировка файла по умолчанию 'utf-8)
            :return: содержимое файла в виде строки,
                    при ошибке пустую строку
            """
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except FileNotFoundError:
                print(f'Файла {file_path} не существует')
                return ""
            except PermissionError:
                print(f'Ошибка доступа при чтении файла {file_path}')
                return ""

    @staticmethod
    def write_file(file_path: str, *data: str, encoding: str = 'utf-8') -> bool:
        """
        Запись данных в файл с обрабоской ошибок
        :param file_path: путь к файлу в виде строки
        :param *data
        :paran encoding: кодировка файла по умолчанию 'utf-8)
        :return: True если запись успешна,
                False если ошибка)
        """
        try:
            with open(file_path, 'w', encoding=encoding) as file:
                file.write(*data)
                return True
        except PermissionError:
                print(f'Ошибка доступа при чтении файла {file_path}')
                return False

    @staticmethod
    def append_file(file_path: str, *data: str, encoding: str = 'utf-8') -> bool:
        """
        Добавление данных в файл с обрабоской ошибок
        Запись данных в файл с обрабоской ошибок
        :param file_path: путь к файлу в виде строки
        :paran encoding: кодировка файла по умолчанию 'utf-8)
        :return: True если запись успешна,
                False если ошибка 
        """
        try:
            with open(file_path, 'a', encoding=encoding) as file:
                file.write(*data)
                return True
        except PermissionError:
                print(f'Ошибка доступа при чтении файла {file_path}')
                return False

