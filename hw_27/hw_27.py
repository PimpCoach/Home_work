import asyncio
import openai
import os
import json

from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

from hw_27_data import DATA

MY_KEY_VSE_GPT = os.getenv("MY_KEY_VSE_GPT")
BASE_URL = os.getenv("BASE_URL", "https://api.vsegpt.ru/v1")

MAX_CHUNKS_SIZE = 5000  # Максимальная длина текста для 1 запроса
SLEEP_TIME = 4  # Задержка между запросами
OUTPUT_FILE = "Lection.md"  # Файл в котором будет конспект

PROMPT_THEME = """
Привет!

Определи общую тему  текста. И постарайся максимально полно и точно описать её,
с использованием пунктов и подпунктов.

Не додумывай того, чего там небыло.
Исключи small talks.
"""

PROMPT_TIMESTAMPS = """
Привет!

Ты - ассистент по созданию таймкодов для видео.
Тебе будет предоставлен текст с таймкодами из видео.
Твоя задача - создать краткое описание каждого смыслового блока.
Ты не должен использовать полное цитирование. Создай краткое описание для блока.
Каждый блок должен начинаться с таймкода в формате чч:мм:сс.
Описание должно быть одним предложением, передающим суть начинающегося отрезка.
Игнорируй слишком короткие фрагменты или паузы.
Объединяй связанные по смыслу части в один большой блок.
Описания должны быть в стиле, как это обычно делают на youtube.



ВАЖНО.
СТРОГИЕ ПРАВИЛА:
1. Для видео длительностью:
   - до 30 минут: максимум 5 таймкодов
   - 30-60 минут: максимум 8 таймкодов
   - 1-2 часа: максимум 10 таймкодов
   - 2+ часа: максимум 15 таймкодов

2. Минимальный интервал между таймкодами:
   - для коротких видео (до 30 мин): 3-5 минут
   - для длинных видео: 10-15 минут

3. Объединяй близкие по смыслу темы в один таймкод

ВАЖНО: Если ты превысишь количество таймкодов - твой ответ будет отклонён!

В твоём ответе должны быть только таймкоды и описания.
Никаких других комментариев или пояснений.

КАК ПИСАТЬ?

Ты не пишешь описательные, длинные предложения. 
Вроде: "Пояснение адаптивного подхода к верстке на примере Visual Studio Code, где контент перестраивается в зависимости от размера экрана. "

Ты пишешь короткий, ёмкий вариант.
"Адаптивный подход к вёрстке. Пример в Visual Studio Code. Контент перестраивается в зависимости от размера экрана."
Или даже ещё немного короче.

Спасибо!
"""

PROMPT_CONSPECT_WRITER = """
Привет!
Ты опытный технический писатель. Ниже, я предоставляю тебе полный текст лекции а так же ту часть,
с которой ты будешь работать.

Ты великолепно знаешь русский язык и отлично владеешь этой темой.

Тема занятия: {topic}

Полный текст лекции:
{full_text}

Сейчас я дам тебе ту часть, с котороый ты будешь работать. Я попрошу тебя написать конспект лекции.
А так же блоки кода.

Ты пишешь в формате Markdown. Начни с заголовка 2го уровня.
В тексте используй заголовки 3го уровня.

Используй блоки кода по необходимости.

Отрезок текста с которым ты работаешь, с которого ты будешь работать:
{text_to_work}
"""

client = AsyncOpenAI(api_key=MY_KEY_VSE_GPT, base_url=BASE_URL)
model_gpt = "openai/gpt-4o-mini"  # Идентификатор используемой модели
max_tokens_gpt = 16000  # Максимальное количество жетонов, которое может быть сгенерировано в завершении чата. Это значение можно использовать для контроля стоимости текста.
temperature_gpt = 0.4  # Температура выборки (фантазия) может использоваться, от 0 до 2


async def get_ai_request(prompt: str, max_retries: int = 3, base_delay: float = 2.0):
    """
    Отправляет запрос к API с мехаизмом повторных попыток
    base_delay - начальная задержка, которая будет увеличиваться экспонециально
    :param prompt: текст запроса
    :param max_retries: максимальное количество попыток
    :param base_delay: начальная задержка между попытками
    :return: ответ от API
    :except RateLimitError: обработка ошибки превышения лимита запроса
    :except APITimeoutError: обработка ошибки таймаут запроса
    :except APIConnectionError: обработка ошибки ошибки соединения

    """
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=model_gpt,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens_gpt,
                temperature=temperature_gpt,
            )
            return response.choices[0].message.content

        except openai.RateLimitError:
            if attempt == max_retries - 1:  # Проверяем не последняя ли это попытка
                raise  # если последняя, то отдаем ошибку наружу
            delay = base_delay * (
                2**attempt
            )  # Если не последнняя, то делаем экспоненциальное увеличение время задержки
            await asyncio.sleep(delay)  # ждем перед следующей попыткой

        except openai.APITimeoutError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2**attempt)
            await asyncio.sleep(delay)

        except openai.APIConnectionError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2**attempt)
            await asyncio.sleep(delay)


def split_text_to_chunks(data: list) -> list:
    """
    Разбивает текст на куски не более чем MAX_CHUNKS_SIZE символов
    """
    chunks = []
    current_chunk = ""

    for item in data:
        text = item["text"]  # Берем текст из списка словарей с ключем 'text'
        if len(current_chunk) + len(text) <= MAX_CHUNKS_SIZE:
            current_chunk += text  # Если новый текст поместится в текущий, то добавляем его к 'current_chunk" и копим до длины MAX_CHUNK_SIZE
        else:
            if current_chunk:  # Если не помещается, то сохраняем накопленный текст в список chunks
                chunks.append(current_chunk)
            current_chunk = text  # Начинаем новый current_chunk с текущего места

    if current_chunk:  # Проверяем остался ли еще текст и если да, то сохраняем в список current_chunk
        chunks.append(current_chunk)

    return chunks


def save_to_markdown(timestamps: str, theme: str, chunks: list):
    """
    Сохраняет результаты в markdown файл
    :param timestamps - таймкоды
    :theme - темы
    :chunks - куски конспекта от сервера

    """
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Таймкод\n\n")
        f.write(timestamps)
        f.write("\n\n---\n\n")

        f.write("# Тема\n\n")
        f.write(theme)
        f.write("\n\n---\n\n")

        f.write("# Конспект\n\n")
        for chunk in chunks:
            f.write(chunk)
            f.write("\n\n---\n\n")


def second_to_timecode(seconds: float) -> str:
    """
    Конвертирует секунды в таймкод
    """
    if seconds is None:
        return "00:00:00"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def add_timestamp_text(data: list[dict]) -> list[dict]:
    """
    Добавляет в словарь ключи 'timestamp_text'
    """
    for item in data:
        start_time = second_to_timecode(item["timestamp"][0])
        end_time = second_to_timecode(item["timestamp"][1])
        item["timestamp_text"] = [start_time, end_time]
    return data


async def main():

    full_data = add_timestamp_text(DATA)  # Добавление ключа 'timestamp_text'
    full_data_json_string = json.dumps(full_data)  # Преобразуем данные в JSON

    timestamps_task = asyncio.create_task(
        get_ai_request(PROMPT_TIMESTAMPS + full_data_json_string)
    )  # Создание асинхронной задачи для таймкодов
    theme_task = asyncio.create_task(
        get_ai_request(PROMPT_THEME + full_data_json_string)
    )  # Создание асинхронной задачи для тем

    chunks = split_text_to_chunks(
        full_data
    )  # Разбивка текста на меньшие части не дожидаясь выполнения задач

    timestamps = await timestamps_task  # Ожидание получения таймкодов
    theme = await theme_task  # Ожидание получения тем

    chunk_tasks = (
        []
    )  # Список для хранния асинхронных задач для обработки каждого куска текста
    for chunk in chunks:
        prompt = PROMPT_CONSPECT_WRITER.format(
            topic=theme, full_text=full_data_json_string, text_to_work=chunk
        )
        task = asyncio.create_task(get_ai_request(prompt))
        chunk_tasks.append(task)

    result = await asyncio.gather(*chunk_tasks)  # Ожидание выполнения всех задач
    save_to_markdown(timestamps, theme, result)  # Сохраняем в файл


if __name__ == "__main__":
    asyncio.run(main())
