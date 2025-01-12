from marvel import full_dict as fd

# user_num = list(map(int, input('Введите цифры через пробел:').split()))
# print(user_num)

# dict_for_user_num = dict(filter(lambda id: id[0] in user_num, fd.items()))
# print(dict_for_user_num)

director_movies = {movie[1]['director'] for movie in fd.items()}
print(director_movies)

full_dict_copy = {key: {**full_dict, 'year': str(full_dict['year'])} for key, full_dict in fd.items()}
print(full_dict_copy)
