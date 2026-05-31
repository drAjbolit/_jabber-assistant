import os
import base64
import mimetypes
import requests

class QwenAPI:
    def __init__(self):
        # Ключ и URL берем из переменных окружения (.env)
        self.api_key = os.getenv("QWEN_API_KEY", "")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def _encode_image(self, image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def ask(self, text):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen/qwen-2.5-72b-instruct",
            "messages": [
                {"role": "system", "content": "Ты персональный ассистент. Отвечай кратко и по делу."},
                {"role": "user", "content": text}
            ]
        }
        try:
            r = requests.post(self.api_url, json=payload, headers=headers, timeout=60)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Ошибка Qwen API: {e}"

    def ask_image(self, image_path, prompt="Что изображено на картинке?"):
        base64_image = self._encode_image(image_path)
        mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen/qwen-vl-max", # Vision модель
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}}
                    ]
                }
            ]
        }
        try:
            r = requests.post(self.api_url, json=payload, headers=headers, timeout=60)
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Ошибка Qwen Vision API: {e}"