import random
from typing import List, Optional

class ProxyRotator:
    def __init__(self, proxy_file: str = "~/.osint_proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies = self._load_proxies()
        self.current_index = 0
    
    def _load_proxies(self) -> List[str]:
        """Загрузить прокси из файла."""
        import os
        proxy_path = os.path.expanduser(self.proxy_file)
        
        if not os.path.exists(proxy_path):
            return []
        
        try:
            with open(proxy_path, 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                return proxies
        except Exception:
            return []
    
    def get_proxy(self) -> Optional[str]:
        """Получить следующий прокси."""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_proxy(self) -> Optional[str]:
        """Получить случайный прокси."""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def add_proxy(self, proxy: str):
        """Добавить прокси."""
        self.proxies.append(proxy)
    
    def has_proxies(self) -> bool:
        """Есть ли прокси."""
        return len(self.proxies) > 0
