# Тестирования JSON
from files_utils import read_json, write_json, append_json

# #Читаем
# read_JSON = read_json("hw_24/test.json")
# print(read_JSON)

# #Перезаписываем
# write = {
#     "name": "Иван Петров",
#     "age": 25,
#     "isStudent": True,
#     "hobbies": [
#         "программирование",
#         "футбол",
#         "чтение"
#     ],
#     "address": {
#         "street": "ул. Ленина",
#         "house": 12,
#         "city": "Москва",
#         "zipCode": "123456"
#     }
# }
# write_json(write, "hw_24/test.json")

#Добавляем
apend = {
    "fiction": {
        "fantasy": ["Гарри Поттер", "Властелин колец"],
        "detective": ["Шерлок Холмс", "Пуаро"],
    },
    "non_fiction": {
        "science": ["Краткая история времени"],
        "biography": ["Стив Джобс"],
    },
}
append_json(apend, "hw_24/test.json")
