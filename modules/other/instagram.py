"""Instagram модуль - рабочий."""
from ..base import BaseModule
import httpx

class InstagramModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Instagram"
        self.domain = "instagram.com"
        self.method = "register"
        self.category = "social"
        self.url = "https://instagram.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "X-IG-App-ID": "936619743392459",
                "X-IG-WWW-Claim": "0",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/password/reset/",
            }
            
            # Получаем cookies
            await client.get("https://www.instagram.com/", headers=headers)
            
            data = {"email": email}
            response = await client.post(
                "https://www.instagram.com/accounts/account_recovery_send_ajax/",
                headers=headers,
                data=data
            )
            
            try:
                resp_data = response.json()
                # status=ok значит email найден
                exists = resp_data.get("status") == "ok"
                return self._create_result(exists=exists)
            except:
                return self._create_result(exists=False, error=True, details="Invalid JSON")
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
