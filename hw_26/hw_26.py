import re
from typing import Callable, Any 

# Декоратор для проверки пароля
def password_checker(func: Callable):
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

