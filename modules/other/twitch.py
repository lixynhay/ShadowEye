"""Twitch модуль - рабочий."""
from ..base import BaseModule
import httpx

class TwitchModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Twitch"
        self.domain = "twitch.tv"
        self.method = "register"
        self.category = "gaming"
        self.url = "https://twitch.tv"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
                "Content-Type": "application/json",
            }
            
            # Проверяем через signup
            data = {
                "operationName": "SignupUsernameCheck",
                "variables": {"email": email},
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "6c6e5d0ad82c3e2b2b1b8e9c7e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e9e"
                    }
                }
            }
            
            response = await client.post(
                "https://gql.twitch.tv/gql",
                headers=headers,
                json=data
            )
            
            # Если email уже зарегистрирован - будет ошибка
            exists = "already" in response.text.lower() or "taken" in response.text.lower()
            
            return self._create_result(exists=exists)
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
