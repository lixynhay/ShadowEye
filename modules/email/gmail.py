"""Gmail модуль - рабочий."""
from ..base import BaseModule
import httpx

class GmailModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Gmail"
        self.domain = "google.com"
        self.method = "register"
        self.category = "email"
        self.url = "https://accounts.google.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://accounts.google.com",
                "Referer": "https://accounts.google.com/signup/v2/createaccount",
            }
            
            # Получаем начальную страницу
            r1 = await client.get("https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp", headers=headers)
            
            # Ищем hidden поля
            import re
            match = re.search(r'name="GMailAddress" value="([^"]*)"', r1.text)
            
            data = {
                "GMailAddress": email,
                "Email": email,
                "identifier": email,
            }
            
            response = await client.post(
                "https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp",
                headers=headers,
                data=data
            )
            
            text = response.text.lower()
            
            # Если email уже занят - есть аккаунт
            if "this email" in text and ("already" in text or "taken" in text or "используется" in text):
                return self._create_result(exists=True, details="Email уже используется")
            
            # Если нет ошибки - email свободен
            if "next" in text or "продолжить" in text:
                return self._create_result(exists=False)
            
            return self._create_result(exists=False)
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
