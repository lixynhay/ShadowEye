"""Базовый класс для модулей."""
from typing import Dict, Any
import httpx

class BaseModule:
    def __init__(self):
        self.name = "base"
        self.domain = ""
        self.method = "register"
        self.category = "other"
        self.url = ""
    
    async def check(self, email: str, client: httpx.AsyncClient) -> Dict[str, Any]:
        raise NotImplementedError
    
    def _create_result(self, exists: bool, details: str = "", error: bool = False) -> Dict[str, Any]:
        return {"exists": exists, "details": details, "error": error, "service": self.name, "category": self.category, "url": self.url}
