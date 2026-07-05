import os
import subprocess
import sys
from typing import List, Dict, Any
from ..ui import console, create_progress

class UsernameChecker:
    def __init__(self, proxy: str = None, timeout: int = 30):
        self.proxy = proxy
        self.timeout = timeout
        self._sherlock_available = False
        self._sherlock_path = None
        self._check_tools()

    def _check_tools(self):
        sherlock_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'sherlock_builtin', 'sherlock.py'),
            os.path.expanduser('~/sherlock/sherlock_project/sherlock.py'),
        ]
        for p in sherlock_paths:
            if os.path.exists(p):
                self._sherlock_path = p
                self._sherlock_available = True
                break

        if self._sherlock_available:
            console.print(f"[green]✓ Sherlock найден: {self._sherlock_path}[/green]")

    def is_available(self) -> bool:
        return self._sherlock_available

    async def check(self, username: str) -> List[Dict[str, Any]]:
        if self._sherlock_available:
            return await self._check_sherlock(username)
        console.print("[bold red]✗ Sherlock не установлен[/bold red]")
        return []
    
    def _parse_sherlock_output(self, output: str) -> List[Dict[str, Any]]:
        results = []
        for line in output.splitlines():
            stripped = line.strip()
            if not stripped.startswith('[+]'):
                continue

            parts = stripped.replace('[+]', '', 1).split(':', 1)
            if len(parts) >= 2:
                service = parts[0].strip()
                url = parts[1].strip()
                results.append({
                    "service": service,
                    "exists": True,
                    "url": url,
                    "status": "Claimed",
                    "details": "",
                    "tags": [],
                    "ids": {}
                })
        return results

    async def _check_sherlock(self, username: str) -> List[Dict[str, Any]]:
        """Проверка через Sherlock."""
        results = []

        try:
            sherlock_script = self._sherlock_path or os.path.join(
                os.path.dirname(__file__), '..', 'sherlock_builtin', 'sherlock.py'
            )
            cmd = [sys.executable, sherlock_script, username, '--print-found', '--no-color']

            if self.proxy:
                cmd.extend(["--proxy", self.proxy])

            cmd.extend(["--timeout", str(self.timeout)])

            console.print(f"[cyan]ℹ Sherlock ищет: {username}[/cyan]")

            with create_progress() as progress:
                task = progress.add_task(f"[cyan]Sherlock сканирует...", total=100)
                try:
                    completed = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=max(20, self.timeout),
                        check=False,
                    )
                except subprocess.TimeoutExpired as exc:
                    combined_output = "\n".join(filter(None, [exc.stdout, exc.stderr]))
                    results = self._parse_sherlock_output(combined_output)
                    console.print("[yellow]⚠ Sherlock превысил время ожидания, используем частичные результаты[/yellow]")
                finally:
                    progress.update(task, completed=100)

            if not results:
                stdout_text = getattr(completed, 'stdout', '') or ''
                stderr_text = getattr(completed, 'stderr', '') or ''
                combined_output = "\n".join(filter(None, [stdout_text, stderr_text]))
                results = self._parse_sherlock_output(combined_output)

            if results:
                console.print(f"[green]✓ Найдено аккаунтов: {len(results)}[/green]")
            else:
                console.print("[yellow]⚠ Sherlock не вернул результатов[/yellow]")

        except Exception as e:
            console.print(f"[bold red]✗ Ошибка Sherlock: {e}[/bold red]")

        return results
    
    def run(self, username: str) -> List[Dict[str, Any]]:
        import asyncio
        return asyncio.run(self.check(username))
