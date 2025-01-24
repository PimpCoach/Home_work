# Класс для работы с текстовыми файлами
class TxtFileHandler:
    # Метод чтения 
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        
    # Метод записи 
    @staticmethod
    def write_file(file_path: str, *data: str, encoding: str = 'utf-8') -> None:
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(*data + '\n')

    #Метод добавления данных 
    @staticmethod
    def append_file(file_path: str, *data: str, encoding: str = 'utf-8') -> None:
        with open(file_path, 'a', encoding=encoding) as file:
            file.write(*data + '\n')