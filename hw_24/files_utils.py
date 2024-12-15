import json


# функция для чтение данных и JSON файла
def read_json(file_path: str, encoding: str = "utf-8") -> dict:
    with open(file_path, "r", encoding=encoding) as file:
        return json.load(file)


# фунция для записи данных в JSON
def write_json(data, file_path: str, encoding: str = "utf-8") -> None:
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# фнукция которая добавляет данные в существующий JSON
def append_json(data: list[dict], file_path: str, encoding: str = "utf-8") -> None:
    with open(file_path, "r", encoding=encoding) as file:
        data_json = json.load(file)

        data_json.update(data)

    with open(file_path, "w", encoding=encoding) as file:
        json.dump(data_json, file, ensure_ascii=False, indent=4)


# Работа с CSV
import csv


def read_csv(file_path, delimiter=";", encoding: str = "utf-8-sig") -> list:
    with open(file_path, "r", encoding=encoding) as file:
        reader = csv.reader(file, delimiter=delimiter)
        return list(reader)


def write_csv(data, file_patch, delimiter=';', encoding: str ="utf-8-sig") -> None:
    with open(file_patch, 'w', encoding=encoding) as file:
        writer = csv.writer(file, delimiter=delimiter, lineterminator='\n')
        writer.writerow(data)

def append_csv(data, file_patch, delimiter=';', encoding: str ='utf-8-sig') -> None:
    with open(file_patch, 'a', encoding=encoding) as file:
        writer = csv.writer(file, delimiter=delimiter,lineterminator='\n')
        writer.writerow(data)
