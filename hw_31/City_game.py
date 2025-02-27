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
        
        # Тип противника
        self.opponent_type: str = "computer"

        # Инициализация игровой логики
        json_file = JsonFile("cities.json")
        cities_serializer = CitiesSerializer(json_file.read_data())
        self.game = CityGame(cities_serializer)

        # Создание элементов интерфейса
        self.create_widgets()

        # Добавляем приветствие
        welcome_text = "Добро пожаловать в игру 'Города'!\n\n"
        self.history_text.insert(tk.END, welcome_text, "stats")

        # Инструкции
        instructions = "Для начала игры нажмите 'Новая игра' или 'Загрузить игру'\n"
        instructions += "Для выхода нажмите 'Выход'\n"
        self.history_text.insert(tk.END, instructions, "system")
        
        # Блокируем поле ввода и кнопку ответа, сохранить и закончить при запуске приложения
        self.entry.config(state='disabled')
        self.submit_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.finish_button.config(state='disabled')

        # Инициализация игроков
        self.player1_name: str = "Игрок 1"
        self.player2_name: str = "Игрок 2"
        self.current_player: int = 1

        # Настройка цветовых тегов для текста
        self.history_text.tag_config("player1", foreground="blue")
        self.history_text.tag_config("player2", foreground="red")
        self.history_text.tag_config("computer", foreground="green")
        self.history_text.tag_config("system", foreground="purple")
        self.history_text.tag_config("error", foreground="red", font=("Arial", 10, "bold"))
        self.history_text.tag_config("stats", foreground="dark blue", font=("Arial", 10, "bold"))

    def choose_opponent(self) -> None:
        """
        Выбор типа противника (компьютер или человек).
        """
        choice_window = tk.Toplevel(self.root) # Создаем новое окно
        choice_window.title("Выбор противника")
        choice_window.geometry("300x150")

        tk.Label(choice_window, text="Выберите противника:", anchor='center', justify='center').pack(expand=True, fill='both') 

        def set_opponent(opponent: str) -> None:
            """
            Устанавливает тип противника и закрывает окно выбора.
            Args:
                opponent (str): Тип противника (компьютер или человек).
            """
            self.opponent_type = opponent
            choice_window.destroy()
            if opponent == "human":
                self.get_player_name()
            else:
                self.start_new_game()

        tk.Button(choice_window, text="Играть с компьютером", command=lambda: set_opponent("computer")).pack(side=tk.LEFT, padx=6, pady=20)
        tk.Button(choice_window, text="Играть с человеком", command=lambda: set_opponent("human")).pack(side=tk.RIGHT, padx=6, pady=20)

    def get_player_name(self) -> None:
        """
        Получает имена игроков от пользователя.
        """
        name_window = tk.Toplevel(self.root)
        name_window.title("Введите имена игроков")
        name_window.geometry("300x150")

        tk.Label(name_window, text="Введите имя первого игрока:", anchor='center', justify='center').pack(expand=True, fill='both')
        player1_entry = tk.Entry(name_window)
        player1_entry.pack()

        tk.Label(name_window, text="Введите имя второго игрока:", anchor='center', justify='center').pack(expand=True, fill='both')
        player2_entry = tk.Entry(name_window)
        player2_entry.pack()

        def save_names() -> None:
            """
            Сохраняет имена игроков и закрывает окно ввода имен.
            """
            player1: str = player1_entry.get().strip()
            player2: str = player2_entry.get().strip()

            self.player1_name = player1 if player1 else "Игрок 1"
            self.player2_name = player2 if player2 else "Игрок 2"

            name_window.destroy()
            self.start_new_game()

        tk.Button(name_window, text="Начать игру", command=save_names).pack(pady=10)

    def create_widgets(self) -> None:
        """
        Создает и размещает все элементы графического интерфейса:
        - Текстовое поле для истории игры со скроллбаром
        - Поле ввода и кнопка ответа
        - Кнопки управления (новая игра, завершение, сохранить, загрузить, выход)
        """
        # Создание фрейма для истории игры
        history_frame = tk.Frame(self.root)  
        history_frame.pack(pady=15)  
        # Текстовое поле для истории игры
        self.history_text = tk.Text(history_frame, height=15, width=60)  
        self.history_text.pack(side=tk.LEFT)  
        # Полоса прокрутки
        scrollbar = tk.Scrollbar(history_frame)  
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  
        self.history_text.config(yscrollcommand=scrollbar.set)  # Связывает текстовое поле с полосой прокрутки
        scrollbar.config(command=self.history_text.yview)  # command - связывает полосу прокрутки с текстовым полем

        # Создание фрейма для поля ввода и кнопки ответа
        input_frame = tk.Frame(self.root)  
        input_frame.pack(pady=10) 
        self.entry = tk.Entry(input_frame, width=50)  # Поле ввода
        self.entry.pack(side=tk.LEFT, padx=10)  
        self.entry.bind('<Return>', lambda event: self.make_move()) # Связывает нажатие клавиши Enter 
        self.submit_button = tk.Button(input_frame, text="Ответить", command=self.make_move)  # Кнопка для ответа
        self.submit_button.pack(side=tk.LEFT)  

        # Кнопки управления
        control_frame = tk.Frame(self.root)  
        control_frame.pack(pady=15) 
        new_game_button = tk.Button(control_frame, text="Новая игра", command=self.choose_opponent)  
        new_game_button.pack(side=tk.LEFT, padx=16)  
        self.finish_button = tk.Button(control_frame, text="Закончить игру", command=self.stop_game)  
        self.finish_button.pack(side=tk.LEFT, padx=16)  
        self.save_button = tk.Button(control_frame, text="Сохранить игру", command=self.save_game) 
        self.save_button.pack(side=tk.LEFT, padx=16)
        load_button = tk.Button(control_frame, text="Загрузить игру", command=self.load_game) 
        load_button.pack(side=tk.LEFT, padx=16)
        quit_button = tk.Button(control_frame, text="Выход", command=self.quit_game)  
        quit_button.pack(side=tk.RIGHT, padx=16) 
        
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
            "history": self.history_text.get(1.0, tk.END),
            "opponent_type": self.opponent_type,
            "current_player": self.current_player,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name
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
            self.opponent_type = game_state["opponent_type"]
            self.current_player = game_state["current_player"]
            self.player1_name = game_state["player1_name"]
            self.player2_name = game_state["player2_name"]

            self.history_text.delete(1.0, tk.END)

            if self.opponent_type == "human":
                curent_player_name = self.player1_name if self.current_player == 1 else self.player2_name
                self.update_history('\nИгра загружена.')
                self.update_history(f'\nИгрок {curent_player_name} ходит.')
            else:
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
        self.game.cities_list = self.game._city_list()  # Получает список всех доступных городов.
        self.history_text.delete(1.0, tk.END)  # Очищает текстовое поле. 1.0 - начало текста. tk.END - конец текста. Удаляет все символы от начала до конца.
        self.current_player = 1  # Устанавливает текущего игрока на 1.

        if self.opponent_type == 'computer':
            self.game.start_game()  # Запускает игру.
            self.update_history(f"Компьютер: {self.game.last_city}", "computer")  # Отображает первый ход компьютера.
            self.update_history(f"Назовите город на букву: {self.game.last_letter().upper()}", "system")  # Отображает последнюю букву.
        else:
            self.update_history(f'Игра началась! Ход игрока: {self.player1_name}', "player1")
        
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

        if self.game.last_city and len(self.game.last_city) > 0:
            last_letter: str = self.game.last_letter().upper()
            if city[0].upper() != last_letter:
                messagebox.showwarning("Ошибка", f"Название города должно начинаться на {last_letter}!")
                return
        
        if self.opponent_type == 'computer':
            # Ход игрока
            if self.game.human_turn(city):
                self.update_history(f"Вы: {city}", 'player1')
                # Ход компьютера
                if self.game.computer_turn():
                    self.update_history(f"Компьютер: {self.game.last_city}", "computer")
                    
        else:
            # Если играют два игрока
            if self.game.human_turn(city):
                current_player_name: str = self.player1_name if self.current_player == 1 else self.player2_name
                player_tag = 'player1' if self.current_player == 1 else 'player2'
                self.update_history(f"{current_player_name}: {city}", player_tag)
                self.game.last_city = city
                self.current_player = 2 if self.current_player == 1 else 1
                next_player_name: str = self.player1_name if self.current_player == 1 else self.player2_name
                self.update_history(f"Ход игрока: {next_player_name}")

        self.update_history(f"Назовите город на букву: {self.game.last_letter().upper()}")

        if self.game.check_game_over():
            self.show_game_stats()
            messagebox.showinfo("Конец игры", "Все города названы!")
            self.start_new_game()

    def show_game_stats(self) -> None:
        """
        Отображает статистику текущей игры:
        - Подсчитывает очки игрока и компьютера
        - Формирует список использованных городов
        - Добавляет статистику в историю игры
        """

        # Формируем текст статистики
        stats_text: str = "\n" + "=" * 30 + "\n"
        self.history_text.insert(tk.END, stats_text)

        self.history_text.insert(tk.END, "Статистика игры:\n", 'stats')
        self.history_text.insert(tk.END, "=" * 30 + "\n\n")

        if self.opponent_type == 'computer':
            # Получаем список использованных городов для игрока и компьютера
            player_cities: list[str] = [city for city in self.game.used_cities if city == self.game.last_city]
            computer_cities: list[str] = [city for city in self.game.used_cities if city != self.game.last_city]
            self.history_text.insert(tk.END, f"Ваш счет: {len(player_cities)}\n", "player1")
            self.history_text.insert(tk.END, f"Счет компьютера: {len(computer_cities)}\n\n", "computer")
        else:
            self.history_text.insert(tk.END, f"Счет {self.player1_name}: {len([city for city in list(self.game.used_cities)[::2]])}\n", "player1")
            self.history_text.insert(tk.END, f"Счет {self.player2_name}: {len([city for city in list(self.game.used_cities)[1::2]])}\n", "player2")

        self.history_text.insert(tk.END, "Использованные города:\n", "system")
        self.history_text.insert(tk.END, ", ".join(sorted(self.game.used_cities)) + "\n", 'system')
        self.history_text.insert(tk.END, "=" * 30 + "\n")
        self.history_text.see(tk.END)

    def update_history(self, text: str, player: str = 'system') -> None:
        """
        Добавляет новую запись в историю игры с указанным цветом.
        Args:
            text (str): Текст для добавления в историю
            player (str): Тип игрока ('player1', 'player2' или 'system')
        """
        self.history_text.insert(tk.END, text + "\n", player)
        self.history_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CityGameGUI(root)
    root.mainloop()
