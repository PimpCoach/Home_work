import tkinter as tk
from tkinter import messagebox
from hw_31 import JsonFile, CitiesSerializer, CityGame
from typing import Any
import json
import os


class CityGameGUI:
    """
    Графический интерфейс игры в города.
    Класс предоставляет пользовательский интерфейс для игры в города с компьютером.
    Включает в себя окно с историей игры, поле ввода для городов и кнопки управления.
    Attributes:
        root (tk.Tk): Главное окно приложения
        game (CityGame): Экземпляр игровой логики
        history_text (tk.Text): Виджет для отображения истории игры
        entry (tk.Entry): Поле ввода для названий городов
    """

    def __init__(self, root) -> None:
        """
        Инициализирует графический интерфейс игры.
        Args:
            root (tk.Tk): Корневое окно приложения
        """
        self.root = root
        self.root.title("Игра в города")
        self.root.geometry("600x400")

        # Инициализация игровой логики
        json_file = JsonFile("cities.json")
        cities_serializer = CitiesSerializer(json_file.read_data())
        self.game = CityGame(cities_serializer)

        # Создание элементов интерфейса
        self.create_widgets()

        # Добавляем приветствие
        welcome_text = "Добро пожаловать в игру 'Города'!\n\n"
        welcome_text += "Для начала игры нажмите 'Новая игра' или 'Загрузить игру'\n"
        welcome_text += "Для выхода нажмите 'Выход'\n"
        self.history_text.insert(1.0, welcome_text)
        
        # Блокируем поле ввода и кнопку ответа, сохранить и закончить при запуске приложения
        self.entry.config(state='disabled')
        self.submit_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.finish_button.config(state='disabled')

    def create_widgets(self) -> None:
        """
        Создает и размещает все элементы графического интерфейса:
        - Текстовое поле для истории игры со скроллбаром
        - Поле ввода и кнопка ответа
        - Кнопки управления (новая игра, завершение, сохранить, загрузить, выход)
        """
        history_frame = tk.Frame(self.root)  # Контейнер для истории игры
        history_frame.pack(pady=15)  # Отступ сверху и снизу

        self.history_text = tk.Text(history_frame, height=15, width=60)  # Текстовое поле для истории игры
        self.history_text.pack(side=tk.LEFT)  # Расположение слева текстового поля. side=tk.LEFT - расположение слева

        scrollbar = tk.Scrollbar(history_frame)  # Полоса прокрутки
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Расположение справа текстового поля. fill=tk.Y - растяжение по вертикали

        self.history_text.config(yscrollcommand=scrollbar.set)  # Связывает текстовое поле с полосой прокрутки
        scrollbar.config(command=self.history_text.yview)  # command - связывает полосу прокрутки с текстовым полем

        # Поле ввода
        input_frame = tk.Frame(self.root)  # Контейнер для поля ввода
        input_frame.pack(pady=10)  # Создает отступ сверху и снизу

        self.entry = tk.Entry(input_frame, width=50)  # Поле ввода
        self.entry.pack(side=tk.LEFT, padx=10)  # Расположение слева текстового поля. padx= - отступ слева и справа
        self.entry.bind('<Return>', lambda event: self.make_move()) # Связывает нажатие клавиши Enter с методом make_move

        self.submit_button = tk.Button(input_frame, text="Ответить", command=self.make_move)  # Кнопка для ответа. command - связывает нажатие кнопки с методом make_move
        self.submit_button.pack(side=tk.LEFT)  # Расположение слева от оставшевогося свободного места

        # Кнопки управления
        control_frame = tk.Frame(self.root)  # Контейнер для кнопок управления
        control_frame.pack(pady=15)  #  Создает отступ сверху и снизу

        new_game_button = tk.Button(control_frame, text="Новая игра", command=self.start_new_game)  # Кнопка для новой игры. command - связывает нажатие кнопки с методом start_new_game
        new_game_button.pack(side=tk.LEFT, padx=16)  # Раасположение слева от оставшевогося свободного места

        self.finish_button = tk.Button(control_frame, text="Закончить игру", command=self.stop_game)  # Кнопка для завершения игры. command - связывает нажатие кнопки с методом stop_game
        self.finish_button.pack(side=tk.LEFT, padx=16)  

        self.save_button = tk.Button(control_frame, text="Сохранить игру", command=self.save_game) # Кнопка для сохранения игры. command - связывает нажатие кнопки с методом save_game
        self.save_button.pack(side=tk.LEFT, padx=16)

        load_button = tk.Button(control_frame, text="Загрузить игру", command=self.load_game) # Кнопка для загрузки игры. command - связывает нажатие кнопки с методом load_game
        load_button.pack(side=tk.LEFT, padx=16)

        quit_button = tk.Button(control_frame, text="Выход", command=self.quit_game)  # Кнопка для выхода. command - связывает нажатие кнопки с методом quit
        quit_button.pack(side=tk.RIGHT, padx=16)  # Раасположение слева от оставшевогося свободного места


    def save_game(self) -> None:
        """
        Сохраняет текущее состояние игры в JSON файл.
        Сохраняются следующие данные:
        - Список использованных городов
        - Последний названный город
        - Полный список доступных городов
        - История игры
        """
        game_state: dict[str, Any] = {
            "used_cities": list(self.game.used_cities),
            "last_city": self.game.last_city,
            "cities_list": self.game.cities_list,
            "history": self.history_text.get(1.0, tk.END)
        }
        
        with open("game_save.json", "w", encoding="utf-8") as f:
            json.dump(game_state, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Сохранение", "Игра успешно сохранена!")

    def load_game(self) -> None:
        """
        Загружает сохраненное состояние игры из JSON файла.
        Восстанавливает:
        - Список использованных городов
        - Последний названный город
        - Список доступных городов
        - Историю игры
        Активирует элементы управления для продолжения игры.
        
        Raises:
            FileNotFoundError: Если файл сохранения не найден
        """
        try:
            with open("game_save.json", "r", encoding="utf-8") as f:
                game_state = json.load(f)
            
            self.game.used_cities = set(game_state["used_cities"])
            self.game.last_city = game_state["last_city"]
            self.game.cities_list = game_state["cities_list"]

            self.history_text.delete(1.0, tk.END)

            self.update_history("\nИгра загружена. Ваш ход!")
            self.update_history(f'\nИспользованные города: {", ".join(sorted(self.game.used_cities))}')
            self.update_history(f'\nПоследний названный город: {self.game.last_city}')
            self.update_history(f"Назовите город на букву: {self.game.last_letter().upper()}")

            self.entry.config(state='normal')
            self.submit_button.config(state='normal')
            self.finish_button.config(state='normal')  
            self.save_button.config(state='normal')  

            messagebox.showinfo("Загрузка", "Игра успешно загружена! Ваш ход.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл сохранения не найден!")

    def start_new_game(self) -> None:
        """
        Начинает новую игру:
        - Очищает список использованных городов
        - Сбрасывает последний названный город
        - Обновляет список доступных городов
        - Очищает историю игры
        - Запускает первый ход компьютера.
        - Удаляет файл сохранения, если он существует.
        """
        try:
            os.remove("game_save.json")
            messagebox.showinfo("Новая игра", "Игра Началась!")
        except FileNotFoundError:
            pass

        self.game.used_cities.clear()  # Очищает список использованных городов.
        self.game.last_city = ""  # Сбрасывает последний город.
        self.game.cities_list = (self.game._city_list())  # Получает список всех доступных городов.
        self.history_text.delete(1.0, tk.END)  # Очищает текстовое поле. 1.0 - начало текста. tk.END - конец текста. Удаляет все символы от начала до конца.
        self.game.start_game()  # Запускает игру.
        self.update_history(f"Компьютер: {self.game.last_city}")  # Отображает первый ход компьютера.
        self.entry.config(state='normal')  # Разрешает ввод пользователя.
        self.submit_button.config(state='normal')  # Разрешает кнопку ответа.
        self.finish_button.config(state='normal')  # Разрешает кнопку завершения игры.
        self.save_button.config(state='normal')  # Разрешает кнопку сохранения.

    def stop_game(self) -> None:
        """
        Обрабатывает запрос на завершение текущей игры.
        Показывает диалог подтверждения и статистику игры при положительном ответе.
        Удаляет файл сохранения
        """
        if messagebox.askyesno("Завершение игры", "Вы уверены, что хотите завершить игру?"):
            try:
                os.remove("game_save.json")
                os.remove('game_state.json')
            except FileNotFoundError:
                pass
            self.update_history("Игра завершена.")
            self.show_game_stats()

    def quit_game(self) -> None:
        """
        Завершает работу приложения и удаляет файл состояния игры.
        """
        try:
            os.remove('game_state.json')
        except FileNotFoundError:
            pass
        self.root.quit()

    def make_move(self)  -> None:
        """
        Обрабатывает ход игрока:
        - Проверяет валидность введенного города
        - Проверяет соответствие первой буквы города последней букве предыдущего
        - Выполняет ход игрока и ответный ход компьютера
        - Обновляет историю игры
        - Проверяет условия завершения игры
        """
        city: str = self.entry.get().strip()
        self.entry.delete(0, tk.END)  # Очищает поле ввода после получения значения.

        if city not in self.game.cities_list:
            messagebox.showwarning("Ошибка", f"Города: {city} нет в списке!")
            if city in self.game.used_cities:
                messagebox.showwarning("Ошибка", f"Город: {city} уже был назван!")
                return
            return

        last_letter: str = self.game.last_letter().upper()
        if city[0].upper() != last_letter:
            messagebox.showwarning("Ошибка", f"Название города должно начинаться на {last_letter}!")
            return

        # Ход игрока
        if self.game.human_turn(city):
            self.update_history(f"Вы: {city}")

            # Ход компьютера
            if self.game.computer_turn():
                self.update_history(f"Компьютер: {self.game.last_city}")

            if self.game.check_game_over():
                self.show_game_stats()
                messagebox.showinfo("Конец игры", "Все города названы!")
                self.start_new_game()
        else:
            messagebox.showwarning("Ошибка", "Неверный ход!")

    def show_game_stats(self) -> None:
        """
        Отображает статистику текущей игры:
        - Подсчитывает очки игрока и компьютера
        - Формирует список использованных городов
        - Добавляет статистику в историю игры
        """

        # Получаем список использованных городов для игрока и компьютера
        player_cities: list[str] = [
            city for city in self.game.used_cities if city == self.game.last_city
        ]
        computer_cities: list[str] = [
            city for city in self.game.used_cities if city != self.game.last_city
        ]

        # Вычисляем количество использованных городов для игрока и компьютера
        player_score: int = len(player_cities)
        computer_score: int = len(computer_cities)

        # Формируем текст статистики
        stats_text: str = "\n" + "=" * 30 + "\n"
        stats_text += "СТАТИСТИКА ИГРЫ\n"
        stats_text += "=" * 30 + "\n\n"
        stats_text += f"Ваш счет: {player_score}\n"
        stats_text += f"Счет компьютера: {computer_score}\n\n"
        stats_text += "Использованные города:\n"
        stats_text += "\n".join(sorted(self.game.used_cities))
        stats_text += "\n" + "=" * 30 + "\n"

        # Добавляем статистику в историю игры
        self.history_text.insert(tk.END, stats_text)
        self.history_text.see(tk.END)

    def update_history(self, text: str) -> None:
        """
        Добавляет новую запись в историю игры.
        Args:
            text (str): Текст для добавления в историю
        """
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CityGameGUI(root)
    root.mainloop()
