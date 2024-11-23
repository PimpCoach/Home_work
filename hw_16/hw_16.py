# Задание №1: Конвертация секунд
response = int(input("Введите количество секунд"))
hour = response // 3600 
minute = response % 3600 // 60 
second = response % 3600 % 60
print(f"В {response} секундах:\n часов: {hour}\n минут: {minute}\n секунд: {second}")

# Задание №2: Конвертация температуры
response_temp = float(input("Введите температуру в градусах °C"))
temp_c = round(response_temp, 2)
temp_k = temp_c + 273.15
temp_f = temp_c * 9 / 5 + 32
temp_r = temp_c * 4 / 5
print(
    f"Если температура в Цельсиях равна {temp_c}°C, то: \n в Кельвинах: {temp_c}°C + 273.15 = {round(temp_k, 2)}K \n в Фаренгейтах: {temp_c}°C * 9/5 + 32 = {round(temp_f, 2)}°F \n в Реомюрах: {temp_c}°C * 4/5 = {round(temp_r, 2)}°Ré"
)
