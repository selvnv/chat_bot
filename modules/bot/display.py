import json

from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme

from pathlib import Path

from modules.bot.config import DISPLAY_MESSAGE_HISTORY_COUNT
from modules.bot.config import Chat

def _print_markdown_message(message: str = ""):
    if len(message) == 0:
        print("\033[1m\033[93m[WARN] _print_markdown_message >>>>\033[0m Нет данных для отображения")

    console = Console(theme=Theme({
        "markdown.h1": "bold bright_magenta",
        "markdown.h2": "bold bright_cyan",
        "markdown.h3": "bold bright_green",
        "markdown.h4": "bold bright_yellow",
        "markdown.h5": "bold bright_blue",
        "markdown.h6": "bold bright_red",
        "markdown.strong": "bold bright_white",
        "markdown.emphasis": "italic bright_cyan",
        "markdown.strike": "strike bright_black",
        "markdown.code": "bright_green on grey11",
        "markdown.code_block": "bright_yellow on grey0",
        "markdown.link": "underline bright_blue",
        "markdown.link_url": "italic bright_cyan",
        "markdown.block_quote": "dim bright_magenta",
    }))

    markdown_text = Markdown(message)

    console.print(markdown_text)


def _print_message_history(username: str = None, message_history: list = None, show_last: int = 10):
    """Show 'show_last' messages of message history

    Args:
        message_history (list, optional): list of messages with content. Defaults to None.
        show_last (int, optional): sets how many messages to display. Defaults to 10.
    """
    if message_history is None or len(message_history) == 0:
        print("\033[1m\033[93m[WARN] _print_message_history >>>>\033[0m История сообщений пуста")

    for message_item in message_history[-show_last:]:
        if message_item.get("role") == "user":
            print(f"\033[1m\033[34m{username if username is not None else "USER"}:\033[0m")

        if message_item.get("role") == "assistant":
            print("\033[1m\033[92mMODEL:\033[0m")

        if "content" in message_item:
            _print_markdown_message(message_item.get("content"))


def print_message(message: str = None):
    if message is not None:
        print("\n\033[1m\033[96m============================================================\033[0m\n")
        _print_markdown_message(message)
        print("\n\033[1m\033[96m============================================================\033[0m\n")


def show_message_history(chat: Chat = None):
    if chat is None:
        print("chat is none")
        return

    # Создание дубликата истории сообщений, т.к. возможна мутация
    messages_to_display = chat.message_history
    message_history_ids = chat.message_history_ids

    # Если в памяти мало сообщений для отображения
    if chat.message_count < DISPLAY_MESSAGE_HISTORY_COUNT:
        path_to_message_history_file = Path(f"data/history/{chat.username}.json")

        is_history_file_exists = path_to_message_history_file.exists()


        if is_history_file_exists:
            # Догрузить сообщения из файла с сохранениями
            with path_to_message_history_file.open("r", encoding="utf-8") as file:
                message_history_object = json.load(file)

                if "message_history_ids" not in message_history_object:
                    print("\033[1m\033[91m[ERROR] show_message_history >>>>\033[0m В файле с сохраненной историей сообщений некорректная структура. Отсутствует поле 'message_history_ids'")
                    return

                if "message_history" not in message_history_object:
                    print("\033[1m\033[91m[ERROR] show_message_history >>>>\033[0m В файле с сохраненной историей сообщений некорректная структура. Отсутствует поле 'message_history'")
                    return

                file_message_histody_len = len(message_history_object["message_history"])
                # Обход списка истории сообщений в обратном порядке
                for shift, message_id in enumerate(reversed(message_history_object["message_history_ids"])):
                    # Если message_id сообщения уже есть в памяти, загрузка такого сообщения не требуется
                    if message_id in message_history_ids:
                        continue

                    # Вставка сообщений в начало истории сообщений в памяти (сообщения в файле старее, чем сообщения в памяти)
                    messages_to_display.insert(0, message_history_object["message_history"][file_message_histody_len - 1 - shift])

                    # При доборе сообщений до нужного количества, завершить обход
                    if len(messages_to_display) >= DISPLAY_MESSAGE_HISTORY_COUNT:
                        break
        elif chat.message_count == 0:
            # История пуста, файл с историей отсутствует
            print("\033[1m\033[93m[WARN] show_message_history >>>>\033[0m История сообщений пуста")
            return

    _print_message_history(chat.username, messages_to_display, DISPLAY_MESSAGE_HISTORY_COUNT)