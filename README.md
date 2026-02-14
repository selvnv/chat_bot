# simple_chat_bot

### Установка сертификата Минцифры [для корректной работы запросов к API GigaChat](https://developers.sber.ru/docs/ru/gigachat/certificates)
```bash
curl -k "https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt" -w "\n" >> "$(python -m certifi)"
```

### Установка переменных окружения

Некоторые данные, необходимые для работы программы, она получает из переменных окружения
Эти переменные можно задать в файле `.env`, который должен находиться в корне проекта
После чего выполнить скрипт `init.sh`, который возьмет данные из `.env` и установит переменные окружения

```bash
# Содержимое файла .env
GIGACHAT_AUTHORIZE_KEY=<YOUR_AUTHORIZATION_KEY>
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_AUTH_URL=https://ngw.devices.sberbank.ru:9443/api/v2/oauth
```

Запуск скрипта для установки переменных окружения
```bash
source ./init.sh
```

