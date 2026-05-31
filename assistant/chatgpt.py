import time
import json
from config import REQUEST_TIMEOUT

class ChatGPT:
    """Работа с веб-интерфейсом ChatGPT (Исправлено для нового UI)"""
    
    def __init__(self, page):
        self.page = page
        print("✓ ChatGPT инициализирован")
    
    def _find_textarea(self):
        """Ищет поле ввода"""
        selectors = [
            "#prompt-textarea",
            "textarea[rows]",
            "div[contenteditable='true']",
            "textarea"
        ]
        for sel in selectors:
            exists = self.page.evaluate(f"!!document.querySelector('{sel}')")
            if exists:
                return sel
        return None
    
    def ask(self, prompt):
        """Отправляет промпт и получает ПОЛНЫЙ ответ"""
        print(f"→ Отправка в ChatGPT: {prompt[:50]}...")
        
        textarea = self._find_textarea()
        if not textarea:
            return "✗ Не найдено поле ввода в ChatGPT"
        
        # Запоминаем количество полных ответов (turns) ДО отправки
        before_turns = self.page.evaluate("""
            (function() {
                return document.querySelectorAll('[data-turn-id-container]').length;
            })();
        """) or 0
        
        # Вставляем промпт
        self.page.type_text(textarea, prompt)
        time.sleep(0.5)
        
        # Эмулируем Enter
        self.page.evaluate(f"""
            (function() {{
                const el = document.querySelector('{textarea}');
                if (el) {{
                    el.dispatchEvent(new KeyboardEvent('keydown', {{
                        key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true
                    }}));
                }}
            }})();
        """)
        
        start = time.time()
        last_text = ""
        stable_count = 0
        
        while time.time() - start < REQUEST_TIMEOUT:
            # Комплексная проверка статуса генерации
            result = self.page.evaluate("""
                (function() {
                    // 1. Проверяем кнопку Stop (если есть - генерация еще идет)
                    const stopBtn = document.querySelector('button[aria-label*="Stop" i], button[aria-label*="Остановить" i], button[data-testid="stop-button"]');
                    if (stopBtn) return JSON.stringify({ generating: true, text: '' });
                    
                    // 2. Ищем последний turn (полный блок ответа)
                    const turns = document.querySelectorAll('[data-turn-id-container]');
                    if (turns.length === 0) return JSON.stringify({ generating: true, text: '' });
                    
                    const lastTurn = turns[turns.length - 1];
                    
                    // 3. Проверяем наличие action-кнопок внутри этого turn
                    // Эти кнопки появляются ТОЛЬКО после завершения генерации
                    const copyBtn = lastTurn.querySelector('[data-testid="copy-turn-action-button"]');
                    const goodBtn = lastTurn.querySelector('[data-testid="good-response-turn-action-button"]');
                    const badBtn = lastTurn.querySelector('[data-testid="bad-response-turn-action-button"]');
                    
                    // 4. Извлекаем текст из markdown контейнера
                    const mdContainer = lastTurn.querySelector('.markdown, [class*="markdown"]');
                    const text = mdContainer ? mdContainer.innerText.trim() : '';
                    
                    // Генерация завершена, если есть хотя бы одна action-кнопка
                    const hasActions = !!(copyBtn || goodBtn || badBtn);
                    
                    return JSON.stringify({ 
                        generating: false, 
                        text: text,
                        hasActions: hasActions
                    });
                })();
            """)
            
            try:
                data = json.loads(result)
            except:
                data = {"generating": True, "text": "", "hasActions": False}
            
            current_text = data.get("text", "")
            
            # Если генерация завершена и текст стабилен
            if not data["generating"] and data["hasActions"] and current_text:
                if current_text == last_text:
                    stable_count += 1
                    # Текст стабилен 1.5 секунды (5 циклов по 0.3с) после появления кнопок
                    if stable_count >= 5:
                        print(f"← Получено символов: {len(current_text)}")
                        return current_text
                else:
                    stable_count = 0
                    last_text = current_text
            else:
                stable_count = 0
            
            time.sleep(0.3)
        
        # Если вышли по таймауту, возвращаем то, что есть
        if last_text:
            return last_text + "\n\n[⚠️ Ответ прерван по таймауту]"
        return "✗ Таймаут ожидания ответа от ChatGPT"
    
    def new_chat(self):
        """Создает новый чат"""
        return self.page.evaluate("""
            (function() {
                const btns = document.querySelectorAll('a, button');
                for (const b of btns) {
                    if (b.innerText.includes('New chat') || b.innerText.includes('Новый чат') || b.getAttribute('aria-label')?.includes('New chat')) {
                        b.click();
                        return true;
                    }
                }
                return false;
            })();
        """)
    
    def stop_generating(self):
        """Останавливает генерацию"""
        return self.page.evaluate("""
            (function() {
                const btns = document.querySelectorAll('button');
                for (const b of btns) {
                    if (b.innerText.includes('Stop') || b.innerText.includes('Остановить') || b.getAttribute('aria-label')?.includes('Stop')) {
                        b.click();
                        return true;
                    }
                }
                return false;
            })();
        """)