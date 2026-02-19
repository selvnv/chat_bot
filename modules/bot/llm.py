from modules.bot.config import MESSAGE_HISTORY_LIMIT, Chat, Role
from modules.bot.message_history import save_message_history
from modules.bot.context import generate_context

def chat_make_request(chat: Chat = None, request_message: str = None):

    if chat is None:
        print("\033[1m\033[91m[ERROR] chat_make_request >>>>\033[0m chat is None")
        return False

    if request_message is None:
        print("\033[1m\033[91m[ERROR] chat_make_request >>>>\033[0m request_message is None")
        return False

    # Действия при превышении объема истории сообщений заданного лимита
    if chat.message_count >= MESSAGE_HISTORY_LIMIT:
        # Сохранить сообщения по достижении лимита
        save_message_history(chat)
        # Сгенерировать контекст - он будет подставляться вместо истории сообщений при отправке к сервису LLM
        generate_context(chat)

        # Очистить предыдущую историю в памяти программы
        chat.clear_messages()

    chat.add_message(Role.USER, request_message)

    assistant_message = chat.make_request(chat.message_history)

    if assistant_message is None or assistant_message.get("content") is None:
        print("\033[1m\033[91m[ERROR] chat_make_request >>>>\033[0m Ответ LLM не получен")
        return False

    chat.add_message(Role.ASSISTANT, assistant_message.get("content"))
    return True
