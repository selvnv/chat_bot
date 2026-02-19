from modules.bot.config import Chat


# Функция для генерации контекста на основе предыдущих сообщений
def generate_context(chat: Chat = None):
    if chat is None:
        raise TypeError("chat is None")

    if chat.context.context_prompt is None:
        print("\033[1m\033[91m[ERROR] generate_context >>>>\033[0m Промпт для генерации контекста не задан")
        return False

    print("\033[1m\033[94m[INFO] generate_context >>>>\033[0m Генерация контекста беседы")

    messages = chat.message_history
    messages.append({
        "role": "user",
        "content": chat.context.context_prompt
    })

    response_message = chat.make_request(messages)

    if response_message is not None and response_message.get("content") is not None:
        chat.context.context = response_message.get("content")
    else:
        return False

    return True
