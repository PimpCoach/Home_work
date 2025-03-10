from pprint import pprint

from typing import List, Dict, Set, Any, Tuple

from marvel import full_dict as fd

# user_num = list(map(int, input("Введите цифры через пробел:").split()))
# print(user_num)

# dict_for_user_num = dict(filter(lambda id: id[0] in user_num, fd.items()))
# pprint(dict_for_user_num)

# director_movies: Set[str] = {movie[1]["director"] for movie in fd.items()}
# print(director_movies)

# full_dict_copy: Dict[int, Dict[str, Any]] = {
#     key: {**full_dict, "year": str(full_dict["year"])} for key, full_dict in fd.items()
# }

# pprint(full_dict_copy)

# dict_for_letter = dict(
#     filter(lambda film: film[1]["title"] and film[1]["title"][0] == "Ч", fd.items())
# )
# pprint(dict_for_letter)

# sorted_full_dict: List[Tuple[int, Dict[str, Any]]] = sorted(
#     fd.items(), key=lambda film: film[1]["director"]
# )
# pprint(sorted_full_dict)

# sorted_full_dict_2: List[Tuple[int, Dict[str, Any]]] = sorted(
#     fd.items(), key=lambda film: (film[1]["director"], film[1]["title"] or "")
# )
# pprint(sorted_full_dict_2)

sorted_dict_for_letter = dict(
    sorted(
        filter(
            lambda film: film[1]["title"] and film[1]["title"][0] == "Ч", fd.items()
        ),
        key=lambda film: film[1]["director"],
    )
)
pprint(sorted_dict_for_letter, sort_dicts=False)
