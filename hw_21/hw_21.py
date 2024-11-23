from random import choice
from cities import cities_list as cl

city_set = set()

# for city in cl:
#     city_set.add((city["name"]))

city_set = {city['name'] for city in cl}




while True:
    print("Для выхода из игры напишите слово 'стоп'")
    user_input = input("Введите название города: ").capitalize()

    if user_input == "Стоп":
        print("Вы проиграли!")
        break

    if user_input not in city_set:
        print("Такого города не существует, либо он уже использован")
        continue


    city_set.remove(user_input)
    print("Ваш город", user_input)
    
    result = []
    for city in city_set:
        bad_letters = {'ь', 'ъ', 'ы', 'й'}

        if user_input[-1] in bad_letters:
            if city[0].lower() == user_input[-2]:
                result.append(city)

        elif city[0].lower() == user_input[-1]:
            result.append(city)
            
    if not result:
        print(f"Поздравляю! Вы победили! \nГородов на букву '{user_input[-1].capitalize()}' больше нет")
        break

    comp_city = choice(result)
    city_set.remove(comp_city)
    print("Город соперника:", comp_city)

