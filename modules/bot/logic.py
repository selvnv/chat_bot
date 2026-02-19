from modules.bot.config import Chat
from modules.bot.config_manager import load_user_config, save_user_config
from modules.bot.llm import chat_make_request
from modules.bot.message_history import save_message_history
from modules.bot.display import print_message, show_message_history

chat_patterns = ["chat", "start", "begin", "старт", "начать"]
exit_patterns = ["quit", "q", "exit", "выход"]
submit_phrases = ["y", "yes", "true", "ok", "да"]

chat = Chat()

def init_chat():
    load_user_config(chat)
    chat.context.set_context_prompt_from_file()


def save_chat_state():
    # Сохранение конфигурации перед выходом (имя пользователя, контекст)
    save_user_config(chat)

    # Сохранение истории сообщений
    save_message_history(chat)


def start_chat():

    init_chat()

    # Ввод имени пользователя, если конфиг пустой
    if chat.username is None:
        input_username = ""

        while True:
            input_username = str(input("Введите ваше имя пользователя \033[1m\033[34m> \033[0m ")).strip()

            if input_username == "":
                continue

            submit_username = str(input(f"Начать чат с именем {input_username} (y, n) \033[1m\033[34m> \033[0m ")).strip()

            if submit_username.lower() in submit_phrases:
                break

        chat.username = input_username


    while True:
        command = str(input("Введите команду (chat, q, hist) \033[1m\033[34m> \033[0m ")).strip()

        if command.lower() in exit_patterns:
            save_chat_state()
            print("Хорошего дня)")
            break

        if command.lower() == "hist":
            show_message_history(chat)

        if command.lower() in chat_patterns:
            while True:
                message = str(input("Введите запрос или команду выхода \033[1m\033[34m> \033[0m ")).strip()

                if message == "":
                    continue

                if message in exit_patterns:
                    break

                # Выполнить запрос пользователя к LLM
                is_request_ok =  chat_make_request(chat, message)
                if not is_request_ok:
                    print("[ERROR] Произошла ошибка при выполнении запроса")
                    continue

                # Последнее сообщение в истории чата (ответ LLM) выводится в консоль
                llm_answer = chat.last_message()
                if llm_answer is not None:
                    print_message(llm_answer.get("content"))
