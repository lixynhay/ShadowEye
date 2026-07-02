"""GitHub модуль."""
from ..base import BaseModule
import httpx

class GitHubModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "GitHub"
        self.domain = "github.com"
        self.method = "register"
        self.category = "other"
        self.url = "https://github.com/join"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            }
            response = await client.post(
                "https://github.com/signup_check/email",
                headers=headers,
                data={"value": email}
            )
            exists = response.status_code == 422
            return self._create_result(exists=exists)
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
