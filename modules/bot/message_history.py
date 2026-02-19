from modules.bot.config import Chat, MESSAGE_HISTORY_DIR
import json
from pathlib import Path
from utils.file_operations import FileFormat, utils_save_file


# Функция для сохранения истории сообщений
def save_message_history(chat: Chat = None) -> bool:
    if chat is None:
        print("\033[1m\033[91m[ERROR] >>>>\033[0m chat is None")
        return False

    username = chat.username
    message_history = chat.message_history
    message_history_ids = chat.message_history_ids

    if chat.message_count == 0:
        print("\033[1m\033[93m[WARN] >>>>\033[0m История сообщений пуста. Сохранение не будет выполнено")
        return False

    if username is None:
        print("\033[1m\033[91m[ERROR] >>>>\033[0m Пользователь для сохранения истории сообщений не известен")
        return False

    if message_history is None:
        print("\033[1m\033[91m[ERROR] >>>>\033[0m Не задана история сообщений для сохранения")
        return False

    if message_history_ids is None:
        print("\033[1m\033[91m[ERROR] >>>>\033[0m Не задан список идентификаторов для сопоставления истории сообщений с сохранением")
        return False

    message_history_object = {}
    filepath = Path(f"{MESSAGE_HISTORY_DIR}{username}.json")

    if (filepath.exists()):
        # Если уже есть сохраненные сообщения, нужно вычитать их в память и выполнить дозапись
        with filepath.open("r", encoding="utf-8") as file:
            message_history_object = json.load(file)

            if "message_history_ids" not in message_history_object:
                print("\033[1m\033[91m[ERROR] >>>>\033[0m В файле с сохраненной историей сообщений некорректная структура. Отсутствует поле 'message_history_ids'")
                return False

            if "message_history" not in message_history_object:
                print("\033[1m\033[91m[ERROR] >>>>\033[0m В файле с сохраненной историей сообщений некорректная структура. Отсутствует поле 'message_history'")
                return False

            for index, id in enumerate(message_history_ids):

                # Пропустить добавление элементов, которые уже есть в файле
                if id in message_history_object.get("message_history_ids"):
                    continue

                # Добавить элементы истории сообщений на запись
                message_history_object["message_history_ids"].append(id)
                message_history_object["message_history"].append(message_history[index])
    else:
        # Если файла с данными нет, все элементы истории сообщений пойдут в запись
        message_history_object["message_history_ids"] = message_history_ids
        message_history_object["message_history"] = message_history

    utils_save_file(filepath, FileFormat.JSON, message_history_object)

    return True
