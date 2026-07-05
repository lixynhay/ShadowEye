"""Кэш результатов для повторных проверок."""
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class CacheManager:
    def __init__(self, cache_file: str = "~/.osint_toolkit_cache.json"):
        self.cache_file = os.path.expanduser(cache_file)
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        """Загрузить кэш из файла."""
        default_cache = {"email": {}, "username": {}, "image": {}}
        if not os.path.exists(self.cache_file):
            return default_cache

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
        except Exception:
            return default_cache

        if not isinstance(loaded, dict):
            return default_cache

        normalized = {key: loaded.get(key, {}) for key in default_cache}
        for key, value in normalized.items():
            if not isinstance(value, dict):
                normalized[key] = {}
        return normalized

    def _save_cache(self):
        """Сохранить кэш в файл."""
        try:
            self.cache.setdefault("email", {})
            self.cache.setdefault("username", {})
            self.cache.setdefault("image", {})
            cache_dir = os.path.dirname(self.cache_file)
            if cache_dir:
                os.makedirs(cache_dir, exist_ok=True)
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2, default=str)
        except Exception:
            pass

    def _get_key(self, value: str) -> str:
        """Создать хэш ключ."""
        return hashlib.md5(value.encode()).hexdigest()

    def _get_cached_results(self, bucket: str, value: str, max_age_hours: int) -> Optional[list]:
        """Получить результаты из кэша, если запись валидна и не устарела."""
        key = self._get_key(value)
        bucket_cache = self.cache.get(bucket, {})
        if key not in bucket_cache:
            return None

        entry = bucket_cache[key]
        if not isinstance(entry, dict):
            return None

        timestamp = entry.get("timestamp")
        if not isinstance(timestamp, str):
            return None

        try:
            cached_time = datetime.fromisoformat(timestamp)
        except ValueError:
            return None

        if datetime.now() - cached_time < timedelta(hours=max_age_hours):
            return entry.get("results")
        return None

    def get_email(self, email: str, max_age_hours: int = 24) -> Optional[list]:
        """Получить кэшированный результат для email."""
        return self._get_cached_results("email", email, max_age_hours)

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
        return self._get_cached_results("username", username, max_age_hours)

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
