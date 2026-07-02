"""VK модуль - рабочий."""
from ..base import BaseModule
import httpx

class VKModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "VK"
        self.domain = "vk.com"
        self.method = "register"
        self.category = "social"
        self.url = "https://vk.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/html,application/xhtml+xml",
            }
            
            data = {"email": email}
            response = await client.post(
                "https://vk.com/login_check.php",
                headers=headers,
                data=data
            )
            
            text = response.text.lower()
            
            # Если email не найден - будет сообщение
            exists = "email is not" not in text and "не найден" not in text
            
            return self._create_result(exists=exists)
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
