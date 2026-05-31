import time
import os
import requests
import tempfile

from assistant.cdp import ChromeCDP
from assistant.jabber import Jabber
from assistant.chatgpt import ChatGPT
from assistant.qwen_api import QwenAPI  # <--- Импорт нового модуля
from assistant.ftp_upload import upload_file
from assistant.ws_server import WSServer

def is_image_url(text):
    text = text.lower()
    return text.startswith("http") and any(ext in text for ext in [".png", ".jpg", ".jpeg", ".webp"])

def main():
    ws = WSServer()
    ws.start()

    cdp = ChromeCDP()
    cdp.connect()

    jabber_page = cdp.find_page("chat.jabber.ru")
    if not jabber_page:
        print("Jabber page not found")
        return
        
    # --- Логика переключения ---
    USE_QWEN = os.getenv("USE_QWEN", "false").lower() == "true"
    
    chatgpt = None
    qwen = None

    if USE_QWEN:
        print("🚀 Режим Qwen API активирован")
        qwen = QwenAPI()
    else:
        print("🌐 Режим ChatGPT Web UI")
        chatgpt_page = cdp.find_page("chatgpt.com")
        if not chatgpt_page:
            print("ChatGPT page not found")
            return
        chatgpt = ChatGPT(chatgpt_page)

    jabber = Jabber(jabber_page)
    print("WS MODE STARTED")

    while True:
        try:
            events = ws.get_events()
            for event in events:
                if event.get("type") != "jabber_message":
                    continue

                body = event.get("text", "").strip()
                if not body:
                    continue
                print("[RECV]", body)

                try:
                    if is_image_url(body):
                        jabber.send_message("📷 Фото получено. Анализирую...")
                        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                        try:
                            r = requests.get(body, timeout=30)
                            r.raise_for_status()
                            with open(tmp.name, "wb") as f:
                                f.write(r.content)
                            
                            # Выбор обработчика картинок
                            answer = qwen.ask_image(tmp.name) if USE_QWEN else chatgpt.ask_image(tmp.name)
                            
                        finally:
                            try: os.unlink(tmp.name)
                            except: pass
                    else:
                        if USE_QWEN:
                            answer = qwen.ask(body)
                            jabber.send_message(answer)
                            print("[QWEN]", answer[:200])
                        else:
                            before_images = chatgpt.get_image_ids()
                            answer = chatgpt.ask(body)
                            after_images = chatgpt.get_image_ids()
                            
                            if after_images - before_images:
                                image_path = "generated.png"
                                if chatgpt.save_last_generated_image(image_path):
                                    url = upload_file(image_path)
                                    jabber.send_message(url)
                                try: os.unlink(image_path)
                                except: pass
                            
                            jabber.send_message(answer)
                            print("[GPT]", answer[:200])

                except Exception as e:
                    print("AI ERROR:", e)

            time.sleep(0.05)
        except Exception as e:
            print("MAIN LOOP ERROR:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()