"""Pinterest модуль - рабочий."""
from ..base import BaseModule
import httpx

class PinterestModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Pinterest"
        self.domain = "pinterest.com"
        self.method = "register"
        self.category = "social"
        self.url = "https://pinterest.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
            }
            
            data = {"email": email}
            response = await client.post(
                "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
                headers=headers,
                data=data
            )
            
            try:
                resp_data = response.json()
                exists = resp_data.get("resource_response", {}).get("data", {}).get("exists", False)
                return self._create_result(exists=exists)
            except:
                return self._create_result(exists=False, error=True, details="Invalid JSON")
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
