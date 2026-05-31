import json
import time
import requests
import websocket
import threading
from config import CDP_HOST, CDP_PORT

class ChromeCDP:
    def __init__(self):
        self.targets = []
        self.pages = {}
        
    def connect(self):
        try:
            r = requests.get(f"http://{CDP_HOST}:{CDP_PORT}/json", timeout=5)
            self.targets = r.json()
            print(f"✓ Найдено вкладок: {len(self.targets)}")
            for t in self.targets:
                print(f"  - {t.get('title', 'N/A')[:60]}")
        except Exception as e:
            print(f"✗ Не удалось подключиться к Chrome: {e}")
            raise
    
    def find_page(self, url_pattern):
        for target in self.targets:
            url = target.get("url", "")
            if url_pattern in url:
                ws_url = target.get("webSocketDebuggerUrl")
                if ws_url and ws_url not in self.pages:
                    self.pages[ws_url] = CDPPage(ws_url)
                return self.pages.get(ws_url)
        return None


class CDPPage:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.ws = None
        self.msg_id = 0
        self.responses = {}
        self.events = []
        self._lock = threading.Lock()
        self._connected = False
        self._connect()
        self._reader_thread = threading.Thread(target=self._reader, daemon=True)
        self._reader_thread.start()
        print(f"✓ Подключено к вкладке: {ws_url[:50]}...")
    
    def _connect(self):
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.ws_url, timeout=30)
            self._connected = True
        except Exception as e:
            print(f"✗ WebSocket connect error: {e}")
            self._connected = False
    
    def _reconnect(self):
        print("⟳ Переподключение CDP...")
        try:
            if self.ws:
                self.ws.close()
        except:
            pass
        self._connect()
    
    def _reader(self):
        while True:
            if not self._connected:
                time.sleep(2)
                self._reconnect()
                continue
            try:
                self.ws.settimeout(5)
                msg = self.ws.recv()
                data = json.loads(msg)
                if "id" in data:
                    with self._lock:
                        self.responses[data["id"]] = data
                elif "method" in data:
                    self.events.append(data)
            except websocket.WebSocketTimeoutException:
                continue  # Нормально, просто нет сообщений
            except Exception as e:
                if "timed out" not in str(e).lower():
                    print(f"CDP Reader error: {e}")
                self._connected = False
                time.sleep(1)
    
    def send(self, method, params=None, timeout=30):
        if not self._connected:
            self._reconnect()
            if not self._connected:
                raise ConnectionError("CDP not connected")
        
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method}
        if params:
            msg["params"] = params
        
        try:
            self.ws.send(json.dumps(msg))
        except Exception as e:
            print(f"Send error: {e}")
            self._connected = False
            raise
        
        start = time.time()
        while time.time() - start < timeout:
            with self._lock:
                if self.msg_id in self.responses:
                    return self.responses.pop(self.msg_id)
            time.sleep(0.05)
        raise TimeoutError(f"Timeout on {method}")
    
    def evaluate(self, expression, return_value=True):
        try:
            result = self.send("Runtime.evaluate", {
                "expression": expression,
                "returnByValue": return_value,
                "awaitPromise": False,  # ВАЖНО: не ждать Promise, чтобы не зависать
                "timeout": 10000
            })
            return result.get("result", {}).get("result", {}).get("value")
        except Exception as e:
            print(f"  Evaluate error: {e}")
            return None
    
    def click(self, selector):
        js = f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (el) {{ el.click(); return true; }}
            return false;
        }})();
        """
        return self.evaluate(js)
    
    def type_text(self, selector, text):
        js = f"""
        (function() {{
            const el = document.querySelector('{selector}');
            if (!el) return false;
            el.focus();
            document.execCommand('insertText', false, {json.dumps(text)});
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            return true;
        }})();
        """
        return self.evaluate(js)
    
    def get_events(self):
        events = self.events.copy()
        self.events.clear()
        return events