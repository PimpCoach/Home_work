import tkinter as tk
from tkinter import messagebox
from hw_31 import JsonFile, CitiesSerializer, CityGame


class CityGameGUI:
    """
    Графический интерфейс игры в города.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Игра в города")
        self.root.geometry("600x400")

        # Инициализация игровой логики
        json_file = JsonFile("cities.json")
        cities_serializer = CitiesSerializer(json_file.read_data())
        self.game = CityGame(cities_serializer)

        # Создание элементов интерфейса
        self.create_widgets()

        # Начало игры
        self.start_new_game()

    def create_widgets(self):
        # Фрейм для истории игры
        history_frame = tk.Frame(self.root)  # Контейнер для истории игры
        history_frame.pack(pady=15)  # Отступ сверху и снизу

        self.history_text = tk.Text(
            history_frame, height=15, width=60
        )  # Текстовое поле для истории игры
        self.history_text.pack(
            side=tk.LEFT
        )  # Расположение слева текстового поля. side=tk.LEFT - расположение слева

        scrollbar = tk.Scrollbar(history_frame)  # Полоса прокрутки
        scrollbar.pack(
            side=tk.RIGHT, fill=tk.Y
        )  # Расположение справа текстового поля. fill=tk.Y - растяжение по вертикали

        self.history_text.config(
            yscrollcommand=scrollbar.set
        )  # Связывает текстовое поле с полосой прокрутки
        scrollbar.config(
            command=self.history_text.yview
        )  # command - связывает полосу прокрутки с текстовым полем

        # Поле ввода
        input_frame = tk.Frame(self.root)  # Контейнер для поля ввода
        input_frame.pack(pady=10)  # Создает отступ сверху и снизу

        self.entry = tk.Entry(input_frame, width=50)  # Поле ввода
        self.entry.pack(
            side=tk.LEFT, padx=10
        )  # Расположение слева текстового поля. padx= - отступ слева и справа

        submit_button = tk.Button(
            input_frame, text="Ответить", command=self.make_move
        )  # Кнопка для ответа. command - связывает нажатие кнопки с методом make_move
        submit_button.pack(
            side=tk.LEFT
        )  # Расположение слева от оставшевогося свободного места

        # Кнопки управления
        control_frame = tk.Frame(self.root)  # Контейнер для кнопок управления
        control_frame.pack(pady=15)  #  Создает отступ сверху и снизу

        new_game_button = tk.Button(
            control_frame, text="Новая игра", command=self.start_new_game
        )  # Кнопка для новой игры. command - связывает нажатие кнопки с методом start_new_game
        new_game_button.pack(
            side=tk.LEFT, padx=5
        )  # Раасположение слева от оставшевогося свободного места

        finish_button = tk.Button(control_frame, text='Закончить игру', command=self.stop_game)  # Кнопка для завершения игры. command - связывает нажатие кнопки с методом stop_game
        finish_button.pack(side=tk.LEFT, padx=5)  # Раасположение слева от оставшевогося свободного места

        quit_button = tk.Button(
            control_frame, text="Выход", command=self.root.quit
        )  # Кнопка для выхода. command - связывает нажатие кнопки с методом quit
        quit_button.pack(
            side=tk.RIGHT, padx=100
        )  # Раасположение слева от оставшевогося свободного места

    def start_new_game(self):
        self.game.used_cities.clear() # Очищает список использованных городов.
        self.game.last_city = "" # Сбрасывает последний город.
        self.game.cities_list = self.game._city_list() # Получает список всех доступных городов.
        self.history_text.delete(1.0, tk.END) # Очищает текстовое поле. 1.0 - начало текста. tk.END - конец текста. Удаляет все символы от начала до конца.
        self.game.start_game() # Запускает игру.
        self.update_history(f"Компьютер: {self.game.last_city}") # Отображает первый ход компьютера.

    def stop_game(self):
        if messagebox.askyesno("Завершение игры", "Вы уверены, что хотите завершить игру?"):
            self.show_game_stats()

    def make_move(self):
        city = self.entry.get().strip()
        self.entry.delete(0, tk.END) # Очищает поле ввода после получения значения.
        
        if city not in self.game.cities_list:
            messagebox.showwarning("Ошибка", f"Города: {city} нет в списке!")
            if city in self.game.used_cities:
                messagebox.showwarning("Ошибка", f"Город: {city} уже был назван!")
                return
            return
        
        last_letter = self.game.last_letter().upper()
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

    def show_game_stats(self):
        # Получаем список использованных городов для игрока и компьютера
        player_cities = [city for city in self.game.used_cities if city != self.game.last_city]
        computer_cities = [city for city in self.game.used_cities if city == self.game.last_city]

        # Вычисляем количество использованных городов для игрока и компьютера
        player_score = len(player_cities)
        computer_score = len(computer_cities)

        # Формируем текст статистики
        stats_text = "\n" + "=" * 30 + "\n"
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

    def update_history(self, text):
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CityGameGUI(root)
    root.mainloop()
