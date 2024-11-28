from random import choice
from cities import cities_list as cl

city_set = set()
city_set = {city['name'] for city in cl}

last_city = ''

bad_letters = set()
sym_lower_set = set(
    " ".join(city_set).lower()
)

count = 0

for letter in sym_lower_set:
    for city in city_set:
        first_letter = city[0]
        count += 1
        if letter.lower() == first_letter.lower():
            break
    else:
        bad_letters.add(letter)


while True:
    print("Для выхода из игры напишите слово 'стоп'")
    user_input = input("Введите название города: ").title()

    if user_input == "Стоп":
        print("Вы проиграли!")
        break

    if last_city:
        last_letter = last_city[-1]

        if last_letter in bad_letters:
            last_letter = last_city[-2]

        if user_input[0].lower() != last_letter:
            print(f'Город должен начинаться на букву "{last_letter.upper()}"')
            continue

    if user_input not in city_set:
        print("Такого города не существует, либо он уже использован")
        continue

    city_set.remove(user_input)
    print("Ваш город", user_input)
    
    result = []
    for city in city_set:

        if user_input[-1] in bad_letters:
            if city[0].lower() == user_input[-2]:
                result.append(city)

        elif city[0].lower() == user_input[-1]:
            result.append(city)
            
    if not result:
        print(f"Поздравляю! Вы победили! \nГородов на букву '{user_input[-1].title()}' больше нет")
        break

    comp_city = choice(result)
    city_set.remove(comp_city)
    last_city = comp_city
    print("Город соперника:", comp_city)

