from pprint import pformat, pprint
from marvel import small_dict

pprint(small_dict, sort_dicts=False)

## Задача 1

user_film = input("Введите название фильма или его часть")

result_film = ""

for film in small_dict.keys():
    if user_film.lower() in film.lower():
        result_film += film + ";\n"

print(f'По вашему запросу "{user_film}" нашлись фильмы: \n{result_film}')


## Задача 2

AGE = 2024

film_after2024 = ''
film_list = []
film_dict = {}
film_list_dict = []

for film, data in small_dict.items():
    if data is None:
        continue
    if data > AGE:

        film_after2024 += film + ", " #.1 

        film_list.append(film) #.2

        film_dict[film] = data #.3

        film_list_dict.append({film: data}) #.4 тут я сдался и включил Cody (

print("Фильмы после 2024г:", (film_after2024)) #.1
print("Фильмы после 2024г списком:", (film_list)) #.2
print("Фильмы после 2024г словарем:", pformat(film_dict)) #.3
print("Фильмы после 2024г списком словарей:", pformat(film_list_dict)) #.4

# result_film_one = {film for film in small_dict.keys() if user_film.lower() in film.lower()}
# print(result_film_one)

# user_film = {key:value for key, value in small_dict.items() if value == AGE}
# print(user_film)

# user_film_2 = {key:value for key, value in small_dict.items() if value is not None and value < AGE}
# pprint(user_film_2)

# user_film_2 = {key:value for key, value in small_dict.items() if isinstance(value, int) and value < AGE}
# pprint(user_film_2)

film_list_dict2 = [{key:value} for key, value in small_dict.items() if isinstance(value, int) and value > AGE]
pprint(film_list_dict2)