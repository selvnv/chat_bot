import json
from pathlib import Path
from enum import Enum

class FileFormat(Enum):
    JSON = "json"
    TEXT = "txt"

# Функция для сохранения файла
def utils_save_file(path: Path, format: str, data) -> bool:
    if not path.exists():
        print("\033[1m\033[93m[WARN] utils_save_file >>>>\033[0m Путь к файлу не существует. Попытка создать файл")
        try:
            path.touch()
        except Exception as ex:
            print("\033[1m\033[91m[ERROR] utils_save_file >>>>\033[0m Ошибка при создании файла", ex)
            return False


    if format == FileFormat.JSON:
        try:
            with path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as ex:
            print("\033[1m\033[91m[ERROR] utils_save_file >>>>\033[0m Ошибка при сохранении JSON файла")
            return False
    elif format == FileFormat.TEXT:
        try:
            with path.open("w", encoding="utf-8") as file:
                file.write(str(data))
        except Exception as ex:
            print("\033[1m\033[91m[ERROR] utils_save_file >>>>\033[0m Ошибка при сохранении текстового файла")
            return False
    else:
        print("\033[1m\033[91m[ERROR] utils_save_file >>>>\033[0m Неизвестный формат файла. Сохранение не будет выполнено")

    return True