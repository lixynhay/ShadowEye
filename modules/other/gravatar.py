"""Gravatar модуль."""
from ..base import BaseModule
import httpx
import hashlib

class GravatarModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Gravatar"
        self.domain = "gravatar.com"
        self.method = "register"
        self.category = "other"
        self.url = "https://gravatar.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            email_hash = hashlib.md5(email.lower().encode()).hexdigest()
            response = await client.get(f"https://www.gravatar.com/{email_hash}.json")
            exists = response.status_code == 200
            details = ""
            if exists:
                try:
                    data = response.json()
                    if "entry" in data and data["entry"]:
                        details = data["entry"][0].get("displayName", "")
                except Exception:
                    pass
            return self._create_result(exists=exists, details=details)
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
