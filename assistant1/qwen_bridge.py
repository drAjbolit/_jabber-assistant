import requests
import json
from typing import Optional

class QwenBridge:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        # Для Qwen можно использовать OpenAI-совместимый endpoint
        # или прямой API от Alibaba Cloud
        self.api_key = api_key
        self.base_url = base_url
        self.conversations = {}  # Хранилище контекста по JID
        
    def send_message(self, jid: str, message: str) -> str:
        """Отправляет сообщение и получает ответ"""
        # Инициализируем историю для нового контакта
        if jid not in self.conversations:
            self.conversations[jid] = []
            
        # Добавляем сообщение пользователя
        self.conversations[jid].append({
            "role": "user",
            "content": message
        })
        
        # Формируем запрос
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "qwen-plus",  # или qwen-max для сложных задач
            "messages": self.conversations[jid],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            # Получаем ответ
            assistant_message = response.json()["choices"][0]["message"]["content"]
            
            # Сохраняем в историю
            self.conversations[jid].append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Ошибка API: {str(e)}"
            
    def clear_conversation(self, jid: str):
        """Очищает историю для конкретного контакта"""
        if jid in self.conversations:
            self.conversations[jid] = []