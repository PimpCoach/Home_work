from marvel import full_dict as fd

user_num = list(map(int, input('Введите цифры через пробел:').split()))
print(user_num)

DictForUserNum = dict(filter(lambda id: id[0] in user_num, fd.items()))
print(DictForUserNum)