import json
from requests.exceptions import JSONDecodeError
from pathlib import Path

from modules.bot.config import USER_SETTINGS_PATH
from utils.file_operations import utils_save_file, FileFormat
from modules.bot.config import Chat

def load_user_config(chat: Chat = None):
    if chat is None:
        raise TypeError("chat is None")

    print("\033[1m\033[94m[INFO] load_user_config >>>>\033[0m Загрузка пользовательской конфигурации")

    filepath = Path(USER_SETTINGS_PATH)

    if (filepath.exists()):
        try:
            with open(filepath, "r", encoding="utf-8") as settings_file:
                settings = json.load(settings_file)

                username = settings.get("username")

                if username is None:
                    print(f"\033[1m\033[91m[ERROR] load_user_config >>>>\033[0m Не удается найти имя пользователя в файле конфигурации {USER_SETTINGS_PATH} (username)")
                    return False

                chat.username = username

                context = settings.get("context")
                if context is None:
                    print(f"\033[1m\033[93m[WARN] load_user_config >>>>\033[0m Не удается найти контекст в файле конфигурации {USER_SETTINGS_PATH} (context)")

                chat.context.context = context

                return True
        except JSONDecodeError as ex:
            print("\033[1m\033[91m[ERROR] load_user_config >>>>\033[0m Ошибка при парсинге файла конфигурации в JSON", ex)
        except Exception as ex:
            print("\033[1m\033[91m[ERROR] load_user_config >>>>\033[0m Непредвиденная ошибка при чтении файла конфигурации", ex)
    else:
        print(f"\033[1m\033[91m[ERROR] load_user_config >>>>\033[0m Не удается найти файл конфигурации пользователя по пути {filepath}")
        return False


def save_user_config(chat: Chat = None):
    if chat is None:
        print(f"\033[1m\033[91m[ERROR] save_user_config >>>>\033[0m chat is None")
        return

    print("\033[1m\033[94m[INFO] save_user_config >>>>\033[0m Сохранение файла пользовательской конфигурации")

    path = Path(USER_SETTINGS_PATH)

    try:
        config_object = {
            "username": chat.username,
            "context": str(chat.context)
        }

        utils_save_file(path, FileFormat.JSON, config_object)
    except Exception as ex:
        print("\033[1m\033[91m[ERROR] save_user_config >>>>\033[0m Ошибка при сохранении файла пользовательской конфигурации", ex)