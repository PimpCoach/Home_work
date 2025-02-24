from dataclasses import dataclass
from random import choice
from typing import Any
import json


@dataclass
class JsonFile:
    """
    Класс для работы с JSON файлом
    Attributes:
        file_path (str): Путь к файлу
    """

    file_path: str

    def read_data(self) -> list[dict[str, Any]]:
        """
        Чтение данных из JSON файла
        Returns:
            list[dict[str, Any]]: Данные из JSON файла
            None: Если прозошла ошибка
        Raises:
            FileNotFoundError: Файл не найден
            json.JSONDecodeError: Содержимое файла не декодируется
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.file_path} не найден!")
            return None
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле {self.file_path}!")
            return None

    def write_data(self, data: dict[str, Any]) -> bool:
        """
        Запись данных в JSON файл
        Args:
            data dict[str, Any]): Данные которые нужно записать
        Returns:
            True: Если данные успешно записались
            False: Если произошла ошибка
        Raises:
            TypeError: Данные не записались
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                return True
        except TypeError as e:
            print(f"Ошибка при записи данных в файл {self.file_path}: {e}")
            return False


@dataclass
class City:
    """
    Класс для представления города
    Attributes:
        name (str): Название города
        population (int): Населения города
        subject (str): Субъект федерации
        district (str): Район
        latitude (float): Широта
        longitude (float): Долгота
        is_used (bool): Флаг, указывающий, использован ли город в игре (по умолчанию False)
    """

    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False


class CitiesSerializer:
    """
    Класс для сериализации данных о городах из списка словарей в список объекта класса City
    """

    def __init__(self, city_data: list[dict[str, Any]]) -> None:
        """
        Инициализирует список городов
        Args:
            city_data (list[dict[str, Any]]) - Данные о городах
            Каждый словарь должен содержать ключи:
                - "name" (str): Название города.
                - "population" (int): Население города.
                - "subject" (str): Субъект федерации.
                - "district" (str): Район.
                - "lat" (float): Широта.
                - "lon" (float): Долгота.
        """
        self.cities = []
        for city in city_data:
            self.cities.append(
                City(
                    name=city["name"],
                    population=city["population"],
                    subject=city["subject"],
                    district=city["district"],
                    latitude=city["lat"],
                    longitude=city["lon"],
                )
            )

    def get_all_cities(self) -> list[City]:
        """
        Возвращает список всех городов
            Returns:
                list[City]: Список городов City
        """
        return self.cities


class CityGame:
    """
    Класс для управления логики игры
    Attributes:
        cities (CitiesSerializer): Объект для работы с данными о городах
        used_cities (set[str]): Использованные города
        last_city (str): Последний город
        city_list (list[str]): Список всех городов
        bad_letters (set): Буквы, которые не используются в названиях городов
    """

    def __init__(self, cities: CitiesSerializer) -> None:
        self.cities: CitiesSerializer = cities
        self.used_cities: set[str] = set()
        self.last_city: str = ""
        self.cities_list: list[str] = self._city_list()
        self.bad_letters: set = self._bad_letters()

    def _city_list(self) -> list[str]:
        """
        Возвращает список городов
        Returns:
            list[str]: Список городов
        """
        return [city.name for city in self.cities.get_all_cities()]

    def _bad_letters(self) -> set:
        """
        Возвращает буквы, которые не используются в названиях городов
        Returns:
            set: Множество букв
        """
        all_last_letters = set()
        all_first_letters = set()

        for city in self.cities_list:
            all_last_letters.add(city[-1].lower())
            all_first_letters.add(city[0].lower())

        bad_letters = all_last_letters - all_first_letters
        return bad_letters

    def _last_letter(self) -> str:
        """
        Возвращает последнюю букву предыдущего города
        Returns:
            str: Последняя буква предыдущего города
        """
        if self.last_city:
            for letter in reversed(self.last_city):
                if letter.lower() not in self.bad_letters:
                    return letter
        return ""

    def start_game(self) -> None:
        """
        Начинает игру, включая первый ход компьютера
        """
        print("Игра началась")
        first_city = choice(self.cities_list)
        self.last_city = first_city
        self.used_cities.add(first_city)
        self.cities_list.remove(first_city)
        return self.computer_turn()

    def human_turn(self, city_input: str) -> bool:
        """
        Обрабатывает ход человека:

        Args:city_input
            city_input (str): Пользовательский ввод города

        Returns:
            bool: True, если город соответствует всем критериям
                False, если человек ошибся
        """
        if city_input.lower() == "стоп":
            print("Игра окончена!")
            return False

        last_letter = self._last_letter().upper()
        if city_input[0].upper() != last_letter:
            print(f"Город должен начинаться на букву {last_letter}. Вы проиграли!")
            return False

        if city_input not in self.cities_list:
            print("Такого города нет. Вы проиграли!")
            return False

        if city_input in self.used_cities:
            print("Этот город уже был использован!")
            return False

        self.cities_list.remove(city_input)
        self.used_cities.add(city_input)
        self.last_city = city_input
        return True

    def computer_turn(self) -> None:
        """
        Обрабатывает ход компьютера
        Создает список городов, которые можно использовать и выбирает один из них случайным образом
        """
        last_letter = self._last_letter().upper()

        computer_city_list: list[str] = [city for city in self.cities_list if city not in self.used_cities and city[0].upper() == last_letter]

        if computer_city_list:
            computer_city = choice(computer_city_list)
            print(f"\nКомпьютер выбирает: {computer_city}\n")
            self.cities_list.remove(computer_city)
            self.used_cities.add(computer_city)
            self.last_city = computer_city
        else:
            print("Компьютер не смог найти подходящий город. Вы выиграли!")

    def check_game_over(self) -> bool:
        """
        Проверяет завершение игры
        Returns:
            bool: True, если все города использованы
                False, если есть города
        """
        return len(self.used_cities) == len(self.cities.get_all_cities())

    def save_game_state(self) -> None:
        """
        Сохраняет состояние игры в файл
        """
        game_state: dict[str, Any] = {
            "Использованные города": list(self.used_cities),
            "Последний город": self.last_city,
            "Список городов": self.cities_list,
        }
        json_game_state = JsonFile('game_state.json')
        json_game_state.write_data(game_state)

    def load_game_state(self):
        """
        Загружает состояние игры из файла
        """
        json_game_state = JsonFile('game_state.json')
        game_state = json_game_state.read_data()

        if game_state:
            self.used_cities = set(game_state["Использованные города"])
            self.last_city = game_state["Последний город"]
            self.cities_list = game_state["Список городов"]
            print("Игра загружена")
            return True
        else:
            return False