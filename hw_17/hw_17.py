LOW_LVL = "начальный уровень знаний (от 1 до 3)"
MEDIUM_LVL = "средний уровень знаний (от 4 до 6)"
SUFFICIENT_LVL = "достаточный уровень знаний (от 7 до 9)"
HIGHER_LVL = "высокий уровень знаний (от 10 до 12)"


student_name = input("Введите имя")
if student_name.isalpha():
    name_title = student_name.title()
else:
    print("Введено некорректное значение.Пожалуйста, введите только имя")
    quit()


student_result = input("Введите оценку")
if student_result.isdigit():
    result_int = int(student_result)
    if result_int == 0:
        print(f"Студента {name_title} с оценкой {result_int} нужно отчислить")
    elif 1 <= result_int <= 3:
        print(f"Студент {name_title} с оценкой {result_int} имеет {LOW_LVL}")
    elif 4 <= result_int <= 6:
        print(f"Студент {name_title} с оценкой {result_int} имеет {MEDIUM_LVL}")
    elif 7 <= result_int <= 9:
        print(f"Студент {name_title} с оценкой {result_int} имеет {SUFFICIENT_LVL}")
    elif 10 <= result_int <= 12:
        print(f"Студент {name_title} с оценкой {result_int} имеет {HIGHER_LVL}")
else:
    print("Введено некорректное значение. Пожалуйста, введите число от 0 до 12")
