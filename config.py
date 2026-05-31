# Конфигурация проекта

# Порт Chrome для отладки (запускать: chrome --remote-debugging-port=9222)
CDP_HOST = "127.0.0.1"
CDP_PORT = 9222

# URL вкладок для поиска
JABBER_URL_PATTERN = "chat.jabber.ru"       # Или ваш веб-клиент
CHATGPT_URL_PATTERN = "chatgpt.com"

# Whitelist JID-ов (кто может общаться с ботом)
ALLOWED_JIDS = [
    "gusarov.m@yax.im",
    "boss@company.com"
]

# Настройки генерации
MAX_RESPONSE_LENGTH = 1500  # Максимальная длина сообщения в XMPP
TYPING_DELAY = 0.03         # Задержка между символами при эмуляции ввода (сек)
REQUEST_TIMEOUT = 60        # Таймаут ожидания ответа от ChatGPT

# Команды управления
COMMANDS = {
    "/new": "Создать новый чат в ChatGPT",
    "/status": "Статус системы",
    "/stop": "Остановить генерацию",
    "/help": "Список команд"
}