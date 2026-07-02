"""Facebook модуль - рабочий."""
from ..base import BaseModule
import httpx

class FacebookModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Facebook"
        self.domain = "facebook.com"
        self.method = "register"
        self.category = "social"
        self.url = "https://facebook.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/html,application/xhtml+xml",
            }
            
            # Получаем cookies
            await client.get("https://www.facebook.com/", headers=headers)
            
            data = {
                "email": email,
                "skip_api_login": "1",
                "signed_next": "1"
            }
            
            response = await client.post(
                "https://www.facebook.com/login/identify/?ctx=recover",
                headers=headers,
                data=data,
                follow_redirects=True
            )
            
            text = response.text.lower()
            
            # Если нашли аккаунт - есть форма подтверждения
            exists = "find your account" in text or "найти аккаунт" in text or "continue" in text
            
            return self._create_result(exists=exists)
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
