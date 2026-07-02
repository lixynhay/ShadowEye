"""Outlook модуль - рабочий."""
from ..base import BaseModule
import httpx

class OutlookModule(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Outlook"
        self.domain = "microsoft.com"
        self.method = "register"
        self.category = "email"
        self.url = "https://login.live.com"
    
    async def check(self, email: str, client: httpx.AsyncClient) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            
            data = {
                "signInName": email,
                "isOtherIdpSupported": True,
                "checkPhones": False,
                "isRemoteNGCSupported": True,
                "isCookieBannerShown": False,
                "isFidoSupported": True,
                "originalRequest": "",
                "country": "US",
                "forceotclogin": False,
                "isExternalFederationDisallowed": False,
                "isRemoteConnectSupported": False,
                "federationFlags": 0,
                "isSignup": False,
                "flowToken": "",
                "isAccessPassSupported": True
            }
            
            response = await client.post(
                "https://login.live.com/GetCredentialType.srf",
                headers=headers,
                json=data
            )
            
            try:
                resp_data = response.json()
                # IfExistsResult: 0 = существует, 1 = не существует, 5 = существует но другой провайдер
                exists = resp_data.get("IfExistsResult") in [0, 5]
                return self._create_result(exists=exists)
            except:
                return self._create_result(exists=False, error=True, details="Invalid JSON")
        except Exception as e:
            return self._create_result(exists=False, error=True, details=str(e))
