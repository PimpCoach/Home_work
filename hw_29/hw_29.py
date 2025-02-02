import os
from typing import Tuple

from PIL import Image
from pillow_heif import register_heif_opener


class ImageCompressor:
    """
    Класса для сжатия изображения в формате HEIF

    Attributes:
        supported_format (Tuple[str, ...]): Кортеж поддерживаемых форматов изображений.
        quality (int): Уровень качества сжатия изображения (от 1 до 100)
    """

    supported_format: Tuple[str, ...] = (".png", ".jpg", ".jpeg")

    def __init__(self, quality: int = 50) -> None:
        """
        Инициализирует компрессор изображений

        Args:
            quality (int): Уровень качества сжатия. По умолчанию 50
        """
        self.__quality = quality

    @property
    def quality(self) -> int:
        """
        Получает текущее значение качества сжатия.

        Returns:
            int: Текущий уровень качества сжатия.
        """
        return self.__quality

    # Устанавливаем новое значение качества сжатия
    @quality.setter
    def quality(self, quality: int) -> None:
        """
        Устанавливает новое значение качества сжатия.

        Args:
            quality (int): Новый уровень качества сжатия.

        Raises:
            ValueError: Если качество не в диапазоне от 1 до 100.
        """
        if not 0 < quality <= 100:
            raise ValueError("Качество должно быть от 0 до 100")
        self.__quality = quality

    def compress_image(self, input_path: str, output_path: str) -> None:
        """
        Сжимает изображение и сохраняет его в формате HEIF.

        Args:
            input_path (str): Путь к исходному изображению.
            output_path (str): Путь для сохранения сжатого изображения.

        Returns:
            None
        """
        with Image.open(input_path) as img:
            img.save(output_path, "HEIF", quality=self.__quality)
        print(f"Сжато: {input_path} -> {output_path}")

    def process_directory(self, directory: str) -> None:
        """
        Обрабатывает все изображения в указанной директории и её поддиректориях.

        Args:
            directory (str): Путь к директории для обработки.

        Returns:
            None
        """
        for root, _, files in os.walk(directory):
            for file in files:
                # Проверяем расширение файла
                if file.lower().endswith(self.supported_format):
                    input_path = os.path.join(root, file)
                    output_path = os.path.splitext(input_path)[0] + ".heic"
                    self.compress_image(input_path, output_path)

    def basic_process(self, input_path: str) -> None:
        """
        Основной процеес программы. Обрабатывает входной путь и запускает сжатие изображений.

        Args:
            input_path (str): Путь к файлу или директории для обработки.

        Returns:
            None
        """
        register_heif_opener()
        input_path = input_path.strip('"')  # Удаляем кавычки, если они есть

        if os.path.exists(input_path):
            if os.path.isfile(input_path):
                # Если указан путь к файлу, обрабатываем только этот файл
                print(f"Обрабатываем файл: {input_path}")
                output_path = os.path.splitext(input_path)[0] + ".heic"
                self.compress_image(input_path, output_path)
            elif os.path.isdir(input_path):
                # Если указан путь к директории, обрабатываем все файлы в ней
                print(f"Обрабатываем директорию: {input_path}")
                self.process_directory(input_path)
                # Функция process_directory рекурсивно обойдет все поддиректории
                # и обработает все поддерживаемые изображения
        else:
            print("Указанный путь не существует")


def main(user_input: str) -> None:
    """
    Главная функция программы.

    Args:
        user_input (str): Путь к файлу или директории, введенный пользователем.

    Returns:
        None
    """
    compressor = ImageCompressor()
    compressor.basic_process(user_input)


if __name__ == "__main__":
    user_input: str = input("Введите путь к файлу или директории: ")
    main(user_input)
