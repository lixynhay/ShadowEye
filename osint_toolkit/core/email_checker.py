import asyncio
import os
import sys
import subprocess
import re
from typing import List, Dict, Any
from typing import List, Dict, Any
from ..ui import console, create_progress

SERVICE_PATTERNS = [
    r"\[\+\]\s*(.+)",
    r"\[-\]\s*(.+)",
    r"\[x\]\s*(.+)",
]

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
    def __init__(self, timeout: int = 90, proxy: str = None):
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

        if any(line.startswith(prefix) for prefix in ['[+]', '[-]', '[x]']):
            for pattern in SKIP_PATTERNS:
                if pattern in line:
                    return False
            return True

        if re.search(r"\b(?:site|service|account|username|email)\b", line, re.IGNORECASE):
            return False

        return False

    def _parse_line(self, line: str, show_all: bool) -> Dict[str, Any] | None:
        """Попытаться распознать строку вывода Holehe."""
        cleaned = line.strip()
        if not cleaned:
            return None

        for pattern in SERVICE_PATTERNS:
            match = re.match(pattern, cleaned)
            if match:
                service = match.group(1).strip()
                if not service:
                    return None
                for skip in SKIP_PATTERNS:
                    if skip in cleaned:
                        return None
                if cleaned.startswith('[+]'):
                    return {
                        "service": service,
                        "exists": True,
                        "details": "✓ Email найден",
                        "error": False,
                    }
                if cleaned.startswith('[-]'):
                    if show_all:
                        return {
                            "service": service,
                            "exists": False,
                            "details": "Не зарегистрирован",
                            "error": False,
                        }
                    return None
                if cleaned.startswith('[x]'):
                    if show_all:
                        return {
                            "service": service,
                            "exists": False,
                            "details": "⚠ Rate limit",
                            "error": True,
                        }
                    return None

        return None
    
    async def check(self, email: str, show_all: bool = False) -> List[Dict[str, Any]]:
        """Проверка email через Holehe."""
        if not self._holehe_available:
            return [{"service": "holehe", "exists": False, "details": "Holehe не установлен", "error": True}]

        results = []

        try:
            import holehe.core as holehe_core

            from io import StringIO
            buffer = StringIO()
            old_argv = sys.argv[:]
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            try:
                sys.argv = ['holehe', email]
                sys.stdout = buffer
                sys.stderr = buffer
                import trio
                trio.run(holehe_core.maincore)
            finally:
                sys.argv = old_argv
                sys.stdout = old_stdout
                sys.stderr = old_stderr

            combined_output = buffer.getvalue()

            if not combined_output.strip():
                console.print("[yellow]⚠ Holehe завершился без данных[/yellow]")
                return results

            for line in combined_output.split('\n'):
                line = line.strip()
                parsed = self._parse_line(line, show_all)
                if parsed:
                    results.append(parsed)

            found = sum(1 for r in results if r.get('exists'))
            not_found = sum(1 for r in results if not r.get('exists') and not r.get('error'))
            rate_limited = sum(1 for r in results if r.get('error'))

            console.print(f"[cyan]ℹ Всего проверено: {found + not_found + rate_limited}[/cyan]")
            console.print(f"[green]✓ Найдено: {found}[/green]")
            console.print(f"[red]✗ Не найдено: {not_found}[/red]")
            console.print(f"[yellow]⚠ Rate limit: {rate_limited}[/yellow]")

        except FileNotFoundError:
            console.print("[bold red]✗ Holehe не найден. Установите: pip install holehe[/bold red]")
            return [{"service": "holehe", "exists": False, "details": "Holehe не найден", "error": True}]
        except (TimeoutError, ConnectionError, OSError) as e:
            console.print(f"[yellow]⚠ Ошибка сети Holehe: {e}[/yellow]")
            return [{"service": "holehe", "exists": False, "details": f"Ошибка сети: {e}", "error": True}]
        except Exception as e:
            console.print(f"[yellow]⚠ Holehe завершился без данных: {e}[/yellow]")
            return [{"service": "holehe", "exists": False, "details": str(e), "error": True}]

        return results
    
    def run(self, email: str, show_all: bool = False) -> List[Dict[str, Any]]:
        return asyncio.run(self.check(email, show_all))
