"""Email OSINT через Holehe CLI с правильным парсингом."""
import asyncio
import re
from typing import List, Dict, Any
from ..ui import console, create_progress

# Мусорные строки которые не являются сервисами
SKIP_PATTERNS = [
    "Email used",
    "websites checked",
    "Twitter :",
    "Github :",
    "BTC Donations",
    "100%|",
    "████",
    "***********************",
]

class EmailChecker:
    def __init__(self, timeout: int = 20, proxy: str = None):
        self.timeout = timeout
        self.proxy = proxy
        self._holehe_available = False
        self._check_holehe()
    
    def _check_holehe(self):
        try:
            import holehe
            self._holehe_available = True
            console.print(f"[green]✓ Holehe установлен[/green]")
        except ImportError:
            console.print("[yellow]⚠ Holehe не установлен. pip install holehe[/yellow]")
            self._holehe_available = False
    
    def is_available(self) -> bool:
        return self._holehe_available
    
    def _is_valid_line(self, line: str) -> bool:
        """Проверяем что строка - это реальный сервис, а не мусор."""
        line = line.strip()
        if not line:
            return False
        
        # Должна начинаться с [+], [-] или [x]
        if not (line.startswith('[+]') or line.startswith('[-]') or line.startswith('[x]')):
            return False
        
        # Фильтруем мусорные строки
        for pattern in SKIP_PATTERNS:
            if pattern in line:
                return False
        
        return True
    
    async def check(self, email: str, show_all: bool = False) -> List[Dict[str, Any]]:
        if not self._holehe_available:
            return []
        
        results = []
        
        try:
            cmd = ["holehe", email]
            
            if self.proxy:
                cmd.extend(["--proxy", self.proxy])
            
            with create_progress() as progress:
                task = progress.add_task(f"[cyan]Holehe проверяет {email}...", total=100)
                
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await proc.communicate()
                progress.update(task, completed=100)
                
                stdout_text = stdout.decode('utf-8', errors='ignore') if stdout else ""
                
                for line in stdout_text.split('\n'):
                    if not self._is_valid_line(line):
                        continue
                    
                    line = line.strip()
                    
                    if line.startswith('[+]'):
                        site = line.replace('[+]', '').strip()
                        results.append({
                            "service": site,
                            "exists": True,
                            "details": "✓ Email найден",
                            "error": False,
                        })
                    elif line.startswith('[-]'):
                        site = line.replace('[-]', '').strip()
                        if show_all:
                            results.append({
                                "service": site,
                                "exists": False,
                                "details": "Не зарегистрирован",
                                "error": False,
                            })
                    elif line.startswith('[x]'):
                        site = line.replace('[x]', '').strip()
                        if show_all:
                            results.append({
                                "service": site,
                                "exists": False,
                                "details": "⚠ Rate limit",
                                "error": True,
                            })
                
                # Статистика (всегда показываем)
                found = sum(1 for r in results if r.get('exists'))
                not_found = sum(1 for r in results if not r.get('exists') and not r.get('error'))
                rate_limited = sum(1 for r in results if r.get('error'))
                
                console.print(f"[cyan]ℹ Всего проверено: {found + not_found + rate_limited}[/cyan]")
                console.print(f"[green]✓ Найдено: {found}[/green]")
                console.print(f"[red]✗ Не найдено: {not_found}[/red]")
                console.print(f"[yellow]⚠ Rate limit: {rate_limited}[/yellow]")
                console.print(f"[cyan]ℹ Совет: используй прокси чтобы уменьшить rate limit[/cyan]")
        
        except Exception as e:
            console.print(f"[bold red]✗ Ошибка запуска Holehe: {e}[/bold red]")
            import traceback
            traceback.print_exc()
        
        return results
    
    def run(self, email: str, show_all: bool = False) -> List[Dict[str, Any]]:
        return asyncio.run(self.check(email, show_all))
