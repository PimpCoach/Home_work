import re
import csv
from typing import Callable, Any

# Декоратор для проверки пароля
def password_checker(func: Callable):

    #Внутрення функиця декоратора, которая проверяет пароль
    def wrapper(args: Any):
        
        # Минимальная длина
        if len(args) < 8:
            return "Пароль должен содержать как минимум 8 символов"

        # Наличие цифры
        if not re.search(r'[0-9]', args):
            return "Пароль должен собержать как минимум 1 цифру"
        
        # Наличие заглавной буквы
        if not re.search(r"[A-Z]", args):
            return "Пароль должен содержать как минимум 1 заглавную букву"
        
        # Наличие строчной буквы
        if not re.search(r'[a-z]', args):
            return 'Пароль должен содержать как минимум 1 строчную букву'
        
        # Наличие спец символа
        if not re.search(r'[!, @, #, $, /, ?, |]', args):
            return 'Паролько должен содержать как минимум 1 спец символ !, @, #, $, /, ?, |'
        
        return func(args)
    
    return wrapper

#Декорируемая функция, которая возращает сообщение об успешной проверке, если пароль соответвует всем критериям
@password_checker
def register_user(password):
    return f"Пароль {password} прошел проверку"

#Принты для проверки разных вариантов паролей
print(register_user('qwerty'))
print(register_user('qwertyyy'))
print(register_user('qwerty123'))
print(register_user('Qwerty123'))
print(register_user('Qwerty123!'))


#Часть 2: Декораторы для валидации данных

#Декоратор для проверки пароля с параметрами по умолчанию
def password_validator(min_lenght: int = 8, min_number: int = 1, min_uppercase: int = 1, min_lowercase: int = 1, min_special_chars: int = 1):

    def password_checker(func: Callable):

        #Внутрення функиця декоратора, которая проверяет пароль
        def wrapper(*args: Any):
            
            # Минимальная длина
            if len(args[1]) < min_lenght:
                raise ValueError (f"Пароль должен содержать минимум {min_lenght} символов")

            # Наличие цифры
            if sum(num.isdigit() for num in args[1]) < min_number:
                raise ValueError (f"Пароль должен собержать минимум {min_number} цифр")
            
            # Наличие заглавной буквы
            if sum(letter.isupper() for letter in args[1]) < min_uppercase:
                raise ValueError (f"Пароль должен содержать минимум {min_uppercase} заглавную букву")
            
            # Наличие строчной буквы
            if sum(letter.islower() for letter in args[1]) < min_lowercase:
                raise ValueError (f'Пароль должен содержать  минимум {min_lowercase} строчную букву')
            
            # Наличие спец символа
            if sum(not chars.isalnum() for chars in args[1]) < min_special_chars:
                raise ValueError (f'Паролько должен содержать минимум {min_special_chars} спец символ')
            
            return func(*args)
        
        return wrapper

    return password_checker

# Декоратор для проверки чтобы в имени пользователя небыло пробелов
def username_validator(func: Callable):

    def wrapper(*args):
        if ' ' in args[0]:
            raise ValueError(f"Имя пользователя '{args[0]}' содержит пробелы")
        return func(*args)
    return wrapper

# Проверяет пароль
@password_validator()
# Проверяет имя
@username_validator
# функция для дозаписи имя пользователя и его пароля в CSV файл
def register_user_csv(username: str, password: str):
    with open('user.csv', 'a', encoding= 'utf-8-sig') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([username, password])

#Тестирование успешного случая
try:
    register_user_csv('Анатолий', 'Qwerty123!')
    print('Регистрация прошла успешно')
except ValueError as e:
    print(f'Ошибка: {e}')

# Тестирование неудачного случая по паролю...
try:
    register_user_csv('Анатолий', 'qwerty12!')
    print('Регистрация прошла успешно')
except ValueError as e:
    print(f'Ошибка: {e}')

# Тестирование неудачного случая по юзернейму...
try:
    register_user_csv('Анат олий', 'Qwerty123!')
    print('Регистрация прошла успешно')
except ValueError as e:
    print(f'Ошибка: {e}')
