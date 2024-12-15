# Тестирования CSV
from files_utils import read_csv, write_csv, append_csv

# #Читаем
# read = read_csv('hw_24/test_csv.csv')
# print(read)

#Перезаписываем

# new_student_list = [
#     "Анатолий",
#     "Андреевич",
#     "Андреев",
# ]
# write = write_csv(new_student_list, 'hw_24/test_csv.csv')

#Добавляем

new_student_list = [
    "Василий",
    "Васильевич",
    "Васильев",
]

append = append_csv(new_student_list, 'hw_24/test_csv.csv')