from file_classes import JsonFile, TxtFile, CsvFile

if __name__ == "__main__":
    # Тест для JSON

    # Читаем
    json_file = JsonFile("test.json")
    print(f"Читаем JSON файл: {json_file.read()}")

    # Перезаписываем
    data_dict = {
        "name": "Василий Васильевич",
        "age": 22,
        "isStudent": False,
        "hobbies": ["спать", "лежать", "сидеть"],
        "address": {
            "street": "ул. Тестовая",
            "house": 6,
            "city": "Москва",
            "zipCode": "33442",
        },
    }
    json_file.write(data_dict)
    print(f"Читаем перезаписанный JSON файл: {json_file.read()}")

    # Добавляем
    data_dict = {
        "fiction": {
            "fantasy": ["Гарри Поттер", "Властелин колец"],
            "detective": ["Шерлок Холмс", "Пуаро"],
        },
        "non_fiction": {
            "science": ["Краткая история времени"],
            "biography": ["Стив Джобс"],
        },
    }
    json_file.append(data_dict)
    print(f"Читаем JSON файл в который добавили данные: {json_file.read()}")

    # Тест для TXT

    # Читаем
    txt_file = TxtFile("test.txt")
    print(f"Читаем TXT документ: {txt_file.read()}")

    # Перезаписываем
    data = "Новая запись для теста\n"
    txt_file.write(data)
    print(f"Читаем перезаписанный TXT документ: {txt_file.read()}")

    # Добавляем
    data = "Новая запись для добавление в документ\n"
    txt_file.append(data)
    print(f"Читаем TXT документ в который добавили запись: {txt_file.read()}")

    # Тест для CSV

    # Читаем
    csv_file = CsvFile("test.csv")
    print(f"Читаем CSV документ: {csv_file.read()}")

    # Перезаписываем
    data = ["Новая", "запись", "для", "теста"]
    csv_file.write(data)
    print(f"Читаем перезаписанный CSV документ: {csv_file.read()}")

    # Добавляем
    data = ["добавил", "ещё", "запись", "тест"]
    csv_file.append(data)
    print(f"Читаем CSV документ в который добавили запись: {csv_file.read()}")
