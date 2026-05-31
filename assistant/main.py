import time
import sys
from assistant.cdp import ChromeCDP
from assistant.jabber import Jabber
from assistant.chatgpt import ChatGPT
from config import COMMANDS, MAX_RESPONSE_LENGTH

def chunk_text(text, max_len=MAX_RESPONSE_LENGTH):
    """Разбивает длинный текст на части по границам предложений/абзацев"""
    if not text:
        return [""]
    if len(text) <= max_len:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_len:
            chunks.append(text)
            break
        
        # Приоритет 1: перенос строки
        split = text.rfind('\n', 0, max_len)
        # Приоритет 2: точка с пробелом
        if split == -1:
            split = text.rfind('. ', 0, max_len)
        # Приоритет 3: просто точка
        if split == -1:
            split = text.rfind('.', 0, max_len)
        # Крайний случай: режем как есть
        if split == -1:
            split = max_len
        
        chunks.append(text[:split + 1].strip())
        text = text[split + 1:].strip()
    
    return chunks


def handle_command(cmd, chatgpt, jabber, sender_jid):
    """Обработка служебных команд"""
    if cmd == "/new":
        chatgpt.new_chat()
        jabber.send_message("✅ Новый чат ChatGPT создан", recipient=sender_jid)
    elif cmd == "/stop":
        chatgpt.stop_generating()
        jabber.send_message("⏹ Генерация остановлена", recipient=sender_jid)
    elif cmd == "/help":
        help_text = "📋 Доступные команды:\n"
        for c, desc in COMMANDS.items():
            help_text += f"{c} — {desc}\n"
        jabber.send_message(help_text, recipient=sender_jid)
    elif cmd == "/status":
        jabber.send_message("🟢 Система активна. ChatGPT готов к работе.", recipient=sender_jid)
    else:
        return False
    return True


def main():
    print("=" * 50)
    print("  JABBER AI ASSISTANT (ChatGPT Web UI Mode)")
    print("=" * 50)
    
    # 1. Подключаемся к Chrome
    cdp = ChromeCDP()
    try:
        cdp.connect()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)
    
    # 2. Находим нужные вкладки
    jabber_page = cdp.find_page("jabber")
    chatgpt_page = cdp.find_page("chatgpt")
    
    if not jabber_page:
        print("✗ Вкладка Jabber не найдена. Откройте веб-клиент (например, chat.jabber.ru).")
        sys.exit(1)
    if not chatgpt_page:
        print("✗ Вкладка ChatGPT не найдена. Откройте chatgpt.com и авторизуйтесь.")
        sys.exit(1)
    
    # 3. Инициализируем модули
    jabber = Jabber(jabber_page)
    chatgpt = ChatGPT(chatgpt_page)
    
    # Даем Converse.js время проинициализировать хуки
    print("⏳ Ожидание инициализации Converse.js (5 сек)...")
    time.sleep(5)
    
    print("\n✓ Готов к работе. Слушаю входящие сообщения...")
    
    # 4. Главный цикл
    error_count = 0
    last_sender = None  # Запоминаем последнего собеседника для стартового сообщения
    
    while True:
        try:
            messages = jabber.get_pending_messages()
            
            for msg in messages:
                text = msg.get("text", "").strip()
                sender = msg.get("from", "unknown")
                
                if not text:
                    continue
                
                # Извлекаем bare JID (без ресурса) для ответа
                bare_jid = sender.split('/')[0]
                last_sender = bare_jid
                print(f"\n[{bare_jid}] {text[:80]}")
                
                # Обработка команд
                if text.startswith("/"):
                    if handle_command(text.lower(), chatgpt, jabber, bare_jid):
                        continue
                
                # Индикация "печатает"
                jabber.send_typing_state("composing")
                
                # Отправляем в ChatGPT
                try:
                    answer = chatgpt.ask(text)
                    
                    # Разбиваем длинные ответы
                    chunks = chunk_text(answer)
                    for i, chunk in enumerate(chunks):
                        # Передаем JID отправителя для ответа в правильный чат
                        jabber.send_message(chunk, recipient=bare_jid)
                        if i < len(chunks) - 1:
                            time.sleep(0.5)
                    
                    print(f"→ Отправлено частей: {len(chunks)}")
                    error_count = 0
                except Exception as e:
                    jabber.send_message(f"⚠️ Ошибка: {e}", recipient=bare_jid)
                    print(f"✗ Ошибка: {e}")
                finally:
                    jabber.send_typing_state("active")
            
            # Отправляем стартовое сообщение только ОДИН РАЗ после запуска
            # (и только если уже есть открытый чат)
            if not hasattr(main, '_started_sent'):
                if last_sender:
                    try:
                        jabber.send_message(
                            "🤖 Ассистент запущен. Отправьте /help для списка команд.",
                            recipient=last_sender
                        )
                    except:
                        pass
                main._started_sent = True
            
            # ⚡ Задержка 1.5 секунды - снижает нагрузку на CDP
            time.sleep(1.5)
            
        except KeyboardInterrupt:
            print("\n✓ Остановка...")
            if last_sender:
                try:
                    jabber.send_message("👋 Ассистент остановлен", recipient=last_sender)
                except:
                    pass
            break
        except Exception as e:
            error_count += 1
            print(f"Main loop error ({error_count}): {e}")
            if error_count > 10:
                print("⚠️ Много ошибок подряд. Проверьте подключение Chrome.")
                error_count = 0
            time.sleep(3)  # Пауза при ошибках


if __name__ == "__main__":
    main()