"""Spotify модуль - рабочий."""
from ..base import BaseModule
import httpx

class SpotifyModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Spotify"
        self.domain = "spotify.com"
        self.method = "register"
        self.category = "music"
        self.url = "https://spotify.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            
            data = {"email": email}
            response = await client.post(
                "https://spclient.wg.spotify.com/signup/public/v1/account",
                headers=headers,
                data=data
            )
            
            try:
                resp_data = response.json()
                # status 20 = email уже зарегистрирован
                exists = resp_data.get("status") == 20
                return self._create_result(exists=exists)
            except:
                return self._create_result(exists=False, error=True, details="Invalid JSON")
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
