"""Кэш результатов для повторных проверок."""
import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class CacheManager:
    def __init__(self, cache_file: str = "~/.osint_toolkit_cache.json"):
        self.cache_file = os.path.expanduser(cache_file)
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict[str, Any]:
        """Загрузить кэш из файла."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {"email": {}, "username": {}, "image": {}}
        return {"email": {}, "username": {}, "image": {}}
    
    def _save_cache(self):
        """Сохранить кэш в файл."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2, default=str)
        except Exception:
            pass
    
    def _get_key(self, value: str) -> str:
        """Создать хэш ключ."""
        return hashlib.md5(value.encode()).hexdigest()
    
    def get_email(self, email: str, max_age_hours: int = 24) -> Optional[list]:
        """Получить кэшированный результат для email."""
        key = self._get_key(email)
        if key in self.cache["email"]:
            entry = self.cache["email"][key]
            cached_time = datetime.fromisoformat(entry["timestamp"])
            if datetime.now() - cached_time < timedelta(hours=max_age_hours):
                return entry["results"]
        return None
    
    def set_email(self, email: str, results: list):
        """Сохранить результат для email."""
        key = self._get_key(email)
        self.cache["email"][key] = {
            "email": email,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        self._save_cache()
    
    def get_username(self, username: str, max_age_hours: int = 24) -> Optional[list]:
        """Получить кэшированный результат для username."""
        key = self._get_key(username)
        if key in self.cache["username"]:
            entry = self.cache["username"][key]
            cached_time = datetime.fromisoformat(entry["timestamp"])
            if datetime.now() - cached_time < timedelta(hours=max_age_hours):
                return entry["results"]
        return None
    
    def set_username(self, username: str, results: list):
        """Сохранить результат для username."""
        key = self._get_key(username)
        self.cache["username"][key] = {
            "username": username,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        self._save_cache()
    
    def clear(self):
        """Очистить кэш."""
        self.cache = {"email": {}, "username": {}, "image": {}}
        self._save_cache()
