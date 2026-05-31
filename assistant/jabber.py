import json
import time
from config import ALLOWED_JIDS

class Jabber:
    def __init__(self, page):
        self.page = page
        self._install_hooks()
    
    def _install_hooks(self):
        """Универсальные хуки для Converse.js (API + DOM Fallback)"""
        hook_js = """
        (function() {
            if (window.__jabberHookInstalled) return 'already installed';
            window.__jabberHookInstalled = true;
            window.__pendingMessages = window.__pendingMessages || [];
            window.__processedMsgIds = new Set();

            function processMessage(from, text, id) {
                if (!text || !text.trim()) return;
                if (window.__processedMsgIds.has(id)) return;
                window.__processedMsgIds.add(id);
                
                // Ограничиваем размер Set, чтобы не течла память
                if (window.__processedMsgIds.size > 500) {
                    const arr = Array.from(window.__processedMsgIds);
                    window.__processedMsgIds = new Set(arr.slice(-200));
                }
                
                window.__pendingMessages.push({
                    from: from || 'unknown',
                    text: text.trim(),
                    ts: Date.now()
                });
                console.log('[CDP-HOOK] Перехвачено:', text.substring(0, 50));
            }

            // Метод 1: Перехват через внутренний API Converse.js
            function hookConverseAPI() {
                if (window.converse && window.converse.api && window.converse.api.listen) {
                    window.converse.api.listen.on('message', function(data) {
                        try {
                            let stanza = data.stanza || data;
                            let from = '', text = '', id = '';
                            if (stanza.getAttribute) {
                                from = stanza.getAttribute('from');
                                let body = stanza.querySelector('body');
                                text = body ? body.textContent : '';
                                id = stanza.getAttribute('id') || from + text;
                            } else if (stanza.get) {
                                from = stanza.get('from');
                                text = stanza.get('message');
                                id = stanza.get('msgid') || from + text;
                            }
                            processMessage(from, text, id);
                        } catch(e) { console.error('[CDP-HOOK] API error', e); }
                    });
                    console.log('[CDP-HOOK] Converse API успешно подключен');
                    return true;
                }
                return false;
            }

            // Метод 2: Перехват через DOM (Надежный фолбэк)
            function hookDOM() {
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(m) {
                        m.addedNodes.forEach(function(node) {
                            if (node.nodeType === 1) {
                                let msgs = [];
                                if (node.matches && node.matches('.chat-msg')) msgs.push(node);
                                if (node.querySelectorAll) {
                                    node.querySelectorAll('.chat-msg').forEach(n => msgs.push(n));
                                }
                                
                                msgs.forEach(function(msgEl) {
                                    // Игнорируем исходящие сообщения
                                    if (msgEl.classList.contains('chat-msg--outgoing')) return;
                                    
                                    let body = msgEl.querySelector('.chat-msg__text, .chat-msg__body');
                                    if (body) {
                                        let text = body.innerText || body.textContent;
                                        let from = msgEl.getAttribute('data-from') || 
                                                   msgEl.querySelector('.chat-msg__author')?.textContent || 'converse_user';
                                        let id = msgEl.getAttribute('data-msgid') || msgEl.getAttribute('data-isodate') || text;
                                        processMessage(from, text, id);
                                    }
                                });
                            }
                        });
                    });
                });

                const target = document.querySelector('#conversejs') || document.body;
                observer.observe(target, { childList: true, subtree: true });
                console.log('[CDP-HOOK] DOM Observer запущен');
            }

            // Пытаемся подключиться к API, если Converse еще грузится - ждем события
            if (!hookConverseAPI()) {
                window.addEventListener('converse-loaded', hookConverseAPI);
            }
            
            // DOM-наблюдатель запускаем всегда
            hookDOM();

            return 'hooks scheduled';
        })();
        """
        result = self.page.evaluate(hook_js)
        print(f"✓ Jabber hooks: {result}")
        time.sleep(2)

    def get_pending_messages(self):
        js = """
        (function() {
            const msgs = window.__pendingMessages || [];
            window.__pendingMessages = [];
            return JSON.stringify(msgs);
        })();
        """
        result = self.page.evaluate(js)
        if not result:
            return []
        try:
            msgs = json.loads(result)
            if ALLOWED_JIDS:
                return [m for m in msgs if any(allowed in m.get("from", "") for allowed in ALLOWED_JIDS)]
            return msgs
        except Exception as e:
            print(f"Error parsing messages: {e}")
            return []

    def send_message(self, text, recipient=None):
        """Отправка сообщения через API Converse.js или DOM"""
        js_send = """
        (async function() {
            const text = """ + json.dumps(text) + """;
            let targetJid = """ + json.dumps(recipient) + """;
            
            // Попытка 1: Через API Converse
            if (window.converse && window.converse.api) {
                try {
                    if (!targetJid) {
                        const chats = await window.converse.api.chats.get();
                        if (chats && chats.length > 0) targetJid = chats[0].get('jid');
                    }
                    if (targetJid) {
                        const chat = await window.converse.api.chats.open(targetJid);
                        if (chat && chat.sendMessage) {
                            chat.sendMessage(text);
                            return 'sent_via_api';
                        }
                    }
                } catch(e) { console.log('[CDP-SEND] API error:', e); }
            }
            
            // Попытка 2: Через DOM (Textarea)
            const textarea = document.querySelector('textarea.chat-textarea');
            if (textarea) {
                textarea.focus();
                textarea.value = text;
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
                textarea.dispatchEvent(new Event('change', { bubbles: true }));
                
                const btn = document.querySelector('button.send-button, .chat-send');
                if (btn) { btn.click(); return 'sent_via_button'; }
                
                textarea.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', keyCode: 13, bubbles: true}));
                return 'sent_via_enter';
            }
            return 'no_method_available';
        })();
        """
        try:
            result = self.page.send("Runtime.evaluate", {
                "expression": js_send,
                "returnByValue": True,
                "awaitPromise": True,
                "timeout": 15000
            })
            val = result.get("result", {}).get("result", {}).get("value", "no_result")
            print(f"  Результат отправки: {val}")
            return 'sent' in str(val)
        except Exception as e:
            print(f"  Send error: {e}")
            return False

    def send_typing_state(self, state="composing"):
        # Converse.js сам управляет статусами "печатает", здесь это не критично
        pass