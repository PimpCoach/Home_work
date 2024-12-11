from urllib import response
import requests
from plyer import notification

API_KEY = r'3440a26919393963464f0b9a933243ef' 
CITY = 'Пермь' 


# Получим данные о погоде в формате JSON
def get_weather(city: str, api_key: str) -> dict:
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    responce = requests.get(url)
    return responce.json()

# Забираем из JSON данные о погоде которые нужны
def format_weather_message(data: dict) -> str:
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']
    return(f'Температура: {temp}°C по ощущению {feels_like}°C \n{description}\nветер {wind_speed}м/с\nдавление {pressure}мм рт. ст., влажность {humidity}%')

# Отправляем уведомление о погоде на компьютер
def notify_weather(message: str) -> None:
    notification.notify(
        title=f'Погода в {CITY}',
        message=message,
        app_name="Погода",
        app_icon=None)

# Запускаем функции
def main() -> None:
    weather_JSON = get_weather(CITY, API_KEY)
    weather_message = format_weather_message(weather_JSON)
    notify_weather(weather_message)
main()