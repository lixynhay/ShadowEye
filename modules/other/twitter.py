"""Twitter модуль - рабочий."""
from ..base import BaseModule
import httpx

class TwitterModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Twitter"
        self.domain = "twitter.com"
        self.method = "register"
        self.category = "social"
        self.url = "https://twitter.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            }
            
            # Получаем guest token
            r1 = await client.post("https://api.twitter.com/1.1/guest/activate.json", headers=headers)
            guest_token = r1.json().get("guest_token")
            
            headers["X-Guest-Token"] = guest_token
            
            data = {"email": email}
            response = await client.post(
                "https://api.twitter.com/i/users/email_available.json",
                headers=headers,
                data=data
            )
            
            try:
                resp_data = response.json()
                # valid=false значит email уже занят
                exists = not resp_data.get("valid", True)
                return self._create_result(exists=exists)
            except:
                return self._create_result(exists=False, error=True, details="Invalid JSON")
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
