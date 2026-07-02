"""Yandex модуль - рабочий."""
from ..base import BaseModule
import httpx

class YandexModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Yandex"
        self.domain = "yandex.ru"
        self.method = "register"
        self.category = "email"
        self.url = "https://passport.yandex.ru"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://passport.yandex.ru",
                "Referer": "https://passport.yandex.ru/auth",
            }
            
            # Получаем cookies
            await client.get("https://passport.yandex.ru/auth", headers=headers)
            
            data = {"login": email}
            response = await client.post(
                "https://passport.yandex.ru/rest/access/check.json",
                headers=headers,
                data=data
            )
            
            try:
                resp_data = response.json()
                # status=ok значит аккаунт существует
                exists = resp_data.get("status") == "ok"
                return self._create_result(exists=exists)
            except:
                return self._create_result(exists=False, error=True, details="Invalid JSON")
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
